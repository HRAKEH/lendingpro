from pathlib import Path
import shutil,re,json,zipfile,hashlib
root=Path('/mnt/data')
src=root/'zdrava-v8-rebuild'
dst=root/'zdrava-v8-motion'
if dst.exists():shutil.rmtree(dst)
shutil.copytree(src,dst)

motion_css=r'''/* ZDRAVA / Motion Studio v8.1 — progressive enhancement, no hidden content without JS. */
:root{--ease-expo:cubic-bezier(.16,1,.3,1)}
.hero{--glow-x:68%;--glow-y:44%;}
.hero::after{content:"";position:absolute;inset:0;z-index:0;pointer-events:none;background:radial-gradient(circle 240px at var(--glow-x) var(--glow-y),rgba(255,255,255,.34),transparent 100%);mix-blend-mode:screen;opacity:.8}
.hero-layout{z-index:2}.hero-copy{isolation:isolate}.display{position:relative}.line-clip{display:block;overflow:hidden;padding-bottom:.07em;margin-bottom:-.07em}.display .line{transform-origin:0 100%}.display .line.accent{position:relative;width:max-content;max-width:100%}
.display .line.accent:after{content:"";display:block;position:absolute;left:1%;right:1%;bottom:0;height:2px;background:currentColor;opacity:.5;transform:scaleX(0);transform-origin:left;animation:accent-sweep 1.1s var(--ease-expo) .88s forwards}
@keyframes accent-sweep{to{transform:scaleX(1)}}
.hero-art{isolation:isolate}
.hero-art .art-product{z-index:8;transform:translate3d(0,0,0);transition:filter .3s ease}
.art-prism{position:absolute;z-index:1;width:46%;height:52%;left:4%;top:13%;pointer-events:none;background:linear-gradient(130deg,rgba(255,255,255,.8),rgba(255,255,255,.08) 53%,color-mix(in srgb,var(--brand) 12%,transparent));backdrop-filter:blur(5px);-webkit-backdrop-filter:blur(5px);border:1px solid rgba(255,255,255,.6);box-shadow:inset 4px 8px 28px rgba(255,255,255,.68),19px 26px 60px rgba(23,64,74,.06);border-radius:51% 49% 58% 42%/35% 63% 37% 65%;transform:rotate(-19deg)}
.glacier .art-prism{border-radius:0;clip-path:polygon(13% 0,94% 10%,100% 81%,50% 100%,0 64%);transform:rotate(9deg);background:linear-gradient(130deg,rgba(255,255,255,.78),rgba(172,223,247,.22) 47%,rgba(27,116,174,.11) 100%)}
.art-orbit-line{position:absolute;z-index:3;top:14%;right:3%;width:35%;height:35%;border:1px solid color-mix(in srgb,var(--brand) 30%,transparent);border-radius:50%;transform:rotate(-26deg) scaleX(.6);opacity:.48;pointer-events:none}
.art-orbit-line::before{content:'';position:absolute;width:7px;height:7px;top:5%;left:23%;border-radius:100%;background:var(--brand);box-shadow:0 0 0 7px color-mix(in srgb,var(--brand) 10%,transparent)}
.stage-seal{position:absolute;z-index:9;top:12%;right:-5%;width:112px;height:112px;display:grid;place-content:center;text-align:center;border:1px solid rgba(255,255,255,.83);background:rgba(255,255,255,.28);backdrop-filter:blur(19px);-webkit-backdrop-filter:blur(19px);border-radius:50%;box-shadow:inset 4px 4px 16px rgba(255,255,255,.65),0 15px 35px rgba(30,69,81,.08);font:600 10px/1.45 var(--font-body);color:var(--brand);letter-spacing:.09em;text-transform:uppercase;pointer-events:none}
.stage-seal:before{content:'';display:block;width:20px;height:1px;background:var(--brand);margin:0 auto 12px;opacity:.6}
.hero-index::before{content:'';display:inline-block;width:44px;height:1px;background:var(--brand);margin-right:13px;vertical-align:middle;transform-origin:left;animation:scrollhint 2.8s var(--ease-expo) infinite}
@keyframes scrollhint{0%,100%{transform:scaleX(.3)}55%{transform:scaleX(1)}}
.hero-art .art-small{z-index:10;background:rgba(255,255,255,.38);border-radius:14px;box-shadow:inset 1px 1px 0 rgba(255,255,255,.95),0 22px 55px rgba(10,45,58,.10)}
.about-scene{background:radial-gradient(circle at 61% 47%,rgba(255,255,255,.90),transparent 40%),var(--surface)}
.about-scene:before{box-shadow:0 0 0 68px color-mix(in srgb,var(--brand) 3%,transparent);opacity:.73}
.about-scene img{will-change:auto}.about-scene:after{opacity:.68}
.about-scene .scene-text{position:absolute;z-index:3;left:26px;bottom:24px;font:600 11px var(--font-body);letter-spacing:.15em;color:var(--brand);text-transform:uppercase;pointer-events:none}
.about-scene .scene-point{position:absolute;z-index:1;width:13px;height:13px;border-radius:50%;background:var(--brand2);left:17%;top:22%;box-shadow:0 0 0 13px color-mix(in srgb,var(--brand2) 23%,transparent)}
.scenario,.ing{position:relative;isolation:isolate;overflow:hidden;transform:translateZ(0);transition:transform .45s var(--ease-expo),box-shadow .45s var(--ease-expo),background-color .45s var(--ease-expo)}
.scenario::before,.ing::before{content:'';position:absolute;z-index:-1;inset:-1px;background:radial-gradient(ellipse 260px 230px at var(--mx,50%) var(--my,30%),color-mix(in srgb,var(--brand2) 24%,transparent),transparent 68%);opacity:0;transition:opacity .35s ease;pointer-events:none}
.scenario:hover::before,.ing:hover::before{opacity:.85}.scenario:first-child::before{opacity:.12}.scenario:hover,.ing:hover{box-shadow:0 24px 65px -48px var(--ink);transform:translateY(-5px)}
.scenarios .chapter-bridge{display:flex;align-items:center;justify-content:space-between;gap:24px;margin-top:38px;color:var(--muted);font:700 10px/1.4 var(--font-body);text-transform:uppercase;letter-spacing:.14em;opacity:.75}
.bridge-line{height:1px;background:var(--line);flex:1;position:relative;overflow:hidden}
.bridge-line::before{content:'';display:block;width:28%;height:1px;background:var(--brand);animation:bridgesweep 5s ease-in-out infinite alternate}
@keyframes bridgesweep{from{transform:translateX(-100%)}to{transform:translateX(440%)}}
.how{position:relative;isolation:isolate;overflow:clip}.how::before{content:'';pointer-events:none;position:absolute;right:-15vw;top:-20%;width:65vw;aspect-ratio:1;border-radius:50%;background:radial-gradient(circle,color-mix(in srgb,var(--brand2) 7%,transparent),transparent 67%)}
.how-content{position:relative}.how-accent-wrap{position:relative;overflow:hidden;isolation:isolate}
.how-accent-wrap::before{content:"";position:absolute;z-index:-1;right:-38%;top:-40%;width:125%;aspect-ratio:1;border:1px solid rgba(255,255,255,.14);border-radius:50%;box-shadow:0 0 0 38px rgba(255,255,255,.028),0 0 0 92px rgba(255,255,255,.018);transform:rotate(24deg)}
.story-phase{width:100%;margin-top:34px;display:flex;align-items:center;gap:12px;font-size:10px;text-transform:uppercase;letter-spacing:.12em;color:rgba(255,255,255,.66)}
.story-phase strong{font-size:13px;letter-spacing:0;color:#fff;white-space:nowrap;margin-left:auto}
.story-progress{height:2px;flex:1;background:rgba(255,255,255,.22);overflow:hidden}
.story-progress i{display:block;width:100%;height:100%;background:var(--brand2);transform:scaleX(.333);transform-origin:left;transition:transform .55s var(--ease-expo)}
.how-content.is-motion-story .steps li{opacity:.38;transition:opacity .5s var(--ease-expo),transform .5s var(--ease-expo);transform:translateY(8px)}
.how-content.is-motion-story .steps li.is-active{opacity:1;transform:translateY(0)}
.how-content.is-motion-story .steps li.is-active .n{color:#fff}
.how-accent-wrap.is-step-2:before{transform:rotate(75deg) scale(1.06)}.how-accent-wrap.is-step-3:before{transform:rotate(130deg) scale(1.13)}
.how-accent-wrap:before{transition:transform 1.1s var(--ease-expo)}
.button{isolation:isolate;transition:transform .35s var(--ease-expo),box-shadow .35s var(--ease-expo),background .2s}
.button:before{content:'';position:absolute;inset:-55% -35%;pointer-events:none;z-index:-1;background:linear-gradient(105deg,transparent 34%,rgba(255,255,255,.27) 46%,transparent 58%);transform:translateX(-150%) skewX(-12deg);transition:transform .75s var(--ease-expo)}.button:hover:before{transform:translateX(150%) skewX(-12deg)}
.button .arrow{transition:transform .4s var(--ease-expo)}.button:hover .arrow{transform:translate(5px,-4px) rotate(10deg)}
.faq-list details[open]{background:linear-gradient(90deg,color-mix(in srgb,var(--brand2) 14%,transparent),transparent 65%)}
.faq-list details[open] summary{padding-left:12px;transition:padding .35s var(--ease-expo)}
@media(min-width:1100px){.how-content .steps li{min-height:192px;align-items:center}.how-content .how-accent-wrap{align-self:start;position:sticky;top:146px;min-height:390px}.stage-seal{right:-2%}.hero-copy .eyebrow{width:max-content}}
@media(max-width:1099px){.stage-seal{right:1%;top:5%;width:86px;height:86px;font-size:8px}.art-prism{left:3%}.how-content.is-motion-story .steps li{opacity:1;transform:none}.story-phase{gap:10px}}
@media(max-width:550px){.hero::after{opacity:.32}.art-prism{width:53%;height:49%;left:0%;top:16%;backdrop-filter:none;-webkit-backdrop-filter:none}.art-orbit-line{width:31%;height:31%;right:1%;top:20%}.stage-seal{width:72px;height:72px;right:1%;top:2%;font-size:7px;border-width:1px;backdrop-filter:blur(7px)}.stage-seal:before{width:13px;margin-bottom:5px}.hero-art .art-small{border-radius:10px}.scenarios .chapter-bridge{gap:11px;font-size:9px}.scenarios .chapter-bridge span{max-width:90px}.story-phase{margin-top:20px}.about-scene .scene-text{left:18px;bottom:15px;font-size:9px}.about-scene .scene-point{width:8px;height:8px}.hero-index::before{animation:none}.button:before{display:none}}
@media(hover:none){.scenario::before,.ing::before{display:none}.button:before{display:none}}
@media(prefers-reduced-motion:reduce){.display .line.accent::after{animation:none;transform:scaleX(1)}.bridge-line::before,.hero-index::before{animation:none!important}.how-content.is-motion-story .steps li{opacity:1!important;transform:none!important}.stage-seal,.art-prism,.art-orbit-line{transform:none!important}.hero::after{display:none}}
'''

