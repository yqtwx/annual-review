"""Render an offline annual review from verified presentation data. Standard library only."""
import argparse
import json
import math
import re
from pathlib import Path


def demo_data():
    return {
        "year": 2025, "title": "我的 GPT\n年度报告。",
        "subtitle": "A YEAR OF MAKING / 设计预览",
        "period": "2025.01.01 — 2025.12.31 · 虚构示例",
        "coverage": "本页所有作品、数字与对话均为虚构示例，只用于展示视觉与阅读节奏。",
        "demo": True, "closing": "下一页，留给还没完成的想象。",
        "summary": {"portrait": "把好奇，做成作品。", "body": "虚构示例：不断尝试与调整，找到自己的表达。", "tags": ["好奇", "尝试", "打磨"], "metrics": [{"value": "12", "label": "示例项目"}, {"value": "86", "label": "示例活跃日"}]},
        "profile": {"name": "虚构示例"},
        "share_card": {"html": "demo-card.html", "hero": {"value": "128", "unit": "万", "label": "虚构示例 Token"}, "project_types": ["工具探索", "视觉创作"], "metrics": [{"value": "12", "label": "示例项目"}, {"value": "86", "label": "示例活跃日"}], "display_date": "2025 / 虚构示例"},
        "chapters": [
            {"id": "footprints", "eyebrow": "01 / 留下的足迹", "title": "一些问题，\n终于有了自己的形状。",
             "body": "从一张草稿开始，到一个真正能打开的页面。\n你一次次把想法交给现实，再把反馈带回下一次修改。",
             "metrics": [{"value": "12", "label": "虚构示例项目", "note": "这里会替换为经核验的项目数"}, {"value": "86", "label": "虚构示例活跃日", "note": "不代表实际用户活动"}]},
            {"id": "works", "tone": "light", "eyebrow": "02 / 年度作品", "title": "这一年，\n有几件事值得留下。",
             "body": "作品不必很大。它只需要回答一个你在意的问题。",
             "projects": [{"name": "城市声音档案", "status": "虚构作品 / 设计示例", "description": "把日常采集整理成可以重新聆听的地图。"}, {"name": "一页书店", "status": "虚构作品 / 设计示例", "description": "给每一本喜爱的书，留一段被记住的理由。"}]},
            {"id": "voice", "tone": "sage", "eyebrow": "03 / 记住一句话", "title": "你在意的，\n慢慢变得更清楚。",
             "body": "真正的报告会从你的原始对话中找到这一刻，并保留日期和依据。",
             "quote": {"text": "我想让它更简单，也更像我。", "attribution": "虚构台词 · 非用户原话"},
             "sources": [{"id": "demo-001", "label": "设计示例，非真实来源", "locator": "实际报告将在此显示可核验的记录位置"}]},
            {"id": "unfinished", "eyebrow": "04 / 未完待续", "title": "没做完的，\n也属于这一年。",
             "body": "有的方向被放下，有的想法还在等待。\n它们不是用来填满成绩单的空白，而是故事本来的样子。"}
        ]
    }


