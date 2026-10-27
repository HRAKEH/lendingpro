from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
import numpy as np, shutil, random, zipfile, re
base=Path('/mnt/data/lendingpro-atmosphere-v6');out=Path('/mnt/data/lendingpro-cinematic-v7')
if out.exists():shutil.rmtree(out)
shutil.copytree(base,out)
# tiny texture with truly transparent low-alpha noise, never touches packaging
rng=np.random.default_rng(1229)
small=(rng.random((256,256))*255).astype('uint8')
tex=np.zeros((256,256,4),dtype='uint8')
tex[:,:,:3]=np.where(small[:,:,None]>127,255,10)
tex[:,:,3]=np.where(small>127,6,4)
Image.fromarray(tex,'RGBA').save(out/'hot-ice/assets/texture.png',optimize=True)
shutil.copy2(out/'hot-ice/assets/texture.png',out/'mikozacid/assets/texture.png')

common_css=r'''/* Motion system / original composition / October 2026. Reduced-motion first. */
:root{--motion-ease:cubic-bezier(.22,1,.36,1);--motion-dur:780ms}
html { scroll-padding-top: 100px; }
/* Makes navigation readable after scroll without altering the established palette. */
.site-header { position:sticky; top:0; z-index:80; transition:background-color .3s,box-shadow .3s; }
.site-header.is-scrolled{background:color-mix(in srgb,var(--bg) 86%,transparent);box-shadow:0 9px 30px color-mix(in srgb,var(--ink) 7%,transparent);backdrop-filter:blur(19px) saturate(1.25);-webkit-backdrop-filter:blur(19px) saturate(1.25)}
.scroll-track{position:fixed;z-index:120;top:0;left:0;right:0;height:3px;pointer-events:none}
.scroll-track__progress{display:block;width:100%;height:100%;background:var(--accent);transform:scaleX(var(--scroll-progress,0));transform-origin:left center;will-change:transform;}
/* Hero copy slides out from a typographic mask: not a stock letter-by-letter effect. */
.hero h1 .motion-line{display:block;overflow:hidden;line-height:1.15;padding-bottom:.055em;margin-bottom:-.055em}
.hero h1 .motion-line__inner{display:block;animation:motion-title 950ms var(--motion-ease) both;animation-delay:var(--line-delay,70ms)}
@keyframes motion-title{from{transform:translate3d(0,102%,0);opacity:.65}to{transform:translate3d(0,0,0);opacity:1}}
.hero h1.entrance{animation:none}
.hero-copy .eyebrow,.hero-copy .hero-intro,.hero-copy .market-actions,.hero-copy .hero-footnote{animation-duration:820ms}
/* Light follows the cursor in stage, but the image pixels and orientation NEVER change. */
.photo-stage{--light-x:50%;--light-y:40%;--sculpt-x:0px;--sculpt-y:0px;transform:translateZ(0)}
.motion-light{position:absolute;inset:0;z-index:1;pointer-events:none;background:radial-gradient(circle 240px at var(--light-x) var(--light-y),rgba(255,255,255,.48),transparent 76%);opacity:.75;transition:opacity .35s}
.atmosphere-sculpt{transform:translate3d(var(--sculpt-x),var(--sculpt-y),0);transition:transform .55s var(--motion-ease)}
.photo-stage::before{animation:stage-pulse 11s ease-in-out infinite alternate}
@keyframes stage-pulse{from{opacity:.46}to{opacity:.87}}
.photo-stage .product-photo{z-index:4;backface-visibility:hidden}
.glass-float{z-index:8;transition:transform 560ms var(--motion-ease);transform:translate3d(var(--float-x,0px),var(--float-y,0px),0)}
/* Buttons use subtle light travel and restrained magnetism, without scaling the product. */
.btn{position:relative;overflow:hidden;isolation:isolate;transform:translate3d(var(--btn-x,0px),var(--btn-y,0px),0);transition:transform .32s var(--motion-ease),box-shadow .28s ease,background-color .25s ease,color .25s ease}
.btn:hover{transform:translate3d(var(--btn-x,0px),calc(var(--btn-y,0px) - 2px),0)}
.btn:active{transform:translate3d(0,1px,0) scale(.985)}
.btn::after{content:"";position:absolute;inset:-100% -100%;pointer-events:none;z-index:-1;opacity:0;background:linear-gradient(110deg,transparent 40%,rgba(255,255,255,.18) 50%,transparent 60%);transform:translateX(-20%);transition:transform .55s var(--motion-ease),opacity .3s}
.btn:hover::after{opacity:1;transform:translateX(25%)}
/* Scroll-triggered section reveals: useful hierarchy, not perpetual bouncing. */
[data-animate].is-visible{animation:motion-section .82s var(--motion-ease) both!important}
@keyframes motion-section{from{opacity:0;filter:blur(4px);transform:translate3d(0,24px,0)}to{opacity:1;filter:blur(0);transform:translate3d(0,0,0)}}
.occasion-grid [data-animate]:nth-child(2).is-visible,.ingredients-grid [data-animate]:nth-child(2).is-visible{animation-delay:.075s!important}
.occasion-grid [data-animate]:nth-child(3).is-visible,.ingredients-grid [data-animate]:nth-child(3).is-visible{animation-delay:.15s!important}
/* Ingredient spotlight follows cursor; transparent layer instead of glossy templated cards. */
.ingredient{position:relative;isolation:isolate;--spot-x:50%;--spot-y:0;transition:transform .45s var(--motion-ease),border-color .45s}
.ingredient::before{content:"";pointer-events:none;position:absolute;z-index:-1;inset:-16px -12px -8px;border-radius:12px;background:radial-gradient(circle 180px at var(--spot-x) var(--spot-y),color-mix(in srgb,var(--soft) 38%,transparent),transparent 90%);opacity:0;transition:opacity .34s}
.ingredient:hover::before{opacity:1}
.ingredient:hover{transform:translateY(-3px);border-color:var(--accent)}
/* The interlude is a second quiet visual crescendo halfway down the page. */
.motion-interlude{position:relative;padding:clamp(30px,5vw,80px) 0;background:var(--bg);overflow:hidden}
.motion-interlude__frame{position:relative;isolation:isolate;overflow:hidden;min-height:540px;border-radius:24px;display:grid;grid-template-columns:minmax(0,1fr) minmax(230px,.75fr);align-items:center;gap:2vw;background:var(--interlude-bg);color:var(--ink);box-shadow:0 24px 60px color-mix(in srgb,var(--ink) 10%,transparent);border:1px solid rgba(255,255,255,.62)}
.motion-interlude__frame::after{content:"";position:absolute;inset:0;pointer-events:none;z-index:6;opacity:.54;background-image:url('assets/texture.png');background-size:256px 256px}
.motion-interlude__copy{z-index:5;position:relative;padding:clamp(32px,6vw,91px) 0 clamp(32px,6vw,91px) clamp(28px,6vw,92px)}
.motion-interlude__copy .section-label{color:var(--accent)}
.motion-interlude h2{font:800 clamp(43px,5vw,72px)/1.09 var(--font-title);letter-spacing:-.065em;margin:25px 0;max-width:570px}
.motion-interlude p{max-width:450px;font:400 clamp(16px,1.4vw,19px)/1.65 var(--font-text);opacity:.82;margin:0 0 23px}
.motion-interlude .simple-link{color:var(--accent)}
.motion-interlude__art{position:relative;z-index:2;height:100%;min-height:540px;display:flex;align-items:center;justify-content:center}
.motion-interlude__art::before{content:"";position:absolute;inset:12% 6%;border-radius:50% 50% 42% 42%;border:1px solid rgba(255,255,255,.7);box-shadow:inset 0 0 48px rgba(255,255,255,.48),0 0 0 26px rgba(255,255,255,.08);transform:translateY(var(--interlude-parallax,0px));transition:transform .13s linear}
.motion-interlude__art::after{content:"";position:absolute;z-index:-1;width:440px;height:440px;max-width:96%;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.72),transparent 70%);filter:blur(13px)}
.motion-interlude__product{position:relative;z-index:3;max-height:470px;max-width:75%;width:auto;height:auto;object-fit:contain;filter:drop-shadow(0 26px 25px rgba(22,52,74,.19));transform:translateY(var(--interlude-img-y,0px));transition:transform .13s linear;will-change:transform}
.motion-interlude__micro{position:absolute;z-index:5;right:6%;bottom:33px;color:var(--accent);font:600 12px var(--font-text);letter-spacing:.04em}
/* Subtle editorial motion for disclosure, no custom JS accordion takeover. */
.faq-list details[open] p,.full-composition[open] .composition-body{animation:motion-answer .28s ease-out both}
@keyframes motion-answer{from{opacity:.6;transform:translateY(-4px)}to{opacity:1;transform:translateY(0)}}
/* Show mobile Buy dock once hero is outside viewport, hide at the purchase section. */
.mobile-buy-dock{display:none}
@media(max-width:1000px){.motion-interlude__frame{min-height:470px}.motion-interlude__art{min-height:470px}.motion-interlude__product{max-height:390px}}
@media(max-width:800px){
.motion-interlude{padding:32px 0}.motion-interlude__frame{grid-template-columns:1fr;gap:0;min-height:unset;border-radius:18px}
.motion-interlude__copy{padding:45px 28px 10px}.motion-interlude h2{font-size:clamp(41px,8vw,60px)}
.motion-interlude__art{min-height:350px;height:350px}.motion-interlude__product{max-height:320px;max-width:60%}
.motion-interlude__micro{bottom:18px}
.mobile-buy-dock{display:flex;align-items:center;gap:9px;position:fixed;z-index:81;bottom:calc(12px + env(safe-area-inset-bottom,0px));left:50%;width:min(440px,calc(100% - 24px));padding:8px;border:1px solid color-mix(in srgb,var(--accent) 20%,rgba(255,255,255,.8));border-radius:15px;background:color-mix(in srgb,var(--bg) 88%,transparent);-webkit-backdrop-filter:blur(22px);backdrop-filter:blur(22px);box-shadow:0 8px 29px rgba(12,32,48,.16);opacity:0;pointer-events:none;transform:translate3d(-50%,20px,0);transition:opacity .33s var(--motion-ease),transform .33s var(--motion-ease)}
.mobile-buy-dock.is-active{opacity:1;pointer-events:auto;transform:translate3d(-50%,0,0)}
.mobile-buy-dock a{flex:1;display:flex;justify-content:space-between;align-items:center;min-width:0;padding:12px 13px;border-radius:9px;background:var(--accent);font:700 14px/1.2 var(--font-text);color:#fff}
.mobile-buy-dock a+a{color:var(--accent);background:rgba(255,255,255,.78);border:1px solid color-mix(in srgb,var(--accent) 35%,transparent)}
body{padding-bottom:0}
}
@media(max-width:600px){
.motion-interlude__frame{border-radius:16px}.motion-interlude__copy{padding:38px 23px 0}.motion-interlude h2{font-size:clamp(37px,10.5vw,53px)}
.motion-interlude__art{min-height:340px;height:340px}.motion-interlude__product{max-height:313px;max-width:75%}
.glass-float{bottom:14px}.site-header .head-inner{height:74px}
}
@media(max-width:360px){.motion-interlude__product{max-height:295px}}
/* Accessibility: stable render if motion preferences are reduced. */
@media(prefers-reduced-motion:reduce){
.scroll-track,.motion-light{display:none!important}
.hero h1 .motion-line__inner,[data-animate].is-visible,.photo-stage::before{animation:none!important;filter:none!important;opacity:1!important;transform:none!important}
.atmosphere-sculpt,.glass-float,.motion-interlude__art::before,.motion-interlude__product,.ingredient,.btn,.btn::after{transform:none!important;transition:none!important}
.mobile-buy-dock{transition:none!important}
}
'''
# note: correct the source description where it calls hot-ice a cream; packaging explicitly says gel
specs={
'mikozacid':dict(section_label='УХОД В ТВОЁМ РИТМЕ',title='Свежесть начинается с заботы.',desc='Для ухода за кожей стоп и ногтями — дома, после тренировки или бассейна.',art='Микозацид',micro='УХОД ЗА КОЖЕЙ И НОГТЯМИ',media='#d0e6d8',media2='#e3f1e7'),
'hot-ice':dict(section_label='КОМФОРТ ПОСЛЕ НАГРУЗКИ',title='Когда хочется лёгкости.',desc='Наружный уход и массаж после активного дня — без лишних обещаний.',art='Горячий лёд',micro='ГЕЛЬ ДЛЯ ТЕЛА · 50 МЛ',media='#c0dff3',media2='#e6f5fe'),
}
for name,s in specs.items():
 folder=out/name
 soup=BeautifulSoup((folder/'index.html').read_text(encoding='utf8'),'html.parser')
 head=soup.find('head')
 # keep existing CSS order and append motion last
 style=soup.new_tag('link',rel='stylesheet',href='motion.css');head.append(style)
 progress=soup.new_tag('div',attrs={'class':'scroll-track','aria-hidden':'true'});progress.append(soup.new_tag('span',attrs={'class':'scroll-track__progress'}));soup.body.insert(0,progress)
 stage=soup.select_one('.photo-stage')
 light=soup.new_tag('span',attrs={'class':'motion-light','aria-hidden':'true'});prod=stage.select_one('.product-photo');prod.insert_before(light)
 # wrap already hard-coded line break into masked lines; no user-visible text changes
 h1=soup.select_one('#hero-title')
 def wrap_line(children,delay):
  outer=soup.new_tag('span',attrs={'class':'motion-line'})
  inner=soup.new_tag('span',attrs={'class':'motion-line__inner','style':f'--line-delay:{delay}ms'})
  for c in children:inner.append(c)
  outer.append(inner)
  return outer
 contents=list(h1.contents);groups=[[]]
 for child in contents:
  if getattr(child,'name',None)=='br':groups.append([])
  else:groups[-1].append(child.extract())
 h1.clear()
 for i,children in enumerate(groups):h1.append(wrap_line(children,90+i*135))
 # chapter composition halfway through site
 chapter=soup.new_tag('section',attrs={'class':'motion-interlude','aria-labelledby':'chapter-heading'})
 wrap=soup.new_tag('div',attrs={'class':'wrap'})
 frame=soup.new_tag('div',attrs={'class':'motion-interlude__frame','data-motion-chapter':'','style':f'--interlude-bg:linear-gradient(116deg,{s["media2"]}, {s["media"]})'})
 c=soup.new_tag('div',attrs={'class':'motion-interlude__copy','data-animate':''})
 label=soup.new_tag('span',attrs={'class':'section-label'});label.string=s['section_label']
 hh=soup.new_tag('h2',id='chapter-heading');hh.string=s['title']
 para=soup.new_tag('p');para.string=s['desc']
 link=soup.new_tag('a',attrs={'class':'simple-link','href':'#usage'});link.string='Как применять ↗'
 for n in [label,hh,para,link]:c.append(n)
 art=soup.new_tag('div',attrs={'class':'motion-interlude__art','aria-hidden':'true'})
 image=soup.new_tag('img',attrs={'class':'motion-interlude__product','src':'assets/product.png','loading':'lazy','decoding':'async','alt':'','width':'349','height':'855'})
 art.append(image)
 micro=soup.new_tag('span',attrs={'class':'motion-interlude__micro'});micro.string=s['micro'];art.append(micro)
 frame.append(c);frame.append(art);wrap.append(frame);chapter.append(wrap)
 target=soup.select_one('.ingredients-section');target.insert_before(chapter)
 # mobile dock with real URLs from the hero
 dock=soup.new_tag('div',attrs={'class':'mobile-buy-dock','aria-label':'Выбрать маркетплейс'})
 for klass,txt in [('btn-primary','Ozon ↗'),('btn-alt','Wildberries ↗')]:
  source=soup.select_one('.market-actions .'+klass)
  a=soup.new_tag('a',href=source['href'],target='_blank',rel='noopener noreferrer')
  a.string=txt;dock.append(a)
 soup.body.append(dock)
 # preserve existing script and add motion script after it, defer
 script=soup.new_tag('script',src='motion.js',defer=True);soup.body.append(script)
 # meta and title preserve
 (folder/'index.html').write_text(str(soup),encoding='utf8')
 (folder/'motion.css').write_text(common_css,encoding='utf8')
 js=r'''"use strict";
/* LandingPro v7: respectful motion, native JS, no third-party animation libraries.
   Images retain their original pixels and aspect ratio. */
(() => {
 const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
 const fine = window.matchMedia('(hover: hover) and (pointer: fine)');
 const root = document.documentElement;
 const header = document.querySelector('.site-header');
 const stage = document.querySelector('.photo-stage');
 const glass = stage?.querySelector('.glass-float');
 const interlude = document.querySelector('.motion-interlude__frame');
 const hero = document.querySelector('.hero');
 const buy = document.querySelector('.purchase-section');
 const dock = document.querySelector('.mobile-buy-dock');
 const clamp=(v,min,max)=>Math.min(max,Math.max(min,v));
 let scheduled=false;
 function onScroll(){
  scheduled=false;
  const doc=document.documentElement;
  const range=Math.max(1, doc.scrollHeight-innerHeight);
  root.style.setProperty('--scroll-progress',(scrollY/range).toFixed(4));
  header?.classList.toggle('is-scrolled',scrollY>25);
  if (dock){
   const heroOut=hero?.getBoundingClientRect().bottom<25;
   const buyRect=buy?.getBoundingClientRect();
   const buyShown=!!buyRect && buyRect.top<innerHeight && buyRect.bottom>0;
   dock.classList.toggle('is-active',Boolean(heroOut && !buyShown && innerWidth<=800));
  }
  if(!reduce.matches&&interlude){
   const b=interlude.getBoundingClientRect();
   if(b.top<innerHeight+70&&b.bottom>-70){
    const progress=clamp((innerHeight-b.top)/(innerHeight+b.height),0,1);
    interlude.style.setProperty('--interlude-img-y',`${((progress-.5)*-29).toFixed(2)}px`);
    interlude.style.setProperty('--interlude-parallax',`${((progress-.5)*16).toFixed(2)}px`);
   }
  }
 }
 function scrollTick(){if(!scheduled){scheduled=true;requestAnimationFrame(onScroll)}}
 addEventListener('scroll',scrollTick,{passive:true});addEventListener('resize',scrollTick,{passive:true});scrollTick();
 function enablePointer(){
  if(!fine.matches||reduce.matches||!stage)return;
  const move=e=>{
   const b=stage.getBoundingClientRect(),nx=clamp((e.clientX-b.left)/b.width,0,1),ny=clamp((e.clientY-b.top)/b.height,0,1);
   stage.style.setProperty('--light-x',(nx*100).toFixed(1)+'%');stage.style.setProperty('--light-y',(ny*100).toFixed(1)+'%');
   stage.style.setProperty('--sculpt-x',((nx-.5)*13).toFixed(2)+'px');stage.style.setProperty('--sculpt-y',((ny-.5)*9).toFixed(2)+'px');
   if(glass){glass.style.setProperty('--float-x',((nx-.5)*-5).toFixed(2)+'px');glass.style.setProperty('--float-y',((ny-.5)*-5).toFixed(2)+'px')}
  };
  stage.addEventListener('pointermove',move,{passive:true});
  stage.addEventListener('pointerleave',()=>{
   stage.style.setProperty('--light-x','50%');stage.style.setProperty('--light-y','40%');
   stage.style.setProperty('--sculpt-x','0px');stage.style.setProperty('--sculpt-y','0px');
   if(glass){glass.style.setProperty('--float-x','0px');glass.style.setProperty('--float-y','0px')}
  },{passive:true});
  for (const btn of document.querySelectorAll('.market-actions .btn,.purchase-links .btn')) {
   btn.addEventListener('pointermove',e=>{
    const b=btn.getBoundingClientRect(),x=(e.clientX-b.left)/b.width-.5,y=(e.clientY-b.top)/b.height-.5;
    btn.style.setProperty('--btn-x',(x*4).toFixed(2)+'px');btn.style.setProperty('--btn-y',(y*3).toFixed(2)+'px');
   },{passive:true});
   btn.addEventListener('pointerleave',()=>{btn.style.setProperty('--btn-x','0px');btn.style.setProperty('--btn-y','0px')},{passive:true});
  }
  for(const box of document.querySelectorAll('.ingredient')){
   box.addEventListener('pointermove',e=>{
    const b=box.getBoundingClientRect();box.style.setProperty('--spot-x',((e.clientX-b.left)/b.width*100).toFixed(1)+'%');box.style.setProperty('--spot-y',(e.clientY-b.top).toFixed(1)+'px');
   },{passive:true});
  }
 }
 enablePointer();
 reduce.addEventListener?.('change',()=>{
  if(reduce.matches){for(const p of [stage,interlude,glass]){p?.style.removeProperty('--sculpt-x');p?.style.removeProperty('--sculpt-y');p?.style.removeProperty('--interlude-img-y');p?.style.removeProperty('--float-x');p?.style.removeProperty('--float-y')}}
 });
})();
'''
 (folder/'motion.js').write_text(js,encoding='utf8')
 # sanity exact photo original
 assert (folder/'assets/product.png').read_bytes()==(base/name/'assets/product.png').read_bytes()
 assert len(soup.select('.hero h1 .motion-line'))==2
 assert len(soup.select('.mobile-buy-dock a'))==2
 assert len(soup.select('.market-actions a'))==2
 assert len(soup.select('.purchase-links a'))==2
