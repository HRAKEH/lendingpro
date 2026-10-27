from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from bs4 import BeautifulSoup
from PIL import Image,ImageOps,ImageDraw,ImageFont
import shutil,hashlib,json,re

src=Path('/mnt/data/lendingpro-timeweb-v5-hot-ice-color-corrected.zip')
base=Path('/mnt/data/lendingpro-atmosphere-v6')
if base.exists():shutil.rmtree(base)
base.mkdir()
with ZipFile(src) as z:z.extractall(base)

for slug in ('mikozacid','hot-ice'):
 folder=base/slug
 orig=(folder/'assets'/'product.png').read_bytes()
 with Image.open(folder/'assets'/'product.png') as img:print(slug,'real package',img.size,img.mode,'hash',hashlib.sha256(orig).hexdigest()[:16])
 page=BeautifulSoup((folder/'index.html').read_text(encoding='utf-8'),'html.parser')
 # own new stylesheet; exact currently shipped styles and original photo untouched
 atmos_link=page.new_tag('link',rel='stylesheet',href='atmosphere.css')
 page.head.append(atmos_link)
 stage=page.select_one('.photo-stage')
 img=stage.select_one('.product-photo')
 vibe=page.new_tag('div');vibe['class']='atmosphere-sculpt';vibe['aria-hidden']='true'
 for cls in (['backdrop-glow','air-column','facet facet-1','facet facet-2','surface-wave','light-sweep'] if slug=='hot-ice' else ['backdrop-glow','foliage foliage-1','foliage foliage-2','ripple-1','ripple-2','light-sweep']):
  sp=page.new_tag('span');sp['class']=cls.split();vibe.append(sp)
 img.insert_before(vibe)
 # add complementary editorial glass plaque; no efficacy promises or fictitious awards
 floatbox=page.new_tag('div');floatbox['class']='glass-float';floatbox['aria-hidden']='true'
 ico=page.new_tag('span');ico['class']='glass-float__symbol';ico.string=('◌' if slug=='mikozacid' else '✳')
 details=page.new_tag('span');details['class']='glass-float__copy'
 top=page.new_tag('strong');top.string=('После активного дня' if slug=='hot-ice' else 'На каждый день')
 secondary=page.new_tag('small');secondary.string=('Уход за телом' if slug=='hot-ice' else 'Уход за стопами и ногтями')
 details.extend([top,secondary]);floatbox.extend([ico,details]);stage.append(floatbox)
 # remove duplicate stamp to let product breathe, user wants visual not tech
 for el in stage.select('.photo-overline,.photo-volume'):el.decompose()
 # Add a glass-overprint section in product introduction but no spurious claims: subtle bento accent in #about
 target=page.select_one('.intro-side')
 if target:
  mini=page.new_tag('div');mini['class']='care-ticket'
  title=page.new_tag('span');title['class']='care-ticket__title';title.string='Формат 50 мл'
  tail=page.new_tag('span');tail['class']='care-ticket__text';tail.string='Компактная туба для привычного ухода'
  mini.extend([title,tail]);target.append(mini)
 # Maintain clear text and avoid fake hero tech data.
 (folder/'index.html').write_text(str(page),encoding='utf-8')