def validate(data):
    def fail(message):
        raise ValueError(message)

    def strings(obj, fields, where):
        if not isinstance(obj, dict):
            fail(f"{where} must be an object")
        for field in fields:
            if not isinstance(obj.get(field), str) or not obj[field].strip():
                fail(f"{where}.{field} must be non-empty text")

    strings(data, ("title", "period", "coverage"), "report")
    if type(data.get("year")) is not int or not 1900 <= data["year"] <= 9999:
        fail("year must be an integer from 1900 to 9999")
    if "demo" in data and type(data["demo"]) is not bool:
        fail("demo must be boolean")
    for key in ("subtitle", "closing"):
        if key in data and not isinstance(data[key], str):
            fail(f"{key} must be text")
    chapters = data.get("chapters")
    if not isinstance(chapters, list) or not chapters:
        fail("chapters must be a non-empty list")
    seen = {"cover", "closing", "report", "report-data", "progress", "prev", "next", "counter", "catalog-button", "motion-button", "evidence-dialog", "dialog-title", "dialog-body", "dialog-close"}
    for ch in chapters:
        strings(ch, ("id", "title", "body"), "chapter")
        if ch["id"] in seen:
            fail(f"duplicate or reserved chapter id: {ch['id']}")
        seen.add(ch["id"])
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', ch['id']):
            fail('chapter id must be a safe unique identifier')
        if ch.get("tone", "dark") not in ("dark", "light", "sage", "blue", "coral", "pink", "yellow"):
            fail("invalid chapter tone")
        if "eyebrow" in ch and not isinstance(ch["eyebrow"], str):
            fail("eyebrow must be text")
        for key, fields in (("metrics", ("value", "label")), ("projects", ("name", "description")), ("sources", ("id", "label", "locator"))):
            items = ch.get(key, [])
            if not isinstance(items, list):
                fail(f"{key} must be a list")
            if key == "metrics" and len(items) > 2:
                fail("at most two metrics per chapter")
            for item in items:
                strings(item, fields, key)
                for optional in ("note", "status"):
                    if optional in item and not isinstance(item[optional], str):
                        fail(f"{key}.{optional} must be text")
        if "quote" in ch:
            strings(ch["quote"], ("text", "attribution"), "quote")
        hero = ch.get('hero')
        if hero is not None:
            if not isinstance(hero, dict):
                fail('hero must be an object')
            if 'text' in hero:
                strings(hero, ('text',), 'hero')
            else:
                value = hero.get('value')
                scale = hero.get('scale', 1)
                if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
                    fail('hero.value must be a finite non-negative number')
                if type(scale) not in (int, float) or not math.isfinite(scale) or scale <= 0:
                    fail('hero.scale must be positive')
                decimals = hero.get('decimals', 0)
                if type(decimals) is not int or not 0 <= decimals <= 4:
                    fail('hero.decimals must be between zero and four')
        for key in ('bars', 'distribution'):
            if key not in ch:
                continue
            if not isinstance(ch[key], list) or not ch[key]:
                fail(key + ' must be a non-empty list')
            total = 0
            for item in ch[key]:
                strings(item, ('label',), key)
                value = item.get('value')
                if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
                    fail(key + '.value must be finite and non-negative')
                if 'color' in item and not re.fullmatch(r'#[0-9a-fA-F]{6}', item['color']):
                    fail(key + '.color must be a six-digit hex color')
                total += value
            if total <= 0:
                fail(key + ' must have a positive total')
    for link in data.get('downloads', []):
        strings(link, ('label', 'href'), 'download')
        if re.match(r'^[A-Za-z]+:', link['href']) or link['href'].startswith(('//', '/')) or '..' in link['href'].split('/'):
            fail('downloads must use safe relative local paths')
    for obj, keys in ((data.get('artwork', {}), ('src',)), (data.get('music', {}), ('src',)), (data.get('share_card', {}), ('image', 'html'))):
        if not isinstance(obj, dict):
            fail('asset configuration must be an object')
        for key in keys:
            if key not in obj:
                continue
            path = obj[key]
            if not isinstance(path, str) or not path or '\\' in path or re.match(r'^[A-Za-z]+:', path) or path.startswith(('/', '//')) or '..' in path.split('/'):
                fail('assets must use safe relative local paths')
    embedded = data.get('share_card', {}).get('download_data')
    if embedded is not None and (not isinstance(embedded, str) or len(embedded) > 32000000 or not re.fullmatch(r'data:image/png;base64,[A-Za-z0-9+/]+=*', embedded)):
        fail('share_card.download_data must be a bounded PNG data URI')


def render(data, template):
    validate(data)
    marker = "__ANNUAL_REVIEW_DATA__"
    if template.count(marker) != 1:
        raise ValueError("template must contain exactly one data marker")
    payload = json.dumps(data, ensure_ascii=False).replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    assets = Path(__file__).resolve().parents[1] / 'assets'
    for marker_name, names in {
        '__ANNUAL_REVIEW_STYLE__': ['editorial.css', 'persona-reveal.css', 'fashion.css', 'holographic.css', 'usage-panels.css', 'compact-controls.css'],
        '__ANNUAL_REVIEW_ENHANCEMENTS__': ['editorial.js', 'usage-panels.js'],
        '__ANNUAL_REVIEW_CARD_FOIL__': ['card-foil.css'],
    }.items():
        if marker_name in template:
            template = template.replace(marker_name, '\n'.join((assets / name).read_text(encoding='utf-8') for name in names))
    return template.replace(marker, payload)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--data", type=Path, help="Verified report-data.json")
    source.add_argument("--demo", action="store_true", help="Render clearly marked fictional design preview")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--force", action="store_true", help="Explicitly overwrite an existing output")
    parser.add_argument("--card", action="store_true", help="Render the independent 9:16 share-card HTML; requires summary and share_card data")
    args = parser.parse_args()
    if args.output.exists() and not args.force:
        parser.error("output already exists; choose a new path or explicitly use --force")
    if args.data and args.output.resolve() == args.data.resolve():
        parser.error("output must not replace input data")
    try:
        data = demo_data() if args.demo else json.loads(args.data.read_text(encoding="utf-8-sig"))
        if args.card and not all(data.get(key) for key in ('summary', 'share_card')):
            raise ValueError('share card requires summary and share_card data')
        template_path = Path(__file__).resolve().parents[1] / "assets" / ("share-card-template.html" if args.card else "report-template.html")
        html = render(data, template_path.read_text(encoding="utf-8"))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w" if args.force else "x", encoding="utf-8") as target:
            target.write(html)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(str(args.output.resolve()))


if __name__ == "__main__":
    main()