motion_js=r'''/* ZDRAVA v8.1 Motion Studio — fast, reversible JS. Native HTML is fully visible if CDNs fail. */
(()=>{
'use strict';
const doc=document;
const reduce=window.matchMedia('(prefers-reduced-motion: reduce)');
const mobile=window.matchMedia('(max-width: 550px)');
const desktop=window.matchMedia('(min-width: 1100px)');
const fine=window.matchMedia('(hover:hover) and (pointer:fine)');
const nav=doc.getElementById('nav');
const trigger=doc.getElementById('menu-trigger');
function closeMenu(){if(!nav||!trigger)return;nav.classList.remove('is-open');trigger.setAttribute('aria-expanded','false');trigger.setAttribute('aria-label','Открыть меню')}
if(nav&&trigger){trigger.addEventListener('click',()=>{const opened=nav.classList.toggle('is-open');trigger.setAttribute('aria-expanded',String(opened));trigger.setAttribute('aria-label',opened?'Закрыть меню':'Открыть меню')});nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));doc.addEventListener('keydown',e=>{if(e.key==='Escape')closeMenu()});doc.addEventListener('click',e=>{if(!nav.contains(e.target)&&!trigger.contains(e.target))closeMenu()})}
const progress=doc.querySelector('.progress span');const dock=doc.querySelector('.mobile-dock');const hero=doc.querySelector('.hero');const buy=doc.getElementById('buy');
let rafBusy=false;
function updateUI(){rafBusy=false;const max=doc.documentElement.scrollHeight-innerHeight;if(progress)progress.style.transform='scaleX('+(max>0?Math.min(1,Math.max(0,scrollY/max)):0)+')';if(dock){const h=hero?.getBoundingClientRect().bottom??400;const b=buy?.getBoundingClientRect().top??10000;dock.classList.toggle('is-visible',mobile.matches&&h<130&&b>innerHeight*.5)}}
function onScroll(){if(!rafBusy){rafBusy=true;requestAnimationFrame(updateUI)}}
window.addEventListener('scroll',onScroll,{passive:true});window.addEventListener('resize',onScroll,{passive:true});updateUI();
function track(name){try{window.dataLayer?.push({event:'zdrava_'+name});if(window.ZDRAVA_METRIKA_ID&&typeof window.ym==='function')window.ym(window.ZDRAVA_METRIKA_ID,'reachGoal',name)}catch(_) {}}
doc.addEventListener('click',e=>{const target=e.target.closest('[data-event]');if(target)track(target.dataset.event)});
if(buy&&'IntersectionObserver'in window){const observer=new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting)){track('buy_section');observer.disconnect()}},{threshold:.35});observer.observe(buy)}
const how=doc.querySelector('.how-content');const steps=Array.from(doc.querySelectorAll('.steps li'));const current=doc.querySelector('[data-current-step]');const meter=doc.querySelector('[data-story-progress]');const accent=doc.querySelector('.how-accent-wrap');
function setStep(index){if(!how||!steps.length)return;const active=Math.min(Math.max(index,0),steps.length-1);steps.forEach((el,i)=>el.classList.toggle('is-active',i===active));if(current)current.textContent=(active+1)+' / '+steps.length;if(meter)meter.style.transform='scaleX('+((active+1)/steps.length)+')';if(accent){accent.classList.toggle('is-step-2',active===1);accent.classList.toggle('is-step-3',active===2)}}
setStep(0);
if(reduce.matches)return;
const gsap=window.gsap;const ST=window.ScrollTrigger;
if(!gsap||!ST){ // Functional fallback. The page never relies on a CDN for content.
 if(fine.matches&&desktop.matches)setupPointer();
 return;
}
gsap.registerPlugin(ST);
// Extra movement on desktop only: no artificial smooth scrolling on phones or tablets.
if(desktop.matches&&fine.matches&&typeof window.Lenis==='function'){
 try{const lenis=new window.Lenis({duration:1.08,smoothWheel:true,autoRaf:false});lenis.on('scroll',ST.update);gsap.ticker.add(t=>lenis.raf(t*1000));gsap.ticker.lagSmoothing(0)}catch(_){/* use browser scrolling */}
}
// One opening sequence with editorial line masks and a precise product reveal.
const entry=gsap.timeline({defaults:{ease:'power3.out'}});
entry.from('.display .line',{yPercent:112,opacity:0,duration:1.22,stagger:.14,clearProps:'all'})
.from('.hero-copy .eyebrow',{y:12,opacity:0,duration:.7,clearProps:'all'},.10)
.from('.hero-copy .subtitle',{y:26,opacity:0,duration:.85,clearProps:'all'},.34)
.from('.hero-copy .actions',{y:22,opacity:0,duration:.85,clearProps:'all'},.50)
.from('.hero-note',{y:12,opacity:0,duration:.65,clearProps:'all'},.68)
.from('.art-product',{y:85,scale:.95,opacity:0,duration:1.45,ease:'expo.out',clearProps:'all'},.12)
.from('.art-prism',{x:-48,rotate:-16,opacity:0,duration:1.8,ease:'expo.out',clearProps:'all'},.10)
.from('.stage-seal,.art-small',{y:18,opacity:0,stagger:.14,duration:.8,clearProps:'all'},.78);
// Parallax only for decoration, never warp the packaging or lettering.
if(desktop.matches){
 const scrub={trigger:hero,start:'top top',end:'bottom top',scrub:1.4,invalidateOnRefresh:true};
 gsap.to('.art-prism',{y:-90,rotation:32,ease:'none',scrollTrigger:scrub});
 gsap.to('.art-orbit-line',{y:-47,rotation:-18,ease:'none',scrollTrigger:{...scrub,scrub:1.7}});
 gsap.to('.art-ring',{y:45,scale:1.09,ease:'none',scrollTrigger:{...scrub,scrub:1.1}});
 const aboutImage=doc.querySelector('.about-scene img');if(aboutImage)gsap.fromTo(aboutImage,{y:20},{y:-32,ease:'none',scrollTrigger:{trigger:'.about-scene',start:'top bottom',end:'bottom top',scrub:1.1}});
}
// Animated facts preserve their true value if JS is disabled.
if(desktop.matches){doc.querySelectorAll('.counter').forEach(el=>{const actual=Number(el.dataset.value);if(!Number.isFinite(actual))return;const state={n:actual};gsap.fromTo(state,{n:0},{n:actual,duration:1.12,ease:'power2.out',scrollTrigger:{trigger:el.closest('.how')||el,start:'top 78%',once:true},onUpdate:()=>{el.textContent=String(Math.round(state.n))},onComplete:()=>{el.textContent=String(actual)}})})}
// Repeated sections animate once, and never fade again when scrolling backward.
const selector='.section .kicker,.section .section-heading,.section .section-lead,.about-grid,.scenario,.ing,.steps li,.faq-list details,.buy .section-heading,.buy .actions';
const all=gsap.utils.toArray(selector);all.forEach(el=>{
 // Never fade/how-steps after activating our sticky scrollytelling.
 if(desktop.matches&&el.matches('.steps li'))return;
 gsap.from(el,{y:mobile.matches?13:35,autoAlpha:0,duration:mobile.matches?.58:.82,ease:'power2.out',clearProps:'all',scrollTrigger:{trigger:el,start:mobile.matches?'top 98%':'top 89%',once:true}});
});
// Desktop scroll narrative: one pin-like sticky product fact panel, three states.
if(desktop.matches&&how&&steps.length){
 how.classList.add('is-motion-story');setStep(0);
 steps.forEach((step,i)=>{ST.create({trigger:step,start:'top 60%',end:'bottom 43%',onEnter:()=>setStep(i),onEnterBack:()=>setStep(i)})});
 ST.create({trigger:how,start:'top 52%',end:'bottom 50%',onUpdate:self=>{ // left rail advances continuously, steps snap to readable positions
 if(meter){const phase=Math.min(1,Math.max(0,self.progress));meter.style.transform='scaleX('+(Math.max(1/steps.length,phase))+')'}
 }});
}
if(fine.matches&&desktop.matches)setupPointer();
function setupPointer(){
 const art=doc.querySelector('.hero-art');
 if(art){let scheduled=false;let px=0,py=0;art.addEventListener('pointermove',e=>{const r=art.getBoundingClientRect();px=(e.clientX-r.left-r.width/2)/r.width;py=(e.clientY-r.top-r.height/2)/r.height;if(!scheduled){scheduled=true;requestAnimationFrame(()=>{art.style.setProperty('--px',String(px));art.style.setProperty('--py',String(py));scheduled=false})}});art.addEventListener('pointerleave',()=>{art.style.setProperty('--px','0');art.style.setProperty('--py','0')})}
 if(hero){const onMove=e=>{const box=hero.getBoundingClientRect();hero.style.setProperty('--glow-x',((e.clientX-box.left)/box.width*100).toFixed(1)+'%');hero.style.setProperty('--glow-y',((e.clientY-box.top)/box.height*100).toFixed(1)+'%')};hero.addEventListener('pointermove',onMove,{passive:true})}
 doc.querySelectorAll('.scenario,.ing').forEach(card=>{card.addEventListener('pointermove',e=>{const r=card.getBoundingClientRect();card.style.setProperty('--mx',((e.clientX-r.left)/r.width*100).toFixed(1)+'%');card.style.setProperty('--my',((e.clientY-r.top)/r.height*100).toFixed(1)+'%')},{passive:true})});
}
})();
'''
# Replacement of existing JS embedded in <script>document.addEventListener('DOMContentLoaded',()=>{...});</script>.
for key in ('hot-ice','mikozacid'):
 p=dst/key/'index.html'
 html=p.read_text(encoding='utf-8')
 css=(dst/key/'source-design.css').read_text(encoding='utf-8')
 (dst/key/'source-design.css').write_text(css+'\n'+motion_css,encoding='utf-8')
 (dst/key/'source-motion.js').write_text(motion_js,encoding='utf-8')
 # replace exact <style> ... </style> first
 html,n=re.subn(r'(<style>)(.*?)(</style>)', lambda m:m.group(1)+css+'\n'+motion_css+m.group(3),html,count=1,flags=re.S)
 assert n==1,key
 # replace second inline script (first configuration and JSON-LD separate; one containing DOMContentLoaded)
 html,n=re.subn(r'<script>document\.addEventListener\(\x27DOMContentLoaded\x27,\(\)=>\{.*?</script>', '<script>document.addEventListener(\'DOMContentLoaded\',()=>{'+motion_js+'});</script>', html,count=1,flags=re.S)
 assert n==1,(key,'js block')
 # inject mask wrappers, art-prism elements, visual seal.
 html,n=re.subn(r'(<h1[^>]+class="display">)(.*?)(</h1>)',lambda m:m.group(1)+re.sub(r'(<span class="line(?: accent)?">.*?</span>)',r'<span class="line-clip">\1</span>',m.group(2))+m.group(3),html,count=1,flags=re.S)
 assert n==1
 # art components inside stage, before art-number and after image, unmodfied images
 html=html.replace('<span class="art-number"', '<div class="art-prism" aria-hidden="true"></div><div class="art-orbit-line" aria-hidden="true"></div><span class="art-number"',1)
 textlabel='ЛЕДЯНАЯ<br>СВЕЖЕСТЬ' if key=='hot-ice' else 'ТИХИЙ<br>УХОД'
 html=html.replace('<div class="art-small">', f'<div class="stage-seal" aria-hidden="true">{textlabel}</div><div class="art-small">',1)
 # Scene signature label, decoration only, before about-scene image
 html=html.replace('<div class="about-scene"><img ', '<div class="about-scene"><span class="scene-point" aria-hidden="true"></span><span class="scene-text" aria-hidden="true">ЗДРАВА / ФОРМУЛЫ УХОДА</span><img ',1)
 # Narration pause under scenarios grid, preserving section order.
 marker='</div></div></section>\n<!-- Section 4: ingredient groups'
 assert marker in html
 html=html.replace(marker, '</div><div class="chapter-bridge" aria-hidden="true"><span>Ключевые моменты</span><i class="bridge-line"></i><span>Состав средства</span></div></div></section>\n<!-- Section 4: ingredient groups',1)
 # Three-step story status inside aside
 marker2='</div></div></div></section>\n<!-- Section 6: native details'
 assert marker2 in html
 html=html.replace(marker2,'<div class="story-phase" aria-hidden="true"><span>Шаг</span><i class="story-progress"><i data-story-progress></i></i><strong data-current-step>1 / 3</strong></div></div></div></div></section>\n<!-- Section 6: native details',1)
 p.write_text(html,encoding='utf-8')