common = '''/* LandingPro v6 — precise glass and subtle relief, original packaging unchanged.
   CSS scenes only: no fake photography, modified labels or product reconstructions. */
.hero-visual {position:relative;isolation:isolate}
.hero-visual::before {content:"";position:absolute;z-index:-1;pointer-events:none;inset:7% 3% -3%;filter:blur(30px);border-radius:50%;background:var(--stage-shadow)}
.photo-stage {isolation:isolate;overflow:hidden;position:relative;min-height:660px;border-radius:32px!important;background:var(--stage-ground)!important;box-shadow:var(--stage-elevation);border:1px solid rgba(255,255,255,.7)}
.photo-stage::before {content:"";position:absolute;z-index:1;inset:13px;border:1px solid rgba(255,255,255,.48)!important;border-radius:24px!important;opacity:1!important;pointer-events:none}
.photo-stage::after {content:"";position:absolute;inset:auto 9% -6% 9%;height:25%;border-radius:50%;background:var(--ground-reflection);filter:blur(22px);z-index:0;pointer-events:none}
.atmosphere-sculpt {position:absolute;inset:0;pointer-events:none;overflow:hidden;z-index:0}
.atmosphere-sculpt>span{position:absolute;display:block;pointer-events:none}
.atmosphere-sculpt .backdrop-glow{inset:3% 0 0;background:var(--backlight);filter:blur(10px)}
.atmosphere-sculpt .light-sweep{width:110%;height:60%;left:-38%;top:-32%;transform:rotate(-27deg);background:linear-gradient(90deg,transparent 32%,rgba(255,255,255,.15) 50%,transparent 67%);filter:blur(4px)}
.photo-stage .product-photo{position:relative;z-index:4;max-height:615px;max-width:84%;width:auto;height:auto;object-fit:contain;transform:translateY(-9px);padding:25px 0 15px;filter:var(--product-shadow);animation:float-in 950ms cubic-bezier(.2,.7,.2,1) both}
@keyframes float-in{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(-9px)}}
.glass-float{position:absolute;z-index:6;left:22px;bottom:29px;display:flex;align-items:center;gap:11px;max-width:235px;min-height:64px;padding:11px 16px;border-radius:13px;border:1px solid rgba(255,255,255,.74);background:rgba(255,255,255,.51);backdrop-filter:blur(15px) saturate(1.22);-webkit-backdrop-filter:blur(15px) saturate(1.22);box-shadow:0 11px 22px rgba(19,55,62,.12),inset 1px 1px 1px rgba(255,255,255,.9);color:var(--ink)}
.glass-float__symbol{display:grid;place-items:center;flex:none;width:34px;height:34px;border-radius:50%;font:700 23px/1 var(--font-title);color:var(--accent);background:rgba(255,255,255,.49);box-shadow:inset 2px 2px 5px rgba(18,57,67,.11),2px 2px 5px rgba(255,255,255,.8)}
.glass-float__copy{display:flex;flex-direction:column;gap:3px;white-space:normal;line-height:1.3}
.glass-float__copy strong{font:700 13px/1.3 var(--font-text);letter-spacing:-.01em}
.glass-float__copy small{font:400 11px/1.3 var(--font-text)}
/* small touch of neomorphism, not a page full of fake soft-shadow buttons */
.care-ticket{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-top:29px;padding:15px 20px;border:1px solid color-mix(in srgb,var(--accent) 14%,transparent);border-radius:15px;background:color-mix(in srgb,var(--soft) 25%,white);box-shadow:9px 9px 20px rgba(20,50,50,.045),-7px -7px 18px rgba(255,255,255,.88),inset 1px 1px 0 rgba(255,255,255,.8)}
.care-ticket__title{font:700 16px/1.3 var(--font-title);white-space:nowrap}.care-ticket__text{font:400 13px/1.4 var(--font-text);opacity:.8;text-align:right}
/* Rest state remains button-like and interactive */
.market-actions .btn-alt{background:rgba(255,255,255,.55);border-color:color-mix(in srgb,var(--accent) 55%,white);box-shadow:inset 0 1px 0 rgba(255,255,255,.85),0 5px 12px rgba(25,67,72,.05)}
.market-actions .btn-alt:hover{background:rgba(255,255,255,.85)}
.market-actions .btn-primary{box-shadow:inset 0 1px 0 rgba(255,255,255,.2),0 6px 14px rgba(25,67,72,.09)}
.occasion-section{position:relative;overflow:hidden}
.occasion-section::before{content:"";position:absolute;top:-130px;right:-115px;width:370px;height:370px;border-radius:50%;background:radial-gradient(circle,rgba(255,255,255,.86),transparent 66%);pointer-events:none}
.occasion{position:relative;z-index:1}
.full-composition{border-radius:13px;overflow:hidden}
.faq-list details{transition:background-color .2s}
.faq-list details:hover{background:color-mix(in srgb,var(--soft) 14%,transparent)}
@media (max-width:1100px){.photo-stage{min-height:540px}.photo-stage .product-photo{max-height:515px}.glass-float{left:17px;bottom:18px}}
@media (max-width:800px){.photo-stage{min-height:520px}.photo-stage .product-photo{max-height:485px}}
@media (max-width:600px){.hero-visual{width:100%}.photo-stage{min-height:455px;border-radius:20px!important}.photo-stage::before{inset:8px;border-radius:14px!important}.photo-stage .product-photo{max-height:448px;max-width:85%;padding:18px 0 14px}.glass-float{left:12px;bottom:12px;max-width:185px;padding:9px 11px;min-height:51px;gap:8px;border-radius:10px}.glass-float__symbol{width:26px;height:26px;font-size:18px}.glass-float__copy strong{font-size:11px}.glass-float__copy small{font-size:10px}.care-ticket{padding:15px;align-items:start;flex-direction:column;gap:6px}.care-ticket__text{text-align:left}}
@media (max-width:360px){.photo-stage{min-height:420px}.photo-stage .product-photo{max-height:407px}}
@media (prefers-reduced-motion:reduce){.photo-stage .product-photo{animation:none!important;transform:none!important}.photo-stage .light-sweep{display:none}}
'''

