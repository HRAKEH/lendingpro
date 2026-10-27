from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import zipfile, io, re, json, html, hashlib, textwrap, shutil

ROOT=Path('/mnt/data/zdrava-v8-rebuild');ROOT.mkdir(exist_ok=True)
V7=Path('/mnt/data/lendingpro-timeweb-v7-cinematic-motion.zip')
SPECS={
 'mikozacid':{
  'name':'Микозацид','pageTitle':'Микозацид — уход за стопами и ногтями | ЗДРАВА',
  'descSEO':'Микозацид — средство для ухода за стопами и ногтями, 50 мл. Состав, применение, особенности. Купить на Ozon и Wildberries.',
  'label':'МИКОЗАЦИД · ЕЖЕДНЕВНЫЙ УХОД ЗА СТОПАМИ','hero1':'Чувство','hero2':'свежести.','hero3':'Каждый день.',
  'hero_desc':'Уход за кожей стоп и ногтями после бассейна, тренировки или долгого дня в закрытой обуви.',
  'aboutTitle':'Уход, к которому хочется возвращаться.','aboutText':'«Микозацид» — средство для наружного ухода за кожей стоп и ногтями. По описанию товара, текстура быстро впитывается и не оставляет жирной плёнки.',
  'scenarios':[('После бассейна','Поддержать привычный уход после бассейна, сауны и общих душевых.'),('После активности','Вернуть ощущение свежести после тренировки и долгой прогулки.'),('На каждый день','Включить уход за стопами в повседневную гигиену, особенно при закрытой обуви.')],
  'ingredientGroups':[('Растительные экстракты','Чистотел, подорожник, календула, шалфей, эвкалипт и другие растения.'),('Натуральные масла','Амарант, виноградная косточка и оливковое масло.'),('Эфирные масла','Чайное дерево, имбирь и кедр.')],
  'fullComp':'Вода очищенная; растительные экстракты: чистотела, подорожника, конского каштана, шалфея, календулы, тысячелистника, мелиссы, ромашки, шиповника, боярышника, эвкалипта, пихты, лопуха; воск пчелиный; масла амаранта, виноградной косточки, оливковое; эфирные масла чайного дерева, имбиря, кедра; цетеариловый спирт, изопропилпальмитат, цетеарет-20, воск эмульсионный, феноксиэтанол, этилгексилглицерин.',
  'steps':[('Подготовить','Перед применением очистите и высушите кожу стоп. При необходимости аккуратно подготовьте ногтевые пластины.'),('Нанести','Наносите средство на чистую сухую кожу ног два раза в день.'),('Повторять курс','Рекомендуемый курс — 21 день. При необходимости применение можно повторить.')],
  'day':'21 день','use':'2 раза в день','aboutKicker':'НАТУРАЛЬНЫЙ РИТМ УХОДА',
  'qa':[('Для чего подходит «Микозацид»?','Для повседневного ухода за кожей стоп и ногтями, например после спорта, бассейна или дня в закрытой обуви.'),('Как использовать средство?','Наносите на чистую сухую кожу ног дважды в день. По описанию товара рекомендуемый курс — 21 день; сверьтесь с инструкцией на упаковке.'),('Поможет ли при грибковой инфекции?','Средство не является лекарственным препаратом. При зуде, шелушении или изменении ногтей обратитесь к врачу для диагностики и лечения.'),('Что делать при раздражении?','Не используйте средство при индивидуальной непереносимости компонентов. Если появилась нежелательная реакция, прекратите применение.')],
  'ozon':'https://www.ozon.ru/product/sredstvo-dlya-uhoda-za-kozhey-i-nogtyami-mikozatsid-3690496505/',
  'wb':'https://www.wildberries.ru/catalog/909408717/detail.aspx',
  'photo':'mikozacid/assets/product.png','srcWidth':468,'srcHeight':734,'stepFlag':'21','accentLabel':'МЯГКИЙ КОНТРАСТ','style':'verdant'
 },
 'hot-ice':{
  'name':'Горячий лёд','pageTitle':'Горячий лёд — гель для тела | ЗДРАВА',
  'descSEO':'Горячий лёд — гель для ухода за телом после активного дня, 50 мл. Состав, применение, особенности. Купить на Ozon и Wildberries.',
  'label':'ГОРЯЧИЙ ЛЁД · ГЕЛЬ ДЛЯ ТЕЛА','hero1':'Прохлада.','hero2':'Движение.','hero3':'Твой ритм.',
  'hero_desc':'Ощущение свежести после тренировок, прогулок и насыщенных дней — в компактной тубе 50 мл.',
  'aboutTitle':'Лёгкость в каждом движении.','aboutText':'«Горячий лёд» — наружный гель для ухода за телом и локального массажа. По описанию товара, он легко распределяется, быстро впитывается и не оставляет липкости.',
  'scenarios':[('После тренировки','Уход за телом после привычной физической активности и занятий спортом.'),('После долгого дня','Когда много ходили, стояли на ногах или активно двигались.'),('Во время массажа','Для массажа коленей, спины, плеч, рук и ног.')],
  'ingredientGroups':[('Растительные экстракты','Ромашка, гвоздика, вербена, бузина, подорожник и тысячелистник.'),('Освежающие компоненты','Ментол, камфора и эфирные масла эвкалипта и гвоздики.'),('Уход за кожей','Д-пантенол, аллантоин и другие компоненты формулы.')],
  'fullComp':'Вода очищенная; растительные экстракты: ромашки, гвоздики, вербены, бузины, подорожника, тысячелистника; ментол; эфирное масло эвкалипта; эфирное масло гвоздики; д-пантенол; масло вазелиновое; цетеариловый спирт; воск эмульсионный; камфора; аллантоин; моностеарат глицерина; цетеарет-20; глицерин; изопропилпальмитат; ПЭГ-40 масло касторовое гидрогенизированное; полисорбат-20; триэтаноламин; феноксиэтанол; этилгексилглицерин.',
  'steps':[('Нанести','Небольшое количество средства нанесите на кожу.'),('Распределить','Равномерно распределите до полного впитывания.'),('Повторять курс','По описанию товара — два раза в день курсом 30 дней. При необходимости повторить через месяц.')],
  'day':'30 дней','use':'2 раза в день','aboutKicker':'ПРИВЫЧНЫЙ УХОД ПОСЛЕ НАГРУЗОК',
  'qa':[('Для чего подходит «Горячий лёд»?','Для наружного ухода за телом и локального массажа после тренировок, прогулок и других повседневных нагрузок.'),('Как часто можно наносить?','По описанию товара — два раза в день, курс 30 дней. При необходимости курс можно повторить через месяц. Сверьтесь с упаковкой.'),('Можно ли использовать при болях в суставах?','Средство не является лекарственным препаратом и не заменяет диагностику и лечение. При боли или выраженных симптомах обратитесь к врачу.'),('Как хранить средство?','В недоступном для детей месте, не выше 25 °C, вдали от прямых солнечных лучей и отопительных приборов.')],
  'ozon':'https://www.ozon.ru/product/sredstvo-dlya-sustavov-goryachiy-led-tuba-50-ml-4342397494/',
  'wb':'https://www.wildberries.ru/catalog/1123489882/detail.aspx',
  'photo':'hot-ice/assets/product.png','srcWidth':349,'srcHeight':855,'stepFlag':'30','accentLabel':'ЛЕДЯНОЙ КОНТРАСТ','style':'glacier'
 }
}
# Real product art, unchanged pixels, from archived v7.
with zipfile.ZipFile(V7) as z:
 for slug,s in SPECS.items():
  folder=ROOT/slug/'assets';folder.mkdir(parents=True,exist_ok=True)
  content=z.read(f'{slug}/assets/product.png')
  (folder/'product.png').write_bytes(content)
  img=Image.open(io.BytesIO(content)).convert('RGBA')
  assert img.size==(s['srcWidth'],s['srcHeight'])
  # Transparent source must not be modified in any way: use original PNG in website.