# README release notes
readme=dst/'README_TIMEWEB.md'
text=readme.read_text(encoding='utf-8')
text='''# ЗДРАВА v8.1 — MOTION STUDIO (обновление анимаций)

Эта версия содержит оригинальные фото и графику v8. Внесены только изменения в интерфейс, анимации и два декоративных элемента секций. Базовая v8 сохранена в отдельной ветке GitHub (после выгрузки).

## Эффекты
- Открытие hero в стиле editorial typography: строки H1 появляются из маски; упаковка движется вперёд без деформации этикетки.
- Многослойная ледяная / ботаническая сцена с прозрачным призмовым стеклом, отсветом и тонкой орбитой.
- Desktop pointer lighting и мягкий parallax декоративных слоёв по скроллу, а не самой упаковки.
- Эффектная прокрутка «3 шага ухода»: sticky-панель со счётчиком длительности, подсветка шага, прогресс.
- Hover spotlight для карточек, более уверенные CTA, разовое появление заголовков/блоков.
- Mobile: лёгкие короткие появления, без Lenis, тяжёлого parallax и scroll-pin.
- reduced-motion и отключённый JavaScript: весь контент остаётся видимым, нативные FAQ и ссылки работают.

Никакого видео/Canvas/WebGL: достаточно CSS + GSAP/ScrollTrigger, Lenis только на мощных десктопах. Если библиотеки недоступны, сайт работает статично.

'''+text
readme.write_text(text,encoding='utf-8')

archive=root/'zdrava-v8-motion-studio-timeweb.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as z:
 for p in sorted(dst.rglob('*')):
  if p.is_file(): z.write(p,p.relative_to(dst))
print('ARCHIVE',archive,archive.stat().st_size)
print('FILES',[(str(p.relative_to(dst)),p.stat().st_size) for p in sorted(dst.rglob('*')) if p.is_file()])
