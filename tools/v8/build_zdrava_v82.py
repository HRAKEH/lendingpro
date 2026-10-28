from pathlib import Path
import re, zipfile, hashlib, json, shutil
root=Path('/mnt/data/zdrava-v82')
original=Path('/mnt/data/zdrava-v8-motion-studio-timeweb.zip')
colors={'hot-ice':'ЛЁД / ДВИЖЕНИЕ / СВЕЖЕСТЬ','mikozacid':'ЧИСТОТА / УХОД / БАЛАНС'}
css=r'''
/* === v8.2 KINETIC EDITORIAL: strictly decorative, CSS/transform only === */
.motion-ribbon{position:relative;isolation:isolate;overflow:hidden;background:var(--ink);color:rgba(255,255,255,.82);border-block:1px solid color-mix(in srgb,var(--ink) 78%,#fff);padding:17px 0;min-height:64px;display:flex;align-items:center}
.motion-ribbon-track{display:flex;gap:46px;white-space:nowrap;width:max-content;will-change:transform;animation:v82-ticker 38s linear infinite}
.motion-ribbon span{display:inline-flex;align-items:center;gap:46px;font:600 clamp(12px,1.5vw,16px)/1 var(--font-title);letter-spacing:.15em;text-transform:uppercase}
.motion-ribbon span::before{content:'✳';color:var(--brand2);font-size:17px}
@keyframes v82-ticker{to{transform:translate3d(-50%,0,0)}}
.motion-ribbon:hover .motion-ribbon-track{animation-play-state:paused}
.hero-art .kinetic-halo{position:absolute;pointer-events:none;width:88%;aspect-ratio:1;max-width:540px;border:1px solid color-mix(in srgb,var(--brand) 20%,transparent);border-radius:50%;z-index:2;transform:rotate(13deg);animation:halo-spin 48s linear infinite}
.hero-art .kinetic-halo::before{content:'';position:absolute;inset:8%;border:1px dashed color-mix(in srgb,var(--brand) 22%,transparent);border-radius:50%}
.hero-art .kinetic-halo::after{content:'';position:absolute;top:6%;left:22%;width:17px;height:17px;border-radius:50%;background:#fff;box-shadow:0 0 0 9px color-mix(in srgb,var(--brand2) 54%,transparent),0 0 35px rgba(255,255,255,.65)}
@keyframes halo-spin{to{transform:rotate(373deg)}}
.kinetic-sheen{position:absolute;z-index:3;width:32%;height:80%;left:28%;top:11%;pointer-events:none;background:linear-gradient(105deg,transparent 23%,rgba(255,255,255,.38) 50%,transparent 77%);transform:translate3d(-120%,0,0) skewX(-14deg);mix-blend-mode:screen;opacity:.42;animation:kinetic-shimmer 11s ease-in-out infinite}
@keyframes kinetic-shimmer{0%,12%,68%,100%{transform:translate3d(-170%,0,0) skewX(-14deg);opacity:0}30%,50%{opacity:.42}56%{transform:translate3d(220%,0,0) skewX(-14deg);opacity:0}}
.about-scene .motion-trace{position:absolute;inset:5%;z-index:2;width:90%;height:90%;pointer-events:none;overflow:visible;fill:none;stroke:color-mix(in srgb,var(--brand) 38%,transparent);stroke-width:1.5;stroke-linecap:round}
.motion-trace path{stroke-dasharray:1100;stroke-dashoffset:1100;transition:stroke-dashoffset 2.2s cubic-bezier(.19,1,.22,1)}
.about-scene.is-drawn .motion-trace path{stroke-dashoffset:0}
.about-scene .motion-dot{position:absolute;z-index:3;right:17%;top:17%;width:7px;height:7px;border-radius:50%;background:var(--brand);box-shadow:0 0 0 12px color-mix(in srgb,var(--brand2) 25%,transparent);animation:dot-breath 4s ease-in-out infinite}
@keyframes dot-breath{50%{transform:scale(1.35);box-shadow:0 0 0 24px color-mix(in srgb,var(--brand2) 6%,transparent)}}
.formula-flow{display:flex;align-items:center;gap:14px;margin:4px 0 33px;color:var(--muted);font:700 10px var(--font-body);text-transform:uppercase;letter-spacing:.15em;opacity:.75;overflow:hidden}
.formula-flow .flow-line{position:relative;height:1px;flex:1;background:var(--line);transform-origin:left;transform:scaleX(.1);transition:transform 1.25s cubic-bezier(.19,1,.22,1)}
.ingredients.is-inview .formula-flow .flow-line{transform:scaleX(1)}
.formula-flow .flow-line::after{content:'';position:absolute;right:0;top:-3px;width:7px;height:7px;border-radius:50%;background:var(--brand)}
/* Chapter navigation: unobtrusive, accessible alternative to endless motion */
.chapter-rail{position:fixed;right:clamp(10px,2vw,32px);top:50%;transform:translateY(-50%) translateX(30px);z-index:42;display:flex;flex-direction:column;gap:13px;opacity:0;pointer-events:none;transition:opacity .4s ease,transform .4s ease}
.chapter-rail.is-visible{opacity:1;pointer-events:auto;transform:translateY(-50%) translateX(0)}
.chapter-rail a{display:flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;border:1px solid color-mix(in srgb,var(--brand) 34%,transparent);background:color-mix(in srgb,var(--cream) 80%,transparent);backdrop-filter:blur(12px);font:700 10px var(--font-body);color:var(--muted);transition:background .28s,transform .28s,color .28s,border-color .28s}
.chapter-rail a:hover,.chapter-rail a.is-active{background:var(--ink);color:white;border-color:var(--ink);transform:scale(1.14)}
/* Fine-pointer 3D effect, almost imperceptible until touched */
@media(hover:hover) and (pointer:fine){.scenario,.ing{transform-style:preserve-3d;transition:transform .28s ease,box-shadow .4s ease}.scenario:hover,.ing:hover{transform:perspective(850px) rotateX(var(--tilt-y,0deg)) rotateY(var(--tilt-x,0deg)) translateY(-3px)}.button{--mag-x:0px;--mag-y:0px;transform:translate3d(var(--mag-x),var(--mag-y),0);will-change:transform}}
.section-heading{position:relative}.section-heading::after{content:'';display:block;width:min(116px,22%);height:3px;margin-top:20px;background:var(--brand);transform-origin:left;transform:scaleX(0);transition:transform 1.1s cubic-bezier(.19,1,.22,1)}
.section.is-inview .section-heading::after,.buy.is-inview .section-heading::after{transform:scaleX(1)}
.section{transition:background-color .65s ease}
.faq-list details{transition:background .4s ease,box-shadow .4s ease}.faq-list details[open]{box-shadow:inset 3px 0 0 var(--brand)}
/* Mobile keeps only lightweight visual movement */
@media(max-width:1099px){.chapter-rail{display:none}.hero-art .kinetic-halo{max-width:370px}.kinetic-sheen{display:none}}
@media(max-width:550px){.motion-ribbon{padding:12px 0;min-height:47px}.motion-ribbon-track{animation-duration:48s;gap:26px}.motion-ribbon span{font-size:10px;gap:26px}.hero-art .kinetic-halo{width:83%;max-width:340px}.hero-art .kinetic-halo::after{width:9px;height:9px;box-shadow:0 0 0 5px color-mix(in srgb,var(--brand2) 45%,transparent)}.formula-flow{font-size:8px}.about-scene .motion-dot{animation:none}}
@media(prefers-reduced-motion:reduce){.motion-ribbon-track,.kinetic-halo,.kinetic-sheen,.motion-dot{animation:none!important}.motion-trace path{stroke-dashoffset:0!important;transition:none!important}.formula-flow .flow-line,.section-heading::after{transform:scaleX(1)!important;transition:none!important}.chapter-rail,.scenario,.ing,.button{transition:none!important;transform:none!important}}
'''
js=r'''
/* v8.2 Kinetic Editorial. Independent of GSAP, respects reduced motion. */
(()=>{
 'use strict';
 const doc=document,root=doc.documentElement;
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const fine=matchMedia('(hover:hover) and (pointer:fine)');
 const large=matchMedia('(min-width: 1100px)');
 const sec=[...doc.querySelectorAll('main > section[id]')].filter(x=>x.id!=='top');
 const rail=doc.querySelector('.chapter-rail');
 const hero=doc.querySelector('.hero');
 const buy=doc.getElementById('buy');
 const links=[...doc.querySelectorAll('.chapter-rail a')];
 const io='IntersectionObserver' in window;
 if(io){
  const draw=new IntersectionObserver((entries)=>{entries.forEach(({target,isIntersecting})=>{if(isIntersecting){target.classList.add('is-drawn');draw.unobserve(target)}})},{threshold:.2});
  doc.querySelectorAll('.about-scene').forEach(el=>draw.observe(el));
  const lines=new IntersectionObserver((entries)=>{entries.forEach(({target,isIntersecting})=>{if(isIntersecting){target.classList.add('is-inview');lines.unobserve(target)}})},{threshold:.08});
  doc.querySelectorAll('.section,.buy').forEach(el=>lines.observe(el));
 }else{doc.querySelectorAll('.about-scene').forEach(el=>el.classList.add('is-drawn'));doc.querySelectorAll('.section,.buy').forEach(el=>el.classList.add('is-inview'))}
 // Section rail: progressive enhancement for precise navigation and scroll orientation.
 let busy=false;
 function updateRail(){busy=false;if(!rail)return;
  const show=large.matches && (hero?.getBoundingClientRect().bottom??0)<110&&(buy?.getBoundingClientRect().top??0)>innerHeight*.36;
  rail.classList.toggle('is-visible',!!show);
  if(!show){links.forEach(a=>{a.classList.remove('is-active');a.removeAttribute('aria-current')});return}
  let active=sec[0]?.id;
  for(const s of sec){if(s.getBoundingClientRect().top<innerHeight*.47)active=s.id}
  links.forEach(a=>{const yes=a.getAttribute('href')==='#'+active;a.classList.toggle('is-active',yes);if(yes)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current')});
 }
 const onScroll=()=>{if(!busy){busy=true;requestAnimationFrame(updateRail)}};
 addEventListener('scroll',onScroll,{passive:true});addEventListener('resize',onScroll,{passive:true});updateRail();
 if(reduced.matches)return;
 // Kinetic affordance on fine-pointer desktops only; no layout-triggering transforms.
 if(fine.matches&&large.matches){
  doc.querySelectorAll('.scenario,.ing').forEach(card=>{
   let frame=0,tx=0,ty=0;
   card.addEventListener('pointermove',e=>{const r=card.getBoundingClientRect();tx=((e.clientX-r.left)/r.width-.5)*4;ty=((e.clientY-r.top)/r.height-.5)*-4;if(!frame)frame=requestAnimationFrame(()=>{frame=0;card.style.setProperty('--tilt-x',tx.toFixed(2)+'deg');card.style.setProperty('--tilt-y',ty.toFixed(2)+'deg')})},{passive:true});
   card.addEventListener('pointerleave',()=>{card.style.setProperty('--tilt-x','0deg');card.style.setProperty('--tilt-y','0deg')})
  });
  doc.querySelectorAll('.hero-copy .button,.buy .button').forEach(button=>{
   let frame=0,x=0,y=0;
   button.addEventListener('pointermove',e=>{const r=button.getBoundingClientRect();x=(e.clientX-r.left-r.width/2)*.075;y=(e.clientY-r.top-r.height/2)*.11;if(!frame)frame=requestAnimationFrame(()=>{frame=0;button.style.setProperty('--mag-x',x.toFixed(1)+'px');button.style.setProperty('--mag-y',y.toFixed(1)+'px')})},{passive:true});
   button.addEventListener('pointerleave',()=>{button.style.setProperty('--mag-x','0px');button.style.setProperty('--mag-y','0px')})
  });
 }
 // GSAP showcase layer: elegant scrubbing on the actual product, no bitmap edits.
 const gsap=window.gsap,ST=window.ScrollTrigger;
 if(gsap&&ST&&large.matches){
  gsap.to('.hero-art .kinetic-halo',{rotation:72,ease:'none',scrollTrigger:{trigger:hero,start:'top top',end:'bottom top',scrub:2}});
  gsap.to('.hero-art .art-product',{y:-25,rotation:1.2,ease:'none',scrollTrigger:{trigger:hero,start:'10% top',end:'bottom top',scrub:1.7}});
  gsap.utils.toArray('.scenario').forEach((el,i)=>{gsap.fromTo(el,{clipPath:'inset(0 0 14% 0 round 1px)'},{clipPath:'inset(0 0 0% 0 round 1px)',duration:.9,scrollTrigger:{trigger:el,start:'top 92%',once:true}})});
 }
})();
'''
nav='<nav class="chapter-rail" aria-label="Быстрый переход по разделам">'+''.join(f'<a href="#{ref}" title="{label}" aria-label="{label}">{i}</a>' for i,(ref,label) in enumerate([('about','О средстве'),('when','Когда пригодится'),('ingredients','Состав'),('how','Применение'),('faq','Вопросы'),('buy','Где купить')],1))+'</nav>'
for name in ('hot-ice','mikozacid'):
 p=root/name/'index.html';s=p.read_text();
 start=s.index('<style>');end=s.index('</style>',start)
 style=s[start+7:end];style=style+'\n'+css
 s=s[:start+7]+style+s[end:]
 # New editorial ribbon after hero, before About. The content is decorative and hidden for SR.
 pattern=r'(</section>\s*)(<!-- Section 2: about the product -->)'
 label=colors[name]
 sep=' • '.join(label.split(' / '))+' • '
 ribbon=f'<div class="motion-ribbon" aria-hidden="true"><div class="motion-ribbon-track"><span>{sep*4}</span><span>{sep*4}</span></div></div>\n'
 s,n=re.subn(pattern,lambda m:m.group(1)+ribbon+m.group(2),s,count=1)
 assert n==1,('ribbon',name)
 # Decor along product packaging in hero, no image edits.
 s=s.replace('<div class="hero-art" aria-label=', '<div class="hero-art" aria-label=',1)
 s=s.replace('<div class="hero-art" aria-label="'+('Фото упаковки Горячий лёд' if name=='hot-ice' else 'Фото упаковки Микозацид')+'">', '<div class="hero-art" aria-label="'+('Фото упаковки Горячий лёд' if name=='hot-ice' else 'Фото упаковки Микозацид')+'"><div class="kinetic-halo" aria-hidden="true"></div><div class="kinetic-sheen" aria-hidden="true"></div>',1)
 # About scene: draw an ornamental curve around product.
 scene='<svg class="motion-trace" viewBox="0 0 500 500" preserveAspectRatio="xMidYMid meet" aria-hidden="true"><path d="M 65 310 C 15 180, 140 40, 270 75 S 515 225, 407 387 S 140 505, 90 380"/></svg><i class="motion-dot" aria-hidden="true"></i>'
 s=s.replace('<span class="scene-point" aria-hidden="true"></span>', '<span class="scene-point" aria-hidden="true"></span>'+scene,1)
 s=s.replace('<div class="ingredients-grid">','<div class="formula-flow" aria-hidden="true"><span>01 / Formula</span><i class="flow-line"></i><span>03 / Ingredients</span></div><div class="ingredients-grid">',1)
 # Note: decorative 01 03 conflict user wants numbering 1,2,3. Change.
 s=s.replace('01 / Formula','Формула').replace('03 / Ingredients','Компоненты')
 s=s.replace('</body>',nav+'\n<script>'+js+'</script>\n</body>',1)
 p.write_text(s)
 (root/name/'source-design.css').write_text(style)
 (root/name/'source-motion.js').write_text((root/name/'source-motion.js').read_text()+'\n'+js)
 print(name,len(s),len(style),s.count('kinetic-halo'),s.count('motion-ribbon'))
