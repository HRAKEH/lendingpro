from pathlib import Path
from PIL import Image
from io import BytesIO
import re, zipfile, os, json, hashlib

SRC=Path('/mnt/data/ZDRAVA_v8_2_compatible.zip')
ROOT=Path('/mnt/data/zdrava-v83-cinematic-experience')
ROOT.mkdir(exist_ok=True)
with zipfile.ZipFile(SRC) as z:
    assert z.testzip() is None
    z.extractall(ROOT)

STORY={
 'hot-ice':[
  ('ЛЁД • ДВИЖЕНИЕ • УХОД','Сила визуальной прохлады','Прохладная атмосфера, свежий ритм и привычный уход за телом.'),
  ('ПОСЛЕ АКТИВНОГО ДНЯ','Движение продолжается','После прогулки, тренировки и насыщенного дня — время для себя.'),
  ('ПРОСТОЙ РИТУАЛ','Забота в твоём ритме','Туба 50 мл. Наружное применение и комфортный ежедневный уход.')
 ],
 'mikozacid':[
  ('ЧИСТОТА • РИТМ • ЗАБОТА','Пространство свежести','Спокойная графика, естественный свет и ежедневный уход за стопами.'),
  ('ПОСЛЕ БАССЕЙНА И СПОРТА','Время для себя','После бассейна, тренировки и долгого дня в закрытой обуви.'),
  ('ПРОСТОЙ РИТУАЛ','Маленькая привычка','Чистая сухая кожа, два нанесения в день и аккуратный уход.')
 ]
}
STYLE=r'''/* v8.3 — editorial canvas storytelling. This CSS works without external animation libraries. */
/* Correct uneven ingredient paddings: all columns use identical inset and minmax sizing. */
.ingredients-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(12px,1.7vw,24px);border-top:0;margin-bottom:48px;align-items:stretch}
.ingredients-grid .ing,.ingredients-grid .ing:first-child,.ingredients-grid .ing:last-child{box-sizing:border-box;min-width:0;padding:clamp(24px,2.5vw,37px)!important;border:1px solid var(--line)!important;border-radius:23px;background:var(--white);min-height:272px;display:flex;flex-direction:column;align-items:flex-start;justify-content:flex-start;overflow:visible}
.ingredients-grid .ing h3{font:800 clamp(21px,2vw,27px)/1.2 var(--font-title);margin:22px 0 14px;letter-spacing:-.045em;max-width:100%;overflow-wrap:break-word;hyphens:auto}
.ingredients-grid .ing p{font-size:clamp(14px,1.3vw,15px);line-height:1.65;overflow-wrap:break-word}
.ingredients-grid .ing-number{display:flex;align-items:center;justify-content:center;width:35px;height:35px;flex:0 0 35px;border:1px solid var(--line);border-radius:50%;font-weight:700;font-size:12px}
.ingredients-grid .ing::before{border-radius:22px}
@media(max-width:820px){.ingredients-grid{grid-template-columns:1fr!important;gap:13px;margin-bottom:34px}.ingredients-grid .ing,.ingredients-grid .ing:first-child,.ingredients-grid .ing:last-child{min-height:unset;padding:clamp(22px,6vw,30px)!important}.ingredients-grid .ing h3{margin:15px 0 9px;font-size:clamp(22px,6.3vw,28px)}}
/* Unlike stacked reveal effects, this is a scroll-scrubbed narrative scene */
.experience{position:relative;width:100vw;margin-left:calc(50% - 50vw);height:255svh;min-height:1400px;isolation:isolate;--xp:0}
.experience__stage{position:sticky;top:74px;height:calc(100svh - 74px);min-height:590px;overflow:hidden;isolation:isolate;color:#fff;background:#112d42;contain:layout style;}
.experience--botanical .experience__stage{background:#0b342b}
.experience__stage::before{content:'';position:absolute;z-index:0;inset:-10%;background:radial-gradient(circle at 68% 48%,rgba(104,207,244,.32),transparent 35%),radial-gradient(circle at 14% 82%,rgba(21,99,126,.62),transparent 60%),linear-gradient(124deg,#0b233d,#163c55 53%,#081b36);filter:saturate(1.15);transform:scale(calc(1 + var(--xp)*.05));}
.experience--botanical .experience__stage::before{background:radial-gradient(circle at 68% 45%,rgba(148,217,165,.34),transparent 35%),radial-gradient(circle at 10% 79%,rgba(47,120,98,.45),transparent 62%),linear-gradient(125deg,#092c29,#134b3b 57%,#082521)}
.experience__stage::after{content:'';position:absolute;inset:0;z-index:1;pointer-events:none;opacity:.32;background-image:repeating-linear-gradient(90deg,transparent 0,transparent 139px,rgba(255,255,255,.1) 140px,transparent 141px);mask-image:linear-gradient(90deg,transparent,#000 20%,#000 85%,transparent)}
.experience__canvas{position:absolute;inset:0;width:100%;height:100%;z-index:2;pointer-events:none;display:block}
.experience__frame{position:absolute;inset:0;z-index:3;pointer-events:none;border:1px solid rgba(255,255,255,.14)}
.experience__brand{position:absolute;left:clamp(22px,5.1vw,90px);top:clamp(27px,6vh,67px);z-index:7;letter-spacing:.18em;font:700 11px var(--font-body);color:rgba(255,255,255,.66)}
.experience__side{position:absolute;right:clamp(22px,5vw,85px);top:clamp(27px,6vh,67px);z-index:7;font:600 11px var(--font-body);letter-spacing:.12em;color:rgba(255,255,255,.57)}
.experience__copy{position:absolute;z-index:8;left:clamp(24px,7vw,124px);top:50%;width:min(43%,610px);transform:translateY(-50%);pointer-events:none;min-height:290px}
.experience__chapter{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;opacity:0;transform:translate3d(0,36px,0);will-change:opacity,transform;visibility:hidden}
.experience__chapter:first-child{visibility:visible;opacity:1;transform:none} .experience__chapter.is-active{visibility:visible;transform:translate3d(0,0,0)}
.experience__kicker{display:block;font:700 clamp(10px,1vw,12px)/1.6 var(--font-body);letter-spacing:.2em;color:#c0e7f4;margin-bottom:clamp(16px,2.5vw,29px)}
.experience--botanical .experience__kicker{color:#c3e4c8}
.experience__chapter h3{font:800 clamp(46px,6.7vw,116px)/.98 var(--font-title);letter-spacing:-.075em;margin:0 0 26px;max-width:720px;text-wrap:balance}
.experience__chapter p{font-size:clamp(15px,1.3vw,19px);line-height:1.65;max-width:440px;color:rgba(255,255,255,.76);margin:0}
.experience__product{position:absolute;z-index:6;right:clamp(9%,19%,29%);top:51%;height:min(71%,700px);width:auto;max-width:30vw;object-fit:contain;transform:translate3d(50%,-50%,0);filter:drop-shadow(0px 25px 35px rgba(0,0,0,.32));will-change:transform;pointer-events:none}
.experience__halo{position:absolute;z-index:4;right:21%;top:48%;width:min(56vw,680px);aspect-ratio:1;transform:translate(50%,-50%);border-radius:50%;background:radial-gradient(circle,rgba(195,239,255,.16) 0 20%,rgba(182,227,255,.09) 24% 38%,transparent 65%);border:1px solid rgba(255,255,255,.18);box-shadow:0 0 0 28px rgba(255,255,255,.022),0 0 0 100px rgba(255,255,255,.018);pointer-events:none}
.experience__reflection{position:absolute;right:0;bottom:0;width:62%;height:18%;z-index:5;opacity:.4;background:linear-gradient(180deg,rgba(255,255,255,.12),transparent);transform:skew(-22deg);clip-path:polygon(5% 0,100% 0,100% 100%,0 100%);filter:blur(12px)}
.experience__footer{position:absolute;z-index:9;bottom:clamp(25px,5vh,52px);left:clamp(24px,7vw,124px);right:clamp(24px,7vw,124px);display:flex;align-items:center;gap:16px;pointer-events:none}
.experience__step{font:700 13px var(--font-title);letter-spacing:.05em;min-width:45px}
.experience__progress{position:relative;flex:1;max-width:280px;height:2px;background:rgba(255,255,255,.25);overflow:hidden}
.experience__progress i{display:block;width:100%;height:100%;background:#d0f5fc;transform:scaleX(0);transform-origin:left;will-change:transform}
.experience__hint{margin-left:auto;font:700 10px var(--font-body);letter-spacing:.15em;color:rgba(255,255,255,.7)}
.experience__fallback{display:none}
@media(max-width:1050px){.experience__chapter h3{font-size:clamp(40px,7vw,75px)}.experience__copy{left:6vw;width:49%}.experience__product{right:21%;max-width:33vw;height:65%}.experience__halo{right:20%}}
@media(max-width:700px){.experience{height:auto;min-height:unset;margin-left:calc(50% - 50vw)}.experience__stage{position:relative;top:auto;height:640px;min-height:0}.experience__stage::before{inset:0}.experience__copy{left:24px;top:80px;transform:none;width:calc(100% - 48px);height:auto;min-height:175px}.experience__chapter{justify-content:flex-start;top:0;bottom:auto}.experience__chapter h3{font-size:clamp(38px,10.3vw,64px);max-width:320px;margin-bottom:12px;letter-spacing:-.065em}.experience__chapter p{font-size:13px;max-width:300px;line-height:1.5}.experience__kicker{font-size:9px;margin-bottom:12px}.experience__product{top:69%;right:50%;height:44%;max-width:60vw}.experience__halo{top:70%;right:50%;width:min(94vw,420px)}.experience__brand{left:24px;top:24px;font-size:9px}.experience__side{right:24px;top:24px;font-size:9px}.experience__footer{bottom:20px;left:24px;right:24px}.experience__hint{display:none}.experience__reflection{display:none}.experience__stage::after{opacity:.1}}
@media(max-width:400px){.experience__stage{height:620px}.experience__product{height:43%}.experience__chapter h3{font-size:38px}.experience__copy{top:78px}.experience__chapter p{max-width:265px}}
@media(prefers-reduced-motion:reduce){.experience{height:auto;min-height:0}.experience__stage{position:relative;top:0;height:min(90svh,780px)}.experience__chapter{display:none!important;transform:none!important;opacity:1!important;visibility:visible!important}.experience__chapter:first-child{display:flex!important}.experience__canvas{display:none}.experience__progress i{transform:scaleX(1)}.experience__product{will-change:auto}.experience__stage::before{transform:none}}
'''
SCRIPT=r'''/* Product Story Engine 1.0: timeline is driven by actual scroll progress, not time. No external libraries. */
(() => {
  'use strict';
  const sections=[...document.querySelectorAll('[data-product-story]')];
  if (!sections.length) return;
  const reduce=matchMedia('(prefers-reduced-motion: reduce)');
  const small=matchMedia('(max-width: 700px)');
  const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
  function engine(section){
    const canvas=section.querySelector('canvas');
    const ctx=canvas.getContext('2d',{alpha:true});
    if (!ctx) return;
    const product=section.querySelector('.experience__product');
    const chapters=[...section.querySelectorAll('.experience__chapter')];
    const bar=section.querySelector('.experience__progress i');
    const count=section.querySelector('.experience__step');
    const leaf=section.dataset.productStory==='botanical';
    let w=0,h=0,dpr=1,current=0,target=0,ticking=false,visible=false,destroyed=false;
    const seeded=(i)=>{let n=Math.sin(i*127.1+leaf*67.3)*43758.5453;return n-Math.floor(n)};
    const shapes=Array.from({length:leaf?26:34},(_,i)=>({seed:seeded(i+2),az:seeded(i+120)*Math.PI*2,r:.15+seeded(i+200)*.56,s:7+seeded(i+500)*38,depth:.5+seeded(i+800)*.8}));
    function resize(){const r=canvas.getBoundingClientRect();w=Math.max(1,r.width);h=Math.max(1,r.height);dpr=Math.min(devicePixelRatio||1,1.6);canvas.width=Math.round(w*dpr);canvas.height=Math.round(h*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);draw(current)}
    function diamond(x,y,s,alpha,rotation){ctx.save();ctx.translate(x,y);ctx.rotate(rotation);ctx.strokeStyle='rgba(199,244,255,'+alpha+')';ctx.fillStyle='rgba(161,226,248,'+(alpha*.21)+')';ctx.lineWidth=1.3;ctx.beginPath();ctx.moveTo(0,-s*1.7);ctx.lineTo(s*.72,-s*.23);ctx.lineTo(s*.6,s*.95);ctx.lineTo(0,s*1.5);ctx.lineTo(-s*.75,s*.37);ctx.closePath();ctx.fill();ctx.stroke();ctx.strokeStyle='rgba(255,255,255,'+(alpha*.6)+')';ctx.beginPath();ctx.moveTo(0,-s*1.7);ctx.lineTo(0,s*1.5);ctx.moveTo(-s*.75,s*.37);ctx.lineTo(s*.72,-s*.23);ctx.stroke();ctx.restore()}
    function drawLeaf(x,y,s,alpha,rot){ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.beginPath();ctx.moveTo(0,s*.9);ctx.bezierCurveTo(-s*.9,-s*.1,-s*.75,-s*.8,0,-s*1.5);ctx.bezierCurveTo(s*.78,-s*.8,s*.86,-s*.1,0,s*.9);ctx.fillStyle='rgba(174,231,174,'+(alpha*.5)+')';ctx.strokeStyle='rgba(213,254,224,'+alpha+')';ctx.lineWidth=1.2;ctx.fill();ctx.stroke();ctx.beginPath();ctx.moveTo(0,s*.9);ctx.quadraticCurveTo(s*.2,-s*.3,0,-s*1.5);ctx.strokeStyle='rgba(226,255,238,'+(alpha*.65)+')';ctx.stroke();ctx.restore()}
    function draw(p){if(!w||!h||small.matches||reduce.matches){ctx.clearRect(0,0,w,h);return}
      ctx.clearRect(0,0,w,h);
      const cx=w*.73,cy=h*.49,base=Math.min(w,h)*.42;
      // Scroll-driven refraction: the same progress animates rings, particles, and the typography.
      for(let ring=0;ring<4;ring++){
        const radius=base*(.45+ring*.27)+p*(ring%2?55:-34);
        ctx.beginPath();ctx.ellipse(cx,cy,radius,radius*(.8+.03*ring),p*.55,0,Math.PI*2);
        ctx.lineWidth=.75+ring*.19;
        ctx.strokeStyle=leaf?'rgba(178,243,197,'+(.16-ring*.025)+')':'rgba(185,236,255,'+(.17-ring*.026)+')';ctx.stroke();
      }
      shapes.forEach((a,i)=>{
        const move=p*Math.PI*(leaf?1.1:1.95),az=a.az+move*(i%2?1:-1),radius=base*(a.r+p*.12),x=cx+Math.cos(az)*radius*1.12,y=cy+Math.sin(az)*radius*.87;
        const s=a.s*(.68+(1+p)*a.depth*.22),alpha=.13+.27*(1-Math.abs(p-.45))*a.depth;
        if(leaf)drawLeaf(x,y,s,alpha,az+p*2.1);else diamond(x,y,s,alpha,az+p*1.2);
      });
      // Optical highlight crossing the foreground at the second chapter.
      const phase=Math.sin((p-.17)*Math.PI*1.4);ctx.save();ctx.globalAlpha=Math.max(0,phase)*.17;ctx.translate(cx,cy);ctx.rotate(-.2+p*.6);const g=ctx.createLinearGradient(-base*.5,0,base*.5,0);g.addColorStop(0,'rgba(255,255,255,0)');g.addColorStop(.5,'rgba(245,255,255,.87)');g.addColorStop(1,'rgba(255,255,255,0)');ctx.fillStyle=g;ctx.fillRect(-base*.5,-h,base,2*h);ctx.restore();
    }
    function render(p){
      section.style.setProperty('--xp',p.toFixed(4));
      if(!small.matches&&!reduce.matches){product.style.transform='translate3d(50%,calc(-50% + '+((p-.5)*-35).toFixed(1)+'px),0) rotate('+((p-.5)*-5).toFixed(2)+'deg) scale('+(1+p*.09).toFixed(4)+')';}
      else{product.style.transform='translate3d(50%,-50%,0)'}
      const phase=p*2;
      const first=Math.min(1,Math.floor(phase));
      const fraction=clamp(phase-first);
      const blend=fraction*fraction*(3-2*fraction);
      const active=p<.25?0:p<.75?1:2;
      chapters.forEach((el,i)=>{
        let alpha=(i===first?1-blend:0)+(i===first+1?blend:0);
        if(small.matches||reduce.matches)alpha=i===0?1:0;
        el.style.opacity=alpha.toFixed(3);
        el.style.visibility=alpha>.025?'visible':'hidden';
        el.style.transform='translate3d(0,'+((1-alpha)*25).toFixed(1)+'px,0)';
        el.classList.toggle('is-active',i===active);
      });
      bar.style.transform='scaleX('+p.toFixed(4)+')';count.textContent=(active+1)+' / 3';
      draw(p);
    }
    function scrollPosition(){if(small.matches||reduce.matches)return 0;const r=section.getBoundingClientRect();const total=Math.max(1,r.height-innerHeight);return clamp(-r.top/total)}
    function tick(){ticking=false;if(destroyed)return;const delta=target-current;if(Math.abs(delta)>.0005){current+=delta*.2;render(current);request()}else{current=target;render(current)}}
    function request(){if(!ticking){ticking=true;requestAnimationFrame(tick)}}
    function scroll(){if(!visible)return;target=scrollPosition();request()}
    const observer=new IntersectionObserver(([entry])=>{visible=entry.isIntersecting;if(visible){target=scrollPosition();request()}},{rootMargin:'250px 0px 250px 0px'});
    observer.observe(section);
    const resizeObserver=new ResizeObserver(()=>{resize();target=scrollPosition();request()});resizeObserver.observe(canvas);
    addEventListener('scroll',scroll,{passive:true});addEventListener('resize',()=>{target=scrollPosition();request()},{passive:true});
    // All content remains available as original sections; story is decorative narrative.
    reduce.addEventListener?.('change',()=>{target=scrollPosition();request()});small.addEventListener?.('change',()=>{resize();target=scrollPosition();request()});
    resize();render(0);
  }
  sections.forEach(engine);
})();'''