ice='''/* ICE PREMIUM — luminous crystal forms with restrained glass; these are CSS only. */
:root {--stage-ground:linear-gradient(132deg,#d4e8f7 1%,#eaf6ff 44%,#b0d0e9 100%);--stage-elevation:19px 25px 54px rgba(31,96,145,.16),-9px -9px 28px rgba(255,255,255,.91);--stage-shadow:rgba(71,133,174,.19);--backlight:radial-gradient(circle at 68% 17%,rgba(255,255,255,.91),transparent 56%);--ground-reflection:radial-gradient(ellipse,rgba(34,99,145,.20),transparent 64%);--product-shadow:drop-shadow(5px 29px 21px rgba(20,59,96,.23))}
.photo-stage--hot-ice .product-photo{max-height:620px;max-width:78%;filter:var(--product-shadow)}
.atmosphere-sculpt .air-column{top:15%;left:17%;width:66%;height:62%;border-radius:48% 52% 48% 52%;background:radial-gradient(ellipse at 46% 31%,rgba(255,255,255,.76) 0,rgba(225,245,255,.25) 44%,rgba(88,159,195,.11) 75%);box-shadow:inset -15px -10px 35px rgba(67,136,174,.19),inset 3px 5px 12px rgba(255,255,255,.8),0 15px 35px rgba(14,79,122,.08);backdrop-filter:blur(3px)}
.atmosphere-sculpt .facet{clip-path:polygon(18% 0,82% 0,100% 33%,77% 100%,5% 90%,0 30%);border-radius:24px;background:linear-gradient(135deg,rgba(255,255,255,.87),rgba(175,214,238,.16) 42%,rgba(255,255,255,.64) 51%,rgba(79,160,202,.14) 87%);box-shadow:inset 0 0 22px rgba(255,255,255,.75),0 12px 24px rgba(48,103,138,.13);border:1px solid rgba(255,255,255,.65);opacity:.72}
.atmosphere-sculpt .facet-1{width:205px;height:245px;right:-76px;bottom:-48px;transform:rotate(18deg)}
.atmosphere-sculpt .facet-2{width:156px;height:146px;left:-61px;bottom:94px;transform:rotate(-14deg);opacity:.5}
.atmosphere-sculpt .surface-wave{height:85px;inset:auto 0 0 0;background:radial-gradient(ellipse at 50% 30%,rgba(255,255,255,.8),transparent 63%),linear-gradient(0deg,rgba(83,144,185,.21),transparent);border-top:1px solid rgba(255,255,255,.63)}
@media(max-width:600px){.photo-stage--hot-ice .product-photo{max-height:445px;max-width:81%}.atmosphere-sculpt .facet-1{width:135px;height:155px;right:-48px;bottom:-20px}.atmosphere-sculpt .facet-2{width:118px;height:100px;left:-52px;bottom:65px}}
'''

