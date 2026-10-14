"""Build a token ledger from supported local logs; never infer tokens from text length."""
import argparse
import collections
import datetime as dt
import json
from pathlib import Path

FIELDS = ('input_tokens', 'output_tokens', 'cached_input_tokens', 'total_tokens')


def timestamp(value, zone):
    if isinstance(value, (int, float)):
        return dt.datetime.fromtimestamp(value / 1000 if value > 100000000000 else value, zone)
    parsed = dt.datetime.fromisoformat(str(value).replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('Timestamp has no timezone')
    return parsed.astimezone(zone)


def cumulative_delta(current, previous, last_usage=None):
    """Repeated snapshots contribute zero; a reset uses its last response, not old totals."""
    previous = previous or {key: 0 for key in FIELDS}
    current = {key: int(current.get(key) or 0) for key in FIELDS}
    if current['total_tokens'] == previous['total_tokens']:
        return None, current, 'duplicate'
    if current['total_tokens'] < previous['total_tokens']:
        if not last_usage:
            return None, current, 'reset_without_last_usage'
        delta = {key: int(last_usage.get(key) or 0) for key in FIELDS}
        status = 'reset_from_last_usage'
    else:
        delta = {key: current[key] - previous.get(key, 0) for key in FIELDS}
        status = 'increment'
    if any(value < 0 for value in delta.values()):
        return None, current, 'negative_component'
    if delta['total_tokens'] != delta['input_tokens'] + delta['output_tokens']:
        return None, current, 'inconsistent_total'
    return delta, current, status


def collect(codex_root, workbuddy_root, index, mapping, cutoff):
    zone = cutoff.tzinfo
    start = dt.datetime(cutoff.year, 1, 1, tzinfo=zone)
    threads = mapping.get('threads', {})
    overrides = mapping.get('message_overrides', {})
    user_rows = {}
    for s in index:
        user_rows[s['source_id']] = sorted(s['messages'], key=lambda m: m['at'])

    def project_for(source_id, when, turn_id=None):
        candidates = user_rows.get(source_id, [])
        eligible = [m for m in candidates if timestamp(m['at'], zone) <= when]
        if turn_id:
            exact = [m for m in candidates if 'turn=' + turn_id + ' ' in m['locator']]
            if exact:
                eligible = exact
        if eligible:
            override = overrides.get(source_id + '/' + eligible[-1]['id'])
            if override:
                return override
        return threads.get(source_id, 'unassigned')

    ledger = []
    quality = collections.Counter()
    failures = []
    thread_meta = {}
    if codex_root:
        paths = sorted(Path(codex_root).rglob('*.jsonl'))
        for path in paths:
            own_id = path.stem[-36:]
            for line in path.open(encoding='utf-8'):
                d = json.loads(line)
                if d.get('type') == 'session_meta' and d.get('payload', {}).get('id') == own_id:
                    thread_meta[own_id] = d['payload']
                    break
        def root_id(tid):
            seen = set()
            while tid not in seen:
                seen.add(tid)
                parent = thread_meta.get(tid, {}).get('parent_thread_id')
                if not parent:
                    return tid
                tid = parent
            return tid
        seen_events = set()
        for path in paths:
            own_id = path.stem[-36:]
            if own_id not in thread_meta:
                quality['codex_files_without_own_metadata'] += 1
                continue
            active = False
            previous = None
            model = 'unknown'
            turn_id = None
            metadata = thread_meta[own_id]
            source = metadata.get('source') or {}
            is_spawned = isinstance(source, dict) and 'thread_spawn' in (source.get('subagent') or {})
            inherited_end = metadata.get('subagent_history_start_ordinal') if is_spawned else None
            for line_no, line in enumerate(path.open(encoding='utf-8'), 1):
                try:
                    d = json.loads(line)
                except ValueError:
                    failures.append({'source': path.name, 'line': line_no, 'error': 'invalid_json'})
                    continue
                p = d.get('payload', {})
                if d.get('type') == 'session_meta' and p.get('id') == own_id:
                    active = True
                if not active:
                    continue
                if inherited_end is not None and d.get('ordinal', 0) < inherited_end:
                    continue
                if d.get('type') == 'turn_context':
                    model = p.get('model') or model
                    turn_id = p.get('turn_id') or turn_id
                if d.get('type') == 'event_msg' and p.get('type') == 'task_started':
                    turn_id = p.get('turn_id') or turn_id
                if d.get('type') != 'event_msg' or p.get('type') != 'token_count' or not p.get('info'):
                    continue
                info = p['info']
                cumulative = info.get('total_token_usage')
                if not cumulative:
                    continue
                key = (own_id, d.get('ordinal', line_no), d.get('timestamp'))
                if key in seen_events:
                    quality['codex_duplicate_event_ids'] += 1
                    continue
                seen_events.add(key)
                delta, previous, status = cumulative_delta(cumulative, previous, info.get('last_token_usage'))
                quality['codex_' + status] += 1
                if not delta:
                    continue
                when = timestamp(d['timestamp'], zone)
                if not start <= when <= cutoff:
                    continue
                parent = root_id(own_id)
                kind = 'auto_review' if model == 'codex-auto-review' else ('delegated' if parent != own_id else 'primary')
                sid = 'codex:' + parent
                ledger.append({'source_id':'codex:'+own_id, 'event_id':str(d.get('ordinal',line_no)), 'locator':path.name+':'+str(line_no),'at':when.isoformat(),'model':model,'kind':kind,'project_id':project_for(sid,when,turn_id if own_id==parent else None),**delta})
                last = info.get('last_token_usage') or {}
                if last.get('total_tokens') != delta['total_tokens']:
                    quality['codex_delta_different_from_last_usage'] += 1
    if workbuddy_root:
        responses = {}
        for path in sorted(Path(workbuddy_root).rglob('*.jsonl')):
            sid = 'workbuddy:' + path.stem
            for line_no,line in enumerate(path.open(encoding='utf-8'),1):
                try:
                    d=json.loads(line)
                except ValueError:
                    failures.append({'source':path.name,'line':line_no,'error':'invalid_json'})
                    continue
                pd=d.get('providerData') or {}
                usage=pd.get('usage') or {}
                raw=pd.get('rawUsage') or {}
                if 'totalTokens' not in usage and 'total_tokens' not in raw:
                    continue
                when=timestamp(d.get('timestamp'),zone)
                if not start<=when<=cutoff:
                    continue
                response_id=pd.get('messageId')
                if not response_id:
                    quality['workbuddy_usage_without_response_id'] += 1
                    continue
                total=usage.get('totalTokens',raw.get('total_tokens'))
                input_tokens=usage.get('inputTokens',raw.get('prompt_tokens',0))
                output_tokens=usage.get('outputTokens',raw.get('completion_tokens',0))
                cached=(raw.get('prompt_tokens_details') or {}).get('cached_tokens',raw.get('prompt_cache_hit_tokens',0))
                event={'source_id':sid,'event_id':response_id,'locator':path.name+':'+str(line_no),'at':when.isoformat(),'model':pd.get('model') or 'unknown','kind':'primary','project_id':project_for(sid,when),'input_tokens':input_tokens,'output_tokens':output_tokens,'cached_input_tokens':cached,'total_tokens':total}
                if total != input_tokens+output_tokens:
                    quality['workbuddy_inconsistent_total'] += 1
                    continue
                key=(sid,response_id)
                if key in responses:
                    quality['workbuddy_duplicate_responses'] += 1
                    if responses[key]['total_tokens'] != total:
                        quality['workbuddy_conflicting_duplicate_usage'] += 1
                        # Preserve the last persisted response revision; disclose conflicts.
                responses[key]=event
        ledger.extend(responses.values())
    ledger.sort(key=lambda e:e['at'])
    return ledger,dict(quality),failures


def summarize(ledger,index,mapping):
    days=collections.defaultdict(lambda:{'total_tokens':0,'projects':collections.Counter()})
    projects=collections.defaultdict(lambda:{'total_tokens':0,'creative_tokens':0,'auto_review_tokens':0,'responses':0,'active_dates':set(),'token_dates':set()})
    models=collections.defaultdict(lambda:{'responses':0,'total_tokens':0})
    kinds=collections.Counter()
    for e in ledger:
        value=e['total_tokens'];day=e['at'][:10];p=projects[e['project_id']]
        days[day]['total_tokens']+=value;days[day]['projects'][e['project_id']]+=value
        p['total_tokens']+=value;p['responses']+=1;p['token_dates'].add(day)
        p['auto_review_tokens' if e['kind']=='auto_review' else 'creative_tokens']+=value
        kinds[e['kind']]+=value
        if e['kind']!='auto_review':
            models[e['model']]['responses']+=1;models[e['model']]['total_tokens']+=value
    for s in index:
        for m in s['messages']:
            pid=mapping.get('message_overrides',{}).get(s['source_id']+'/'+m['id'],mapping.get('threads',{}).get(s['source_id'],'unassigned'))
            projects[pid]['active_dates'].add(m['at'][:10])
    project_rows=[]
    for pid,p in projects.items():
        p={**p,'project_id':pid,'label':mapping.get('labels',{}).get(pid,pid),'active_dates':sorted(p['active_dates']),'token_dates':sorted(p['token_dates'])}
        p['active_days']=len(p['active_dates']);project_rows.append(p)
    daily=[{'date':day,'total_tokens':d['total_tokens'],'projects':dict(d['projects'])} for day,d in sorted(days.items())]
    return {'total_tokens':sum(e['total_tokens'] for e in ledger),'input_tokens':sum(e['input_tokens'] for e in ledger),'output_tokens':sum(e['output_tokens'] for e in ledger),'cached_input_tokens':sum(e['cached_input_tokens'] for e in ledger),'kinds':dict(kinds),'responses':len(ledger),'daily':daily,'peak_day':max(daily,key=lambda r:r['total_tokens']) if daily else None,'projects':sorted(project_rows,key=lambda r:r['creative_tokens'],reverse=True),'models':sorted([{'model':k,**v} for k,v in models.items()],key=lambda r:r['responses'],reverse=True)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex-root',type=Path)
    parser.add_argument('--workbuddy-root',type=Path)
    parser.add_argument('--index',type=Path,required=True)
    parser.add_argument('--project-map',type=Path,required=True)
    parser.add_argument('--cutoff',required=True,help='ISO timestamp with user timezone')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    cutoff=dt.datetime.fromisoformat(args.cutoff)
    if cutoff.tzinfo is None:parser.error('cutoff requires timezone')
    if not args.codex_root and not args.workbuddy_root:parser.error('at least one supported log root is required')
    index=json.loads(args.index.read_text(encoding='utf-8-sig'));mapping=json.loads(args.project_map.read_text(encoding='utf-8-sig'))
    ledger,quality,failures=collect(args.codex_root,args.workbuddy_root,index,mapping,cutoff)
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'token-ledger.jsonl').write_text('\n'.join(json.dumps(e,ensure_ascii=False) for e in ledger)+'\n',encoding='utf-8')
    result={**summarize(ledger,index,mapping),'cutoff':cutoff.isoformat(),'scope':'Local Codex + WorkBuddy only; cached input included; no ChatGPT token data','quality':quality,'failures':failures}
    (args.output/'usage-statistics.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('total_tokens','kinds','peak_day','models','quality','failures')},ensure_ascii=False))


if __name__=='__main__':main()
