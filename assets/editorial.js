// Decorative elements are original graphics and carry no statistical meaning.
for(const [i,p] of [...document.querySelectorAll('.page')].entries()){
 const o=el('div','ornaments',undefined,p);o.setAttribute('aria-hidden','true');
 el('div','dot-field',undefined,o);el('div','ribbon',undefined,o);el('div','edge-code',`ARCHIVE / ${data.year} / ${String(i+1).padStart(2,'0')}`,o);
 const stamp=el('div','archive-stamp',undefined,o);el('span','','IN THE MAKING',stamp);el('b','','✦',stamp);el('span','','独属于你的形状',stamp);el('div','folio',`FIELD NOTES   /   ${String(i+1).padStart(2,'0')}   —   ${data.year}`,p);
}
if(data.share_card?.image){
 end.c.replaceChildren();const layout=el('div','final-layout',undefined,end.c),copy=el('div','final-copy',undefined,layout);
 el('p','final-label',data.summary?.eyebrow||'YOUR YEAR / YOUR CHARACTER',copy);el('h2','title',data.summary?.display_title||data.summary?.portrait,copy);if(data.summary?.display_title)el('p','final-persona',data.summary?.portrait.replaceAll('\n',''),copy);el('p','body',data.summary?.body,copy);tags(data.summary?.tags,copy);
 const facts=el('div','final-facts',undefined,copy);for(const m of (data.summary?.metrics||[]).slice(0,4)){const f=el('div','final-fact',undefined,facts);el('b','',m.value,f);el('span','',m.label,f)}
 el('p','summary-note',data.summary?.note,copy);sources(data.summary?.sources,copy);
 const card=el('div','final-card',undefined,layout),img=el('img','share-preview',undefined,card);img.src=data.share_card.image;img.alt='年度画像分享卡：'+data.summary?.portrait.replaceAll('\n','');
 const save=el('a','save-card','保存我的年度卡片 ↓',card);save.href=data.share_card.download_data||data.share_card.image;save.download='我的'+data.year+'年度卡片.png';
 layout.inert=true;layout.setAttribute('aria-hidden','true');end.p.classList.add('awaiting-reveal');end.p.setAttribute('aria-busy','true');
 const loader=el('div','persona-loader',undefined,end.c);loader.setAttribute('role','status');loader.setAttribute('aria-live','polite');
 el('p','loader-kicker','YOUR YEAR / YOUR AI PERSONA',loader);el('h2','loader-title','正在生成你的年度 AI 形象',loader);
 const meter=el('div','persona-meter',undefined,loader);meter.setAttribute('role','progressbar');meter.setAttribute('aria-label','年度 AI 形象揭晓进度');meter.setAttribute('aria-valuemin','0');meter.setAttribute('aria-valuemax','100');meter.setAttribute('aria-valuenow','0');const fill=el('div','persona-fill',undefined,meter);
 const percent=el('span','persona-percent','0%',loader);percent.setAttribute('aria-hidden','true');el('p','loader-hint','从这一年的创作里，找到你的专属形状。',loader);el('p','loader-disclosure','形象已根据年度总结生成 · 此处为揭晓动画',loader);
 let started=false,finished=false;
 function completeReveal(){if(finished)return;finished=true;fill.style.width='100%';meter.setAttribute('aria-valuenow','100');percent.textContent='100%';layout.inert=false;layout.removeAttribute('aria-hidden');end.p.setAttribute('aria-busy','false');end.p.classList.remove('awaiting-reveal');end.p.classList.add('persona-ready');loader.setAttribute('aria-hidden','true');revealObserver.disconnect()}
 const revealObserver=new IntersectionObserver(entries=>{if(started||!entries.some(e=>e.isIntersecting&&e.intersectionRatio>=.25))return;started=true;if(paused||reduced.matches){completeReveal();return}let start=performance.now();function frame(now){if(paused||reduced.matches){completeReveal();return}const x=Math.min(1,(now-start)/3200);const value=Math.round(100*(1-Math.pow(1-x,1.3)));fill.style.width=value+'%';meter.setAttribute('aria-valuenow',String(value));percent.textContent=value+'%';if(x<1)requestAnimationFrame(frame);else completeReveal()}requestAnimationFrame(frame)},{threshold:.25});revealObserver.observe(end.p);
 window.addEventListener('beforeprint',completeReveal);
}
if(data.music?.src){
 const audio=new Audio(data.music.src);audio.loop=true;audio.preload='metadata';audio.volume=.2;window.annualAudio=audio;
 const dock=el('div','music-dock',undefined,document.body),b=el('button','music-toggle',undefined,dock);b.type='button';
 b.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="2.5"/><path d="M12 6.5a5.5 5.5 0 0 1 5.5 5.5M6.5 12a5.5 5.5 0 0 0 5.5 5.5"/><path class="music-slash" d="M4 4l16 16"/></svg>';
 let enabled=data.music.autoplay!==false,autoplayPending=enabled;
 function state(){b.setAttribute('aria-pressed',String(enabled));b.setAttribute('aria-label',enabled?'关闭背景音乐':'开启背景音乐');b.title=enabled?'关闭背景音乐':'开启背景音乐';dock.classList.toggle('music-enabled',enabled);dock.classList.toggle('music-playing',!audio.paused)}
 function disarm(){autoplayPending=false;document.removeEventListener('pointerdown',onGesture,true);document.removeEventListener('keydown',onGesture,true)}
 function arm(){autoplayPending=true;document.addEventListener('pointerdown',onGesture,true);document.addEventListener('keydown',onGesture,true)}
 async function onGesture(e){if(!autoplayPending||!enabled||e.target.closest?.('.music-dock'))return;try{await audio.play()}catch{}}
 b.onclick=async()=>{enabled=!enabled;if(enabled){arm();try{await audio.play()}catch{}}else{disarm();audio.pause()}state()};audio.onplay=()=>{disarm();state()};audio.onpause=state;
 state();if(enabled){arm();audio.autoplay=true;audio.play().catch(()=>{});}
 const credit=el('a','music-credit',data.music.title+' · 音乐署名',document.body);credit.href='music-credits.html';credit.target='_blank';credit.rel='noopener';
}