green='''/* JADE BOTANICAL — translucent leaves, mineral glass and diffused daylight. CSS only. */
:root {--stage-ground:linear-gradient(145deg,#d2e2d6 0%,#e9f1e8 43%,#b5d5c1 100%);--stage-elevation:18px 23px 49px rgba(37,100,68,.14),-10px -10px 25px rgba(255,255,255,.86);--stage-shadow:rgba(70,114,84,.16);--backlight:radial-gradient(circle at 55% 10%,rgba(255,255,255,.85),transparent 62%);--ground-reflection:radial-gradient(ellipse,rgba(37,88,55,.17),transparent 64%);--product-shadow:drop-shadow(5px 27px 19px rgba(13,67,43,.25))}
.photo-stage--mikozacid .product-photo{max-height:615px;max-width:88%;filter:var(--product-shadow);transform:translate(11px,-8px)}
.atmosphere-sculpt .foliage{background:radial-gradient(ellipse at 27% 25%,rgba(245,255,232,.79) 0%,rgba(92,155,110,.47) 45%,rgba(11,86,58,.30) 90%);border-radius:2% 100% 10% 100%;box-shadow:inset 4px 5px 13px rgba(255,255,255,.43),15px 17px 29px rgba(22,80,39,.10);filter:blur(1.6px)}
.atmosphere-sculpt .foliage-1{width:240px;height:350px;left:-137px;bottom:80px;transform:rotate(-29deg)}
.atmosphere-sculpt .foliage-2{width:180px;height:230px;right:-93px;top:-91px;transform:rotate(21deg);opacity:.57}
.atmosphere-sculpt .ripple-1{width:350px;height:350px;left:calc(50% - 175px);top:19%;border:1px solid rgba(255,255,255,.5);border-radius:50%;box-shadow:0 0 0 33px rgba(255,255,255,.07),0 0 0 73px rgba(246,255,244,.05);opacity:.86}
.atmosphere-sculpt .ripple-2{height:110px;bottom:-60px;left:-16%;width:132%;border-radius:50%;border-top:2px solid rgba(255,255,255,.57);background:linear-gradient(0deg,rgba(28,102,68,.14),transparent)}
@media(max-width:600px){.photo-stage--mikozacid .product-photo{max-height:452px;max-width:89%;transform:translate(8px,-7px)}.atmosphere-sculpt .foliage-1{width:145px;height:210px;left:-90px;bottom:59px}.atmosphere-sculpt .foliage-2{width:105px;height:155px;right:-55px;top:-53px}.atmosphere-sculpt .ripple-1{width:245px;height:245px;left:calc(50% - 122px)}}
@media(prefers-reduced-motion:reduce){.photo-stage--mikozacid .product-photo{transform:none!important}}
'''

(base/'hot-ice'/'atmosphere.css').write_text(common+ice,encoding='utf-8')
(base/'mikozacid'/'atmosphere.css').write_text(common+green,encoding='utf-8')

(base/'README_TIMEWEB.txt').write_text('''LendingPro / V6 — glass, atmospheric product visuals, subtle neomorphism\n\nFor Timeweb: extract the mikozacid/ and hot-ice/ folders into the CONFIRMED document root next to your current website index.html, WITHOUT overwriting it.\n\nInside each folder: index.html, styles.css, editorial.css, atmosphere.css, script.js, assets/product.png.\n\nProduct PNG is EXACTLY BYTE-IDENTICAL to version V5 and user-provided cutouts — only surrounding HTML/CSS has changed.\n\nThese pages are currently set to noindex,nofollow. Confirm product labels, claims and image rights before public ad/SEO launch. Do not publish as a medically approved website.\n\nTo preview locally, open mikozacid/index.html or hot-ice/index.html. For correct mobile navigation, view in browser.\n''',encoding='utf-8')

zipout=Path('/mnt/data/lendingpro-timeweb-v6-glass-and-relief.zip')
with ZipFile(zipout,'w',ZIP_DEFLATED,compresslevel=8) as z:
 for f in base.rglob('*'):
  if f.is_file():z.write(f,f.relative_to(base).as_posix())
print('Archive:',zipout,zipout.stat().st_size, 'files',sum(1 for f in base.rglob('*') if f.is_file()))