print('Wrote',out)
readme='''LendingPro — версия v7 / cinematic motion\n\nТехнический архив для предпросмотра на Timeweb, без сборки.\n\nРАЗМЕЩЕНИЕ: извлеките две папки mikozacid и hot-ice рядом с существующим index.html в ПОДТВЕРЖДЁННОМ корне целевого домена. НИКОГДА НЕ заменяйте главный index.html сайта ЗДРАВА.\n\nВ каждой папке index.html, styles.css, editorial.css, atmosphere.css, motion.css, script.js, motion.js и assets.\n\nФото упаковок взяты из материалов пользователя и сохранены побайтово по сравнению с v6. На фото и этикетках ничего не изменялось. Визуальные эффекты — только CSS/JS-слои ВОКРУГ них.\n\nАнимации: masked title, lighting/parallax of decorative backdrop, scroll reveal, spotlight on ingredient sections, CTA hover, scroll progress, mobile marketplace dock, mid-page editorial scene. Учитывается prefers-reduced-motion.\n\nНа страницах meta robots noindex,nofollow. НЕ запускать рекламу/индексацию до документальной проверки текстов, этикеток, составов, лицензий изображений и корректности карточек маркетплейсов.\n\nШрифты Onest/Golos Text грузятся Google Fonts. Для работы независимо от них надо отдельно разместить лицензированные webfonts локально.\n'''
(out/'README_TIMEWEB.txt').write_text(readme,encoding='utf8')
zipfile_path=Path('/mnt/data/lendingpro-timeweb-v7-cinematic-motion.zip')
with zipfile.ZipFile(zipfile_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(out.rglob('*')):
  if f.is_file():z.write(f,f.relative_to(out))
print('Zip',zipfile_path,zipfile_path.stat().st_size)