# Improve README disclaimer
readme=root/'README_TIMEWEB.md'
readme.write_text(readme.read_text()+'''\n\n## v8.2 — Kinetic Editorial (28.10.2026)\nНовые независимые эффекты: типографическая лента, вращающаяся декоративная орбита, мягкий световой отблеск вокруг сцены, нарисованная при прокрутке SVG-кривая, маркеры разделов, лёгкие магнитные кнопки/перспективные карточки, параллакс подлинной упаковки при доступности GSAP. Все движения отключаются при prefers-reduced-motion. На мобильных сложные GSAP эффекты отключены. Реальные product.png не менялись.\nСодержимое, ссылки, JSON-LD и индексация не менялись. Вариант для согласования, не для открытой индексации.\n''')
# Make ZIP reproducible from directory
out=Path('/mnt/data/zdrava-v8-2-kinetic-editorial-timeweb.zip')
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as z:
 for p in sorted(root.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(root).as_posix())
print('ZIP',out,out.stat().st_size)
# Original packaging exact bytes retained
with zipfile.ZipFile(original) as z:
 for name in colors:
  rel=name+'/assets/product.png'
  assert z.read(rel)==(root/rel).read_bytes()
  print('PACKAGE SAME',name,hashlib.sha256(z.read(rel)).hexdigest()[:16]);