# og images are brand design compositions with preserved source pack PNG (alpha composite; labels accurate)
fonts_candidates=['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
for slug,s in SPECS.items():
 bg='#f3f8f5' if slug=='mikozacid' else '#edf8fd';ink='#1c342b' if slug=='mikozacid' else '#102e49';accent='#2a8062' if slug=='mikozacid' else '#236aa5'
 im=Image.new('RGB',(1200,630),bg);d=ImageDraw.Draw(im)
 for r in range(470,90,-14):
  box=(870-r//2,315-r//2,870+r//2,315+r//2)
  # subtle concentric rings
  d.ellipse(box,outline=('#d6e8e1' if slug=='mikozacid' else '#d3e9f5'),width=2)
 f1=ImageFont.truetype(fonts_candidates[1],66);f2=ImageFont.truetype(fonts_candidates[1],26);f3=ImageFont.truetype(fonts_candidates[0],29)
 d.text((65,65),'ЗДРАВА',fill=accent,font=f2)
 d.text((65,205),s['name'],fill=ink,font=f1)
 sub='Уход за кожей стоп и ногтями' if slug=='mikozacid' else 'Гель для тела после активного дня'
 d.text((66,309),sub,fill=ink,font=f3)
 d.rounded_rectangle((65,443,400,505),radius=30,fill=accent)
 d.text((98,459),'Ozon  ·  Wildberries',font=ImageFont.truetype(fonts_candidates[0],22),fill='white')
 tube=Image.open(ROOT/slug/'assets'/'product.png').convert('RGBA')
 tube.thumbnail((360,515),Image.Resampling.LANCZOS)
 im.paste(tube,(875-tube.width//2,55+(515-tube.height)//2),tube)
 im.save(ROOT/slug/'assets'/'og-image.jpg',quality=90,optimize=True)

css=r'''/* Single-file, mobile-first CSS: responsive and motion-aware. */
:root{--cream:#f7faf7;--ink:#18352c;--muted:#577269;--brand:#237958;--brand2:#b7dfc9;--line:#cfdfd5;--surface:#e9f2eb;--hero:#e5efe9;--white:#fff;--font-title:'Onest',sans-serif;--font-body:'Golos Text',sans-serif}
body.glacier{--cream:#f5faff;--ink:#112c47;--muted:#53748b;--brand:#2869a4;--brand2:#c1e5f5;--line:#cfdfec;--surface:#e8f3fa;--hero:#e8f5fc;--white:#fff}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:84px}body{margin:0;background:var(--cream);color:var(--ink);font-family:var(--font-body);font-size:16px;-webkit-font-smoothing:antialiased;overflow-x:clip}button,a{-webkit-tap-highlight-color:transparent}button{font:inherit;cursor:pointer}a{color:inherit;text-decoration:none}img{display:block;max-width:100%;height:auto}::selection{background:var(--brand2);color:var(--ink)}
.skip{position:absolute;z-index:100;top:-80px;left:14px;background:var(--ink);color:#fff;padding:12px 18px}.skip:focus{top:12px}
.wrap{width:min(1300px,calc(100% - 56px));margin:auto}.site-header{position:sticky;top:0;z-index:60;background:color-mix(in srgb,var(--cream) 89%,transparent);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);border-bottom:1px solid color-mix(in srgb,var(--line) 65%,transparent)}.header-inner{min-height:84px;display:flex;align-items:center;justify-content:space-between;gap:24px}.logo{font:800 22px/1 var(--font-title);letter-spacing:-.065em;display:inline-flex;gap:11px;align-items:center}.logo-mark{display:inline-block;width:18px;height:18px;border:3px solid var(--brand);border-radius:2px 70% 2px 70%;transform:rotate(-45deg)}.nav{display:flex;gap:34px;align-items:center}.nav a{font-size:13px;color:var(--muted);transition:color .2s}.nav a:hover{color:var(--brand)}.nav a{min-height:44px;display:inline-flex;align-items:center}.header-action{font-size:13px;font-weight:700;border-bottom:1px solid var(--brand);padding:9px 0}.menu-trigger{display:none;background:transparent;border:1px solid var(--line);border-radius:50%;height:46px;width:46px;color:var(--ink);font-size:22px;align-items:center;justify-content:center}
.progress{position:fixed;top:0;left:0;width:100%;height:3px;z-index:101;pointer-events:none}.progress span{display:block;height:100%;width:100%;background:var(--brand);transform:scaleX(0);transform-origin:left;will-change:transform}
.hero{position:relative;isolation:isolate;min-height:min(845px,calc(100svh - 84px));background:var(--hero);overflow:hidden}.hero::before{content:'';position:absolute;pointer-events:none;inset:0;background:radial-gradient(ellipse 55% 77% at 91% 52%,color-mix(in srgb,var(--brand2) 56%,transparent),transparent 75%),linear-gradient(115deg,rgba(255,255,255,.32),transparent 55%)}.hero-layout{display:grid;grid-template-columns:1.08fr .92fr;min-height:735px;align-items:center;gap:5vw;padding-top:65px;padding-bottom:90px;position:relative}.hero-copy{position:relative;z-index:5;max-width:740px}.eyebrow{display:flex;align-items:center;gap:15px;color:var(--brand);font-size:11px;letter-spacing:.18em;font-weight:700;text-transform:uppercase}.eyebrow:before{content:'';width:31px;height:1px;background:var(--brand)}.display{font-family:var(--font-title);font-weight:800;letter-spacing:-.075em;font-size:clamp(57px,6.65vw,111px);line-height:.99;margin:35px 0 28px}.display .line{display:block;white-space:nowrap}.display .line.accent{color:var(--brand)}.subtitle{color:var(--muted);font-size:clamp(17px,1.55vw,21px);line-height:1.65;max-width:515px;margin:0 0 35px}.actions{display:flex;flex-wrap:wrap;gap:12px;align-items:center}.button{--button-bg:var(--ink);--button-fg:#fff;min-height:55px;display:inline-flex;align-items:center;justify-content:center;gap:20px;background:var(--button-bg);color:var(--button-fg);border:1px solid transparent;border-radius:3px;padding:17px 24px;font-size:14px;font-weight:700;position:relative;overflow:hidden;transition:transform .2s ease,box-shadow .2s ease,background .2s ease}.button.primary{--button-bg:var(--brand)}.button.secondary{--button-bg:transparent;--button-fg:var(--ink);border-color:var(--ink)}.button:hover{transform:translateY(-2px);box-shadow:0 13px 25px -19px var(--ink)}.button:active{transform:translateY(0) scale(.985)}.button .arrow{display:inline-block;transition:transform .2s}.button:hover .arrow{transform:translate(3px,-2px)}.button:focus-visible,.menu-trigger:focus-visible,a:focus-visible,summary:focus-visible{outline:3px solid var(--brand);outline-offset:4px}.hero-note{display:flex;gap:22px;align-items:center;margin-top:37px;font-size:12px;letter-spacing:.03em;color:var(--muted)}.hero-note span+span{border-left:1px solid var(--line);padding-left:21px}
.hero-art{position:relative;z-index:2;min-height:620px;display:flex;align-items:center;justify-content:center;--px:0;--py:0}.art-ring{position:absolute;width:575px;height:575px;max-width:125%;aspect-ratio:1;border:1px solid color-mix(in srgb,var(--brand) 19%,transparent);border-radius:50%;transform:translate(calc(var(--px)*-10px),calc(var(--py)*-7px));transition:transform .35s ease}.art-ring::before,.art-ring::after{content:'';position:absolute;border-radius:50%;inset:38px;border:1px solid color-mix(in srgb,var(--brand) 12%,transparent)}.art-ring::after{inset:105px}.art-plate{position:absolute;width:77%;height:67%;border-radius:46% 54% 58% 42%/49% 47% 53% 51%;background:linear-gradient(145deg,rgba(255,255,255,.7),color-mix(in srgb,var(--brand2) 75%,#fff));box-shadow:inset 17px 15px 42px rgba(255,255,255,.78),30px 24px 70px color-mix(in srgb,var(--brand) 12%,transparent);transform:rotate(-12deg);filter:blur(.3px)}.glacier .art-plate{border-radius:32% 56% 35% 49%;transform:rotate(18deg);clip-path:polygon(16% 0%,84% 5%,100% 70%,65% 100%,5% 83%,0 28%)}.art-light{position:absolute;width:58%;aspect-ratio:1;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.77),transparent 70%);filter:blur(13px);transform:translate(17%,3%)}.art-product{position:relative;z-index:4;width:auto;height:min(560px,55vw);object-fit:contain;filter:drop-shadow(13px 28px 20px rgba(11,34,35,.18));transform:translate(calc(var(--px)*5px),calc(var(--py)*3px));transition:transform .45s cubic-bezier(.2,.7,.1,1)}.art-small{position:absolute;bottom:52px;right:0;z-index:5;background:rgba(255,255,255,.5);border:1px solid rgba(255,255,255,.75);backdrop-filter:blur(14px);padding:19px 23px;min-width:168px;box-shadow:0 14px 32px -28px var(--ink)}.art-small strong{display:block;font:800 38px/1 var(--font-title);letter-spacing:-.07em}.art-small span{font-size:11px;color:var(--muted);letter-spacing:.11em;text-transform:uppercase}.art-number{font:800 clamp(170px,24vw,410px)/1 var(--font-title);letter-spacing:-.11em;color:color-mix(in srgb,var(--brand) 7%,transparent);position:absolute;z-index:-1;right:-5%;top:0;pointer-events:none}.hero-index{position:absolute;bottom:31px;left:calc((100% - min(1300px,100% - 56px))/2);z-index:2;color:var(--brand);font-size:11px;letter-spacing:.18em;display:flex;align-items:center;gap:13px}.hero-index:after{content:'';width:55px;height:1px;background:var(--brand)}
.section{padding:112px 0}.kicker{color:var(--brand);font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:700}.section-heading{font:800 clamp(43px,5vw,76px)/1.08 var(--font-title);letter-spacing:-.069em;margin:24px 0 30px}.section-lead{font-size:18px;line-height:1.75;color:var(--muted);max-width:570px}.section-top{display:grid;grid-template-columns:1fr .9fr;gap:7vw;align-items:end;margin-bottom:55px}.about{background:var(--cream)}.about-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}.about-scene{min-height:520px;background:var(--surface);position:relative;overflow:hidden;isolation:isolate;display:flex;align-items:center;justify-content:center}.about-scene:before{content:'';position:absolute;width:82%;aspect-ratio:1;border:1px solid var(--line);border-radius:50%}.about-scene:after{content:'';position:absolute;width:56%;aspect-ratio:1;background:rgba(255,255,255,.45);border-radius:49% 51% 39% 61%}.about-scene img{position:relative;z-index:2;height:390px;max-width:80%;object-fit:contain;filter:drop-shadow(13px 20px 14px rgba(5,31,31,.13))}.about-textbox{padding:clamp(30px,5vw,73px);background:var(--ink);color:#fff;display:flex;flex-direction:column;justify-content:space-between;gap:65px;min-height:520px}.about-textbox p{color:rgba(255,255,255,.74);font-size:18px;line-height:1.72;max-width:460px}.about-textbox strong{font:800 clamp(30px,4vw,57px)/1.12 var(--font-title);letter-spacing:-.056em}.smallnote{font-size:12px!important;letter-spacing:.11em;text-transform:uppercase}
.scenarios{background:var(--surface)}.scenario-grid{display:grid;grid-template-columns:1.12fr .9fr .9fr;gap:18px}.scenario{border:1px solid color-mix(in srgb,var(--line) 70%,#fff);background:color-mix(in srgb,var(--cream) 78%,transparent);padding:38px 31px 39px;min-height:310px;display:flex;flex-direction:column;justify-content:space-between;transition:background .2s,transform .25s}.scenario:hover{transform:translateY(-5px);background:var(--white)}.scenario:first-child{background:var(--ink);color:#fff}.scenario:first-child .s-n,.scenario:first-child p{color:rgba(255,255,255,.7)}.s-n{font-size:14px;color:var(--brand);font-weight:700}.scenario h3{font:800 clamp(25px,2.6vw,37px)/1.12 var(--font-title);letter-spacing:-.05em;margin:0 0 15px}.scenario p{margin:0;line-height:1.65;font-size:14px;color:var(--muted)}
.ingredients .section-top{margin-bottom:50px}.ingredients-grid{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--line);margin-bottom:48px}.ing{padding:34px 35px 50px;border-right:1px solid var(--line);min-height:233px}.ing:first-child{padding-left:0}.ing:last-child{border-right:0}.ing-number{color:var(--brand);font-size:12px}.ing h3{font:800 26px/1.22 var(--font-title);letter-spacing:-.04em;margin:28px 0 15px}.ing p{color:var(--muted);line-height:1.65;font-size:15px}.expand{border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:0}.expand summary{display:flex;justify-content:space-between;align-items:center;cursor:pointer;list-style:none;gap:25px;padding:25px 4px;font-size:17px;font-weight:700}.expand summary::-webkit-details-marker{display:none}.expand summary:after{content:'+';font-size:24px;font-weight:400;color:var(--brand)}.expand[open] summary:after{content:'−'}.expand .inner{padding:0 4px 30px;max-width:970px;color:var(--muted);line-height:1.8;font-size:15px}
.how{background:var(--ink);color:white;overflow:hidden}.how .kicker{color:var(--brand2)}.how .section-lead{color:rgba(255,255,255,.64)}.how-content{display:grid;grid-template-columns:1fr 1fr;gap:10vw}.steps{list-style:none;margin:10px 0 0;padding:0}.steps li{display:grid;grid-template-columns:58px 1fr;gap:15px;padding:24px 0;border-bottom:1px solid rgba(255,255,255,.18)}.steps li:first-child{border-top:1px solid rgba(255,255,255,.18)}.steps .n{color:var(--brand2);font:700 19px var(--font-title)}.steps h3{font:800 24px/1.15 var(--font-title);margin:0 0 11px;letter-spacing:-.045em}.steps p{font-size:15px;line-height:1.7;color:rgba(255,255,255,.66);margin:0}.how-accent{font:800 clamp(100px,17vw,250px)/.82 var(--font-title);color:var(--brand2);letter-spacing:-.1em}.how-unit{font:700 17px var(--font-body);letter-spacing:.06em;margin-top:26px;text-transform:uppercase}.how-accent-wrap{display:flex;flex-direction:column;justify-content:center;border:1px solid rgba(255,255,255,.19);padding:40px;min-height:360px}
.faq{background:var(--cream)}.faq-grid{display:grid;grid-template-columns:.68fr 1.32fr;gap:10vw}.faq .section-heading{margin-top:17px}.faq-list{border-top:1px solid var(--line)}.faq-list details{border-bottom:1px solid var(--line)}.faq-list summary{list-style:none;display:flex;align-items:center;justify-content:space-between;gap:30px;padding:26px 0;cursor:pointer;font-weight:700;font-size:18px}.faq-list summary::-webkit-details-marker{display:none}.faq-list summary:after{content:'+';font-size:24px;flex-shrink:0;font-weight:400;color:var(--brand)}.faq-list details[open] summary:after{content:'−'}.faq-list p{margin:0;padding:0 0 27px;line-height:1.75;color:var(--muted);max-width:660px}
.buy{background:var(--hero);padding:125px 0 105px;position:relative;overflow:hidden}.buy:before{content:'';position:absolute;width:650px;aspect-ratio:1;border:1px solid var(--line);border-radius:50%;left:-230px;bottom:-480px}.buy-inner{position:relative;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:30px}.buy .section-heading{max-width:820px;margin-bottom:35px}.buy-remark{color:var(--muted);font-size:12px;margin-top:18px}.footer{padding:45px 0 35px;background:var(--ink);color:rgba(255,255,255,.7)}.footer-inner{display:grid;grid-template-columns:1fr 1.4fr auto;gap:50px}.footer .logo{color:white}.footer p{font-size:12px;line-height:1.8;max-width:650px;margin:0}.up{text-decoration:underline;text-underline-offset:4px;color:white;font-size:13px}.copyright{margin-top:55px;border-top:1px solid rgba(255,255,255,.15);padding-top:20px;font-size:11px}
.mobile-dock{display:none}
@media(max-width:1150px){.wrap{width:min(100% - 48px,1300px)}.display{font-size:clamp(56px,7vw,90px)}.hero-layout{gap:15px}.hero-art{min-height:500px}.art-product{height:min(510px,51vw)}.art-ring{width:450px;height:450px}.section{padding:88px 0}}
@media(max-width:820px){.header-inner{min-height:70px}.nav{position:absolute;top:70px;left:0;right:0;padding:25px 28px;background:var(--cream);border-bottom:1px solid var(--line);display:none;flex-direction:column;align-items:stretch;gap:20px}.nav.is-open{display:flex}.menu-trigger{display:inline-flex}.header-action{margin-left:auto}.hero-layout{grid-template-columns:1fr;gap:10px;min-height:0;padding:74px 0 85px}.hero-copy{z-index:4}.hero-art{min-height:500px;grid-row:2}.hero-note{margin-top:26px}.art-product{height:450px}.art-plate{max-height:340px}.art-small{right:1%;bottom:0}.display{font-size:clamp(55px,11vw,89px)}.section-top,.faq-grid,.how-content{grid-template-columns:1fr;gap:20px}.about-grid{grid-template-columns:1fr}.about-scene,.about-textbox{min-height:420px}.scenario-grid{grid-template-columns:1fr 1fr}.scenario:first-child{grid-column:1/-1;min-height:260px}.ingredients-grid{grid-template-columns:1fr}.ing,.ing:first-child{padding:25px 0;min-height:unset;border-right:0;border-bottom:1px solid var(--line)}.ing:last-child{border-bottom:0}.how-accent-wrap{min-height:270px}.footer-inner{grid-template-columns:1fr 1fr}.footer .up{grid-column:2;justify-self:end}}
@media(max-width:550px){.wrap{width:calc(100% - 36px)}.header-action{display:none}.hero-layout{padding-top:63px;padding-bottom:68px}.eyebrow{font-size:10px;letter-spacing:.11em}.display{font-size:clamp(48px,13.6vw,70px);margin:28px 0 20px}.display .line{white-space:normal}.subtitle{font-size:16px;line-height:1.55;max-width:355px;margin-bottom:25px}.actions{display:grid;grid-template-columns:1fr 1fr;gap:8px}.button{min-height:52px;gap:9px;font-size:12px;padding:13px 9px}.hero-art{min-height:440px;margin-top:0}.art-plate{height:79%;width:88%}.art-ring{width:min(370px,108vw);height:min(370px,108vw)}.art-product{height:385px;max-width:70vw}.art-small{min-width:120px;padding:13px 16px;bottom:0;right:0}.art-small strong{font-size:32px}.hero-note{font-size:11px;gap:16px}.hero-note span+span{padding-left:15px}.hero-index{display:none}.section{padding:72px 0}.section-heading{font-size:clamp(41px,11.5vw,59px);margin:16px 0 24px}.section-lead{font-size:16px}.section-top{margin-bottom:29px}.about-scene{min-height:330px}.about-scene img{height:275px}.about-textbox{min-height:370px;padding:31px}.about-textbox strong{font-size:39px}.about-textbox p{font-size:16px}.scenario-grid{grid-template-columns:1fr}.scenario:first-child{grid-column:auto}.scenario{min-height:245px;padding:27px}.scenario h3{font-size:31px}.ing h3{margin:15px 0 10px}.how-accent-wrap{padding:30px;min-height:235px}.how-accent{font-size:120px}.faq-list summary{font-size:16px}.buy{padding:88px 0 96px}.buy .actions{width:100%}.footer-inner{grid-template-columns:1fr;gap:22px}.footer .up{grid-column:auto;justify-self:start}.footer{padding-bottom:95px}.mobile-dock{display:flex;position:fixed;z-index:55;bottom:0;left:0;right:0;gap:8px;padding:9px 13px calc(9px + env(safe-area-inset-bottom));border-top:1px solid var(--line);background:color-mix(in srgb,var(--cream) 95%,transparent);backdrop-filter:blur(18px);transform:translateY(120%);transition:transform .24s ease}.mobile-dock.is-visible{transform:translateY(0)}.mobile-dock a{flex:1;min-height:44px;display:flex;justify-content:center;align-items:center;background:var(--brand);color:white;font-weight:700;font-size:13px}.mobile-dock a:last-child{background:var(--ink)}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{scroll-behavior:auto!important;animation:none!important;transition:none!important;transform:none!important}.progress{display:none}.mobile-dock{transform:translateY(120%)!important}.mobile-dock.is-visible{transform:translateY(0)!important}}
'''
js=r'''/* Progressive enhancement: content, links, and details remain usable without JS. */
(()=>{
 const doc=document;
 const reduce=window.matchMedia('(prefers-reduced-motion: reduce)');
 const mobile=window.matchMedia('(max-width: 550px)');
 const nav=doc.getElementById('nav');const trigger=doc.getElementById('menu-trigger');
 if(trigger&&nav){trigger.addEventListener('click',()=>{const open=nav.classList.toggle('is-open');trigger.setAttribute('aria-expanded',String(open));trigger.setAttribute('aria-label',open?'Закрыть меню':'Открыть меню')});nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('is-open');trigger.setAttribute('aria-expanded','false')}));}
 const progress=doc.querySelector('.progress span');const dock=doc.querySelector('.mobile-dock');const hero=doc.querySelector('.hero');const buy=doc.getElementById('buy');
 const update=()=>{const total=doc.documentElement.scrollHeight-innerHeight;if(progress){progress.style.transform='scaleX('+(total?Math.min(1,scrollY/total):0)+')';}if(dock){const h=hero?hero.getBoundingClientRect():{bottom:400};const b=buy?buy.getBoundingClientRect():{top:10000};dock.classList.toggle('is-visible',mobile.matches&&h.bottom<130&&b.top>innerHeight*.5);}};
 window.addEventListener('scroll',update,{passive:true});window.addEventListener('resize',update,{passive:true});update();
 // Data attributes allow Yandex.Metrika and GA4 hooks after counters are configured.
 function track(name){try{window.dataLayer?.push({event:'zdrava_'+name});if(window.ZDRAVA_METRIKA_ID&&typeof window.ym==='function')window.ym(window.ZDRAVA_METRIKA_ID,'reachGoal',name);}catch(e){}}
 doc.addEventListener('click',e=>{const a=e.target.closest('[data-event]');if(a)track(a.dataset.event);});
 const target=doc.getElementById('buy');if(target&&'IntersectionObserver'in window){const o=new IntersectionObserver(es=>{if(es.some(e=>e.isIntersecting)){track('buy_section');o.disconnect()}},{threshold:.35});o.observe(target)}
 // Smooth scroll + entrance motion only on capable devices; native scroll works without CDNs.
 if(reduce.matches)return;
 if(!mobile.matches&&typeof window.Lenis==='function'){
  try{const lenis=new window.Lenis({duration:1.12,smoothWheel:true,touchMultiplier:1.1});if(window.gsap&&window.ScrollTrigger){lenis.on('scroll',window.ScrollTrigger.update);window.gsap.ticker.add(t=>lenis.raf(t*1000));window.gsap.ticker.lagSmoothing(0);}else{const raf=t=>{lenis.raf(t);requestAnimationFrame(raf)};requestAnimationFrame(raf)}}catch(e){}
 }
 const gsap=window.gsap,st=window.ScrollTrigger;
 if(gsap&&st){
  gsap.registerPlugin(st);
  gsap.from('.display .line',{y:45,autoAlpha:0,duration:.9,ease:'power3.out',stagger:.13,clearProps:'all'});
  gsap.from('.hero-copy .subtitle,.hero-copy .actions,.hero-note',{y:20,autoAlpha:0,duration:.8,ease:'power2.out',stagger:.13,delay:.36,clearProps:'all'});
  gsap.from('.art-product',{y:45,autoAlpha:0,scale:.94,duration:1.15,ease:'power3.out',clearProps:'all'});
  // Accurate numeric facts animate only once on desktop; HTML values remain correct without JS.
  if(!mobile.matches)doc.querySelectorAll('.counter').forEach(el=>{const actual=Number(el.dataset.value);const state={v:0};if(!Number.isFinite(actual))return;gsap.to(state,{v:actual,duration:.85,ease:'power1.out',scrollTrigger:el.closest('.how')?{trigger:el.closest('.how'),start:'top 78%',once:true}:undefined,onUpdate:()=>{el.textContent=String(Math.round(state.v))},onComplete:()=>{el.textContent=String(actual)}})});

  doc.querySelectorAll('.section .kicker,.section .section-heading,.section .section-lead,.scenario,.ing,.steps li').forEach((el,i)=>{gsap.from(el,{scrollTrigger:{trigger:el,start:'top 90%',once:true},y:24,autoAlpha:0,duration:.7,ease:'power2.out',clearProps:'all'})});
 }else if('IntersectionObserver'in window){
  const obs=new IntersectionObserver(es=>{es.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('is-in');obs.unobserve(entry.target)}})},{threshold:.08});
  doc.querySelectorAll('.scenario,.ing,.steps li').forEach(el=>{el.style.transition='opacity .55s ease,transform .55s ease';obs.observe(el);el.classList.add('is-in')});
 }
 if(window.matchMedia('(hover:hover) and (pointer:fine)').matches){const art=doc.querySelector('.hero-art');art?.addEventListener('pointermove',e=>{const r=art.getBoundingClientRect();art.style.setProperty('--px',String((e.clientX-r.left-r.width/2)/r.width));art.style.setProperty('--py',String((e.clientY-r.top-r.height/2)/r.height));});art?.addEventListener('pointerleave',()=>{art.style.setProperty('--px','0');art.style.setProperty('--py','0')});}
})();'''

nav_items=[('about','О средстве'),('ingredients','Состав'),('how','Применение'),('faq','Вопросы')]

favicon='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="13" fill="#1d614d"/><path d="M18 42C19 24 31 14 46 14c0 23-11 35-28 28ZM23 39 42 21" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
for slug,s in SPECS.items():
 (ROOT/slug/'assets'/'favicon.svg').write_text(favicon,encoding='utf8')
 def e(v):return html.escape(str(v))
 def btns(location):
  return f'''<div class="actions">
    <a class="button primary" data-event="ozon_click" href="{e(s['ozon'])}" target="_blank" rel="noopener noreferrer"><span>Ozon</span><span class="arrow" aria-hidden="true">↗</span></a>
    <a class="button secondary" data-event="wb_click" href="{e(s['wb'])}" target="_blank" rel="noopener noreferrer"><span>Wildberries</span><span class="arrow" aria-hidden="true">↗</span></a></div>'''
 questions=[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in s['qa']]
 jld={"@context":"https://schema.org","@graph":[{"@type":"Organization","@id":"https://zdrava.top/#organization","name":"ЗДРАВА","url":"https://zdrava.top/"},{"@type":"Product","@id":f"https://zdrava.top/{slug}/#product","name":s['name'],"description":s['hero_desc'],"url":f"https://zdrava.top/{slug}/","image":[f"https://zdrava.top/{slug}/assets/product.png"],"brand":{"@id":"https://zdrava.top/#organization"},"size":"50 мл","sameAs":[s['ozon'],s['wb']]},{"@type":"FAQPage","mainEntity":questions}]}
 # No fake Offer or InStock: seller/platform availability and real price unverified.
 scenario_html=''.join(f'<article class="scenario" data-animate><span class="s-n">{i}</span><div><h3>{e(title)}</h3><p>{e(desc)}</p></div></article>' for i,(title,desc) in enumerate(s['scenarios'],1))
 ingr_html=''.join(f'<article class="ing" data-animate><span class="ing-number">{i}</span><h3>{e(title)}</h3><p>{e(desc)}</p></article>' for i,(title,desc) in enumerate(s['ingredientGroups'],1))
 steps_html=''.join(f'<li data-animate><span class="n">{i}</span><div><h3>{e(title)}</h3><p>{e(desc)}</p></div></li>' for i,(title,desc) in enumerate(s['steps'],1))
 faq_html=''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in s['qa'])
 html_code=f'''<!doctype html>
<html lang="ru"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light"><meta name="theme-color" content="{'#e5efe9' if slug=='mikozacid' else '#e8f5fc'}">
<title>{e(s['pageTitle'])}</title>
<meta name="description" content="{e(s['descSEO'])}">
<!-- Preview only. After verifying product labels, rights, domain and legal copy: replace with index,follow. -->
<meta name="robots" content="noindex,nofollow">
<link rel="canonical" href="https://zdrava.top/{slug}/">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" as="image" href="assets/product.png" fetchpriority="high">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500;600;700&family=Onest:wght@500;600;700;800&display=swap" rel="stylesheet">
<meta property="og:site_name" content="ЗДРАВА"><meta property="og:type" content="product"><meta property="og:locale" content="ru_RU">
<meta property="og:title" content="{e(s['pageTitle'])}"><meta property="og:description" content="{e(s['descSEO'])}">
<meta property="og:image" content="https://zdrava.top/{slug}/assets/og-image.jpg"><meta property="og:url" content="https://zdrava.top/{slug}/">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(jld,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')}</script>
<style>{css}</style>
<!-- To enable Yandex.Metrika/Webvisor: install approved counter in head and set window.ZDRAVA_METRIKA_ID below. No tracking is sent without an installed counter. -->
<script>window.ZDRAVA_METRIKA_ID=null;window.dataLayer=window.dataLayer||[];</script>
<!-- Motion libraries are enhancement only. Page remains functional if CDN fails. -->
<script defer src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/ScrollTrigger.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/lenis@1.3.17/dist/lenis.min.js"></script>
<script>document.addEventListener('DOMContentLoaded',()=>{{{js}}});</script>
<noscript><style>@media(max-width:820px){{.header-inner{{flex-wrap:wrap}}.nav{{display:flex;position:static;flex:1 1 100%;flex-direction:row;overflow:auto;align-items:center;padding:6px 0 18px;gap:22px}}.nav a{{min-height:44px;display:inline-flex;align-items:center;white-space:nowrap}}.menu-trigger{{display:none}}}}</style></noscript>
</head><body class="{s['style']}">
<a class="skip" href="#main">Перейти к содержимому</a><div class="progress" aria-hidden="true"><span></span></div>
<header class="site-header"><div class="wrap header-inner">
 <a href="#top" class="logo" aria-label="ЗДРАВА — наверх"><span class="logo-mark" aria-hidden="true"></span>ЗДРАВА</a>
 <nav id="nav" class="nav" aria-label="Навигация по странице">{''.join(f'<a href="#{id}">{label}</a>' for id,label in nav_items)}</nav>
 <a href="#buy" class="header-action" data-event="where_buy_click">Где купить ↗</a>
 <button class="menu-trigger" type="button" id="menu-trigger" aria-label="Открыть меню" aria-controls="nav" aria-expanded="false">☰</button>
 </div></header>
<main id="main">
<section class="hero" id="top" aria-labelledby="title"><div class="wrap hero-layout">
 <div class="hero-copy"><p class="eyebrow">{e(s['label'])}</p>
  <h1 id="title" class="display"><span class="line">{e(s['hero1'])}</span><span class="line accent">{e(s['hero2'])}</span><span class="line">{e(s['hero3'])}</span></h1>
  <p class="subtitle">{e(s['hero_desc'])}</p>{btns('hero')}
  <div class="hero-note"><span>50 мл</span><span>Наружное применение</span></div></div>
 <div class="hero-art" aria-label="Фото упаковки {e(s['name'])}"><span class="art-number" aria-hidden="true">50</span><div class="art-ring" aria-hidden="true"></div><div class="art-plate" aria-hidden="true"></div><div class="art-light" aria-hidden="true"></div><img class="art-product" src="assets/product.png" alt="{e(s['name'])}, оригинальная туба 50 мл" width="{s['srcWidth']}" height="{s['srcHeight']}" loading="eager" decoding="async" fetchpriority="high"><div class="art-small"><strong><em class="counter" data-value="50" style="font-style:normal;font-variant-numeric:tabular-nums">50</em> <span style="font:700 12px var(--font-body);letter-spacing:0">мл</span></strong><span>Формат тубы</span></div></div>
 </div><div class="hero-index" aria-hidden="true">ЛИСТАЙТЕ НИЖЕ</div></section>
<!-- Section 2: about the product -->
<section class="section about" id="about" aria-labelledby="about-title"><div class="wrap">
 <div class="section-top"><div><p class="kicker">{e(s['aboutKicker'])}</p><h2 class="section-heading" id="about-title">{e(s['aboutTitle'])}</h2></div><p class="section-lead">{e(s['aboutText'])}</p></div>
 <div class="about-grid"><div class="about-scene"><img src="assets/product.png" alt="Упаковка {e(s['name'])} — 50 мл" width="{s['srcWidth']}" height="{s['srcHeight']}" loading="lazy" decoding="async"></div>
 <div class="about-textbox"><strong>{'Чистота и комфорт в привычном ритме.' if slug=='mikozacid' else 'После активности — время для себя.'}</strong><div><p>Небольшую тубу удобно взять с собой и использовать в рамках привычного ухода.</p><p class="smallnote">Уход за телом · 50 мл</p></div></div></div></div></section>
<!-- Section 3: three realistic use occasions -->
<section class="section scenarios" id="when" aria-labelledby="when-title"><div class="wrap"><p class="kicker">ВПИСЫВАЕТСЯ В ВАШ ДЕНЬ</p><h2 class="section-heading" id="when-title">Когда пригодится</h2><div class="scenario-grid">{scenario_html}</div></div></section>
<!-- Section 4: ingredient groups and full supplied composition -->
<section class="section ingredients" id="ingredients" aria-labelledby="ingredients-title"><div class="wrap"><div class="section-top"><div><p class="kicker">НАПОЛНЕНИЕ ФОРМУЛЫ</p><h2 class="section-heading" id="ingredients-title">В основе — состав.</h2></div><p class="section-lead">Выделили ключевые группы ингредиентов. Полный перечень доступен ниже — без сокращений.</p></div>
<div class="ingredients-grid">{ingr_html}</div>
<details class="expand" data-event="full_composition_open"><summary>Полный состав средства</summary><div class="inner"><p>{e(s['fullComp'])}</p><p>Состав приведён по предоставленному описанию товара. Перед использованием сверьтесь с актуальной упаковкой.</p></div></details></div></section>
<!-- Section 5: usage steps -->
<section class="section how" id="how" aria-labelledby="how-title"><div class="wrap"><div class="section-top"><div><p class="kicker">ПРОСТОЙ РИТУАЛ</p><h2 class="section-heading" id="how-title">Применение —<br>в три шага.</h2></div><p class="section-lead">Следуйте инструкции производителя и учитывайте индивидуальную реакцию кожи.</p></div><div class="how-content"><ol class="steps">{steps_html}</ol><div class="how-accent-wrap"><div class="how-accent"><span class="counter" data-value="{e(s['stepFlag'])}" style="font-variant-numeric:tabular-nums">{e(s['stepFlag'])}</span></div><div class="how-unit">Дней · рекомендованный курс</div><p class="section-lead" style="font-size:14px;margin-top:20px">Нанесение: {e(s['use'])}. По описанию товара. Сверьтесь с упаковкой.</p></div></div></div></section>
<!-- Section 6: native details, accessible without JavaScript -->
<section class="section faq" id="faq" aria-labelledby="faq-title"><div class="wrap faq-grid"><div><p class="kicker">ЧАСТЫЕ ВОПРОСЫ</p><h2 class="section-heading" id="faq-title">Коротко<br>о важном.</h2><p class="section-lead">То, что обычно хочется уточнить до покупки.</p></div><div class="faq-list">{faq_html}</div></div></section>
<!-- Section 7: purchase links to marketplaces only -->
<section class="buy" id="buy" aria-labelledby="buy-title"><div class="wrap buy-inner"><div><p class="kicker">ВЫБРАТЬ ПЛОЩАДКУ</p><h2 class="section-heading" id="buy-title">{e(s['name'])}.<br>Выбирайте, где удобно.</h2><p class="section-lead">Переход к официальным карточкам товара на маркетплейсах.</p></div><div>{btns('bottom')}<p class="buy-remark">Актуальная цена, наличие и доставка — в карточке товара.</p></div></div></section>
</main>
<footer class="footer"><div class="wrap"><div class="footer-inner"><a href="#top" class="logo"><span class="logo-mark" aria-hidden="true"></span>ЗДРАВА</a><p>Средство для наружного применения. Не является лекарственным препаратом. При индивидуальной непереносимости компонентов не использовать. Информация на странице не заменяет рекомендацию врача. Перед применением сверьтесь с упаковкой.</p><a class="up" href="#top">Наверх ↑</a></div><div class="copyright">© ЗДРАВА. Сведения о товаре приведены по предоставленному описанию.</div></div></footer>
<div class="mobile-dock" aria-label="Покупка на маркетплейсах"><a href="{e(s['ozon'])}" target="_blank" rel="noopener noreferrer" data-event="ozon_click">Ozon ↗</a><a href="{e(s['wb'])}" target="_blank" rel="noopener noreferrer" data-event="wb_click">Wildberries ↗</a></div>
</body></html>'''
 (ROOT/slug/'index.html').write_text(html_code,encoding='utf8')
 # project source files for standalone reuse & audit (page is self-contained)
 (ROOT/slug/'source-design.css').write_text(css,encoding='utf8')
 (ROOT/slug/'source-motion.js').write_text(js,encoding='utf8')

(ROOT/'robots.txt').write_text('''# TEMPLATE. Publish in domain root ONLY after release approval.
User-agent: *
Allow: /
Sitemap: https://zdrava.top/sitemap.xml
''',encoding='utf8')
(ROOT/'sitemap.xml').write_text('''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://zdrava.top/mikozacid/</loc></url>
  <url><loc>https://zdrava.top/hot-ice/</loc></url>
</urlset>''',encoding='utf8')
(ROOT/'README_TIMEWEB.md').write_text('''# ЗДРАВА — два новых лендинга v8 (новая разработка)

## Папки и загрузка на Timeweb
- `mikozacid/` — независимый лендинг «Микозацид».
- `hot-ice/` — независимый лендинг «Горячий лёд».
- В каждой папке `index.html` — **автономная страница**, плюс `assets/product.png`, `assets/favicon.svg`, `assets/og-image.jpg`. Файлы `source-design.css` и `source-motion.js` — редактируемые исходники того же встроенного CSS/JS; браузер их отдельно не запрашивает.
- В корне этого ZIP `robots.txt` и `sitemap.xml` — **шаблоны, не устанавливать поверх существующих файлов домена до проверки**. Их корректность зависит от подтверждения канонического домена.
- Убедиться в настройках Timeweb, что `zdrava.top` действительно указывает на предполагаемый `public_html`. Только после этого загрузить **две папки** внутрь корня домена, рядом с его существующим `index.html`. Не заменять основной сайт «ЗДРАВА» и `flebodia/`.

## Визуальная система
- Оба сайта: Onest для заголовков и Golos Text для текста (2 семейства).
- Микозацид — ботанический зелёный editorial; Горячий лёд — ледяной голубой editorial.
- Оригинальные PNG туб побайтово сохранены из v7. Новые OG-превью собраны композиционно, не перерисовывают надпись на упаковке.
- GSAP/ScrollTrigger и Lenis по возможности загружаются по CDN; без них текст, ссылки и `<details>` доступны.
- На мобильных тяжёлые эффекты должны быть отключены и при `prefers-reduced-motion` анимация отсутствует.

## ПЕРЕД ЗАПУСКОМ (обязательные проверки)
1. **Подтвердить домен**: мастер-ТЗ использует `zdrava.top`, в истории фигурирует `zdrava.ru`; canonical/OG/JSON-LD/sitemap должны совпасть с реальным основным URL.
2. **Подтвердить состав и маркировку по физической тубе**. Особенно «Горячий лёд»: в предоставленном текстовом описании «крем», на тубе «гель»; далее на тубе может быть упоминание «водоросли», которых нет в предоставленном полном списке. У «Микозацида» рекламный текст перечислял вещества, отсутствующие в полном составе; они сознательно НЕ заявлены на сайте.
3. **Нет подтверждённых цен и остатков на площадках**: в Product JSON-LD **НЕ добавлялись фиктивные price, InStock или Offers**. FAQPage разметка не гарантирует расширенный сниппет.
4. **Индексация отключена** через `<meta name="robots" content="noindex,nofollow">`. Только после редакционной и юридической проверки заменить на `index,follow` и публиковать robots/sitemap в доменном корне (не мешая существующему сайту).
5. Проверить работу интернет/CDN/Google Fonts у целевой аудитории; для полноценно автономного релиза желательно перенести лицензированные WOFF2 и JS-библиотеки локально. 
6. Подключить Яндекс Метрику только после получения ID и пользовательского согласования. В HTML есть `window.ZDRAVA_METRIKA_ID=null` и отслеживаемые `data-event` для Ozon/WB/куда купить; система не утверждает, что аналитика уже работает.
7. Проверить реальный мобильный браузер, Yandex.Webmaster, Google Search Console, PageSpeed, JSON-LD валидатор. Lighthouse ≥ 90 и LCP <2.5с — **целевые показатели, не измеренные**.
8. **Не изменять действующие страницы** на Timeweb до проверки/согласования.

## Сохранение v7 и исходников
В GitHub отдельная ветка `archive/v7-cinematic-motion` сохраняет весь предыдущий проект. Новые исходники v8 лежат в `next-v8/mikozacid` и `next-v8/hot-ice`; предыдущие v7 в основной ветке можно сохранять до финального релиза.
''',encoding='utf8')
# validate html/links and images
for slug,s in SPECS.items():
 txt=(ROOT/slug/'index.html').read_text()
 assert txt.count('<h1')==1
 assert 'Wildberries' in txt and 'Ozon' in txt
 assert 'noindex,nofollow' in txt
 assert txt.count('<details')==5
 assert 'src="assets/product.png"' in txt
 assert (ROOT/slug/'assets/product.png').read_bytes()==zipfile.ZipFile(V7).read(f'{slug}/assets/product.png')
 assert 'Manrope' not in txt and 'Arial' not in txt
 for dest in ['assets/product.png','assets/favicon.svg','assets/og-image.jpg']:
  assert (ROOT/slug/dest).is_file()
 print(slug,'html bytes',len(txt.encode()),'image bytes',(ROOT/slug/'assets'/'product.png').stat().st_size)

zipout=Path('/mnt/data/zdrava-next-v8-timeweb.zip')
with zipfile.ZipFile(zipout,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for f in sorted(ROOT.rglob('*')):
  if f.is_file():z.write(f,f.relative_to(ROOT))
print('ZIP',zipout,zipout.stat().st_size,'SHA256',hashlib.sha256(zipout.read_bytes()).hexdigest())