for name,chapters in STORY.items():
    path=ROOT/name/'index.html'
    html=path.read_text(encoding='utf-8')
    style=html[html.index('<style>')+7:html.index('</style>')]
    assert '.ingredients-grid' in style
    html=html.replace('</style>',STYLE+'\n</style>',1)
    story_type='botanical' if name=='mikozacid' else 'glacier'
    heading='СВЕЖЕСТЬ В ДВИЖЕНИИ' if name=='hot-ice' else 'СПОКОЙНЫЙ РИТМ УХОДА'
    imgname='Горячий лёд' if name=='hot-ice' else 'Микозацид'
    dimensions=('349','855') if name=='hot-ice' else ('468','734')
    chapter_html='\n'.join(f'<div class="experience__chapter{" is-active" if i==0 else ""}"><span class="experience__kicker">{kicker}</span><h3>{title}</h3><p>{detail}</p></div>' for i,(kicker,title,detail) in enumerate(chapters))
    scene=f'''\n<div class="experience experience--{story_type}" data-product-story="{story_type}" aria-label="Анимированная предметная сцена — {imgname}">
<div class="experience__stage">
<canvas class="experience__canvas" aria-hidden="true"></canvas>
<div class="experience__halo" aria-hidden="true"></div><div class="experience__reflection" aria-hidden="true"></div><div class="experience__frame" aria-hidden="true"></div>
<span class="experience__brand">ЗДРАВА / ДИЗАЙН УХОДА</span><span class="experience__side">{heading}</span>
<div class="experience__copy" aria-live="off">{chapter_html}</div>
<img class="experience__product" src="assets/product.png" width="{dimensions[0]}" height="{dimensions[1]}" loading="lazy" decoding="async" alt="Оригинальная упаковка {imgname}, 50 мл">
<div class="experience__footer"><span class="experience__step" aria-hidden="true">1 / 3</span><span class="experience__progress" aria-hidden="true"><i></i></span><span class="experience__hint">ЛИСТАЙТЕ — СЦЕНА ОЖИВАЕТ</span></div>
</div></div>\n'''
    # append within about section, not reorder its numbered sections.
    anchor='</div></div></section>\n<!-- Section 3:'
    if anchor not in html:
        # tolerate whitespace
        m=re.search(r'</div></div></section>\s*<!-- Section 3:',html)
        if not m:raise ValueError('about closing not found '+name)
        html=html[:m.start()]+'</div></div>'+scene+'</section>'+html[m.end()-len('<!-- Section 3:'):]
    else:
        html=html.replace(anchor,'</div></div>'+scene+'</section>\n<!-- Section 3:',1)
    # Script should run AFTER existing GSAP code, also works with blocked CDN.
    html=html.replace('</body>','<script>\n'+SCRIPT+'\n</script>\n</body>',1)
    assert html.count('data-product-story=')==1
    path.write_text(html,encoding='utf-8')
    (ROOT/name/'source-design.css').write_text(style+'\n'+STYLE,encoding='utf-8')
    (ROOT/name/'source-motion.js').write_text((ROOT/name/'source-motion.js').read_text(encoding='utf-8')+'\n'+SCRIPT,encoding='utf-8')
    assert (ROOT/name/'assets/product.png').read_bytes()==zipfile.ZipFile(SRC).read(name+'/assets/product.png')

(ROOT/'README_TIMEWEB.md').write_text('''# ЗДРАВА v8.3 — Cinematic Product Story

Два отдельных статических лендинга «Горячий лёд» и «Микозацид». В каждом index.html содержит CSS и JS, файлы source-design.css / source-motion.js — редактируемые копии, не требуются для запуска.

## Что исправлено
- Ошибка отступов в секции «Состав»: все три карточки имеют одинаковые внутренние поля, нормальный перенос длинных заголовков и границы, в мобильном режиме — одна колонка.
- Новая действительно scroll-driven сцена в разделе «О средстве»: оригинальная туба и рисуемые Canvas 2D ледяные кристаллы (Горячий лёд) / ботанические листья (Микозацид). На 3 этапах прокрутки меняются тексты, движение частиц, свет и прогресс.
- Скорость сцены зависит ТОЛЬКО от scroll progress, не от таймера; для мобильных и reduced-motion сцена статична. Без внешних библиотек сцена и контент видны.
- Ссылки Ozon/Wildberries, 2 шрифта Onest + Golos Text, исходный состав, FAQ, SEO и оригинальные изображения упаковки не менялись.

## Размещение
Содержимое папок hot-ice/ и mikozacid/ распаковать в ПОДТВЕРЖДЁННЫЙ корень сайта рядом с существующим index.html. Главный сайт ЗДРАВА не заменять. robots.txt/sitemap.xml — шаблоны для согласования, не перезаписывать действующие корневые файлы. На страницах по-прежнему noindex,nofollow. До рекламы подтвердить домен, этикетки, составы и юридические тексты, подключить Метрику. Тестировать на настоящем URL и в Lighthouse; статический QA не равен производственному тесту.

## Проверка
Открытие на ширинах 360/390/768/1440, изображения, нативные FAQ и меню, доступность текста без CDN, JS ошибки, canvas и динамика сцены; reduced-motion. Код не требует сборки.
''',encoding='utf-8')

# Standard ZIP STORED, ascii paths only, avoids mobile extractor issues
outfile=Path('/mnt/data/ZDRAVA_v8_3_CINEMATIC_FIXED.zip')
with zipfile.ZipFile(outfile,'w',compression=zipfile.ZIP_STORED,allowZip64=False) as z:
  for p in sorted(ROOT.rglob('*')):
    if p.is_file():z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(outfile) as z: assert z.testzip() is None
print('CREATED',outfile,outfile.stat().st_size, 'files',len(zipfile.ZipFile(outfile).namelist()))
