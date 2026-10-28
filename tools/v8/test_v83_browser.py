from playwright.sync_api import sync_playwright
import json,base64
from pathlib import Path
root=Path('/mnt/data/zdrava-v83-cinematic-experience')
out=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for name in ['hot-ice','mikozacid']:
  html=(root/name/'index.html').read_text()
  data='data:image/png;base64,'+base64.b64encode((root/name/'assets/product.png').read_bytes()).decode()
  html=html.replace('src="assets/product.png"',f'src="{data}"')
  for width in [360,390,768,1440]:
   ctx=browser.new_context(viewport={'width':width,'height':850},reduced_motion='no-preference',device_scale_factor=1)
   page=ctx.new_page()
   errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.route('**/*',lambda route:route.abort())
   try:
    page.set_content(html,wait_until='domcontentloaded',timeout=17000)
    page.wait_for_timeout(450)
    metrics=page.evaluate('''() => {const e=document.querySelector('.experience'),i=document.querySelector('.experience__product'), cards=[...document.querySelectorAll('.ingredients-grid .ing')],b=cards.map(x=>{const r=x.getBoundingClientRect(),cs=getComputedStyle(x);return {x:Math.round(r.x),right:Math.round(r.right),width:Math.round(r.width),pad:cs.paddingLeft,padR:cs.paddingRight}});return {width:document.documentElement.scrollWidth, viewport:innerWidth, chapters:document.querySelectorAll('.experience__chapter').length, canvas:!!document.querySelector('canvas'), imgLoaded:i?.complete&&i.naturalWidth>0, cards:b, heroImage:document.querySelector('.hero .art-product')?.naturalWidth>0, sectionHeight:Math.round(e.getBoundingClientRect().height), sticky:getComputedStyle(e.querySelector('.experience__stage')).position} }''')
    if width==1440:
     page.evaluate('''() => {const e=document.querySelector('.experience');window.scrollTo({top:e.offsetTop+e.offsetHeight*.52-innerHeight*.5,behavior:'instant'})}''')
     page.wait_for_timeout(500)
     metrics['middle']=page.evaluate('''() => ({step:document.querySelector('.experience__step').textContent,progress:document.querySelector('.experience__progress i').style.transform,productStyle:document.querySelector('.experience__product').style.transform,chapterOpacity:[...document.querySelectorAll('.experience__chapter')].map(x=>x.style.opacity)})''')
     page.screenshot(path=f'/mnt/data/v83-{name}-desktop-story.png')
     page.locator('.ingredients').scroll_into_view_if_needed();page.screenshot(path=f'/mnt/data/v83-{name}-desktop-ingredients.png')
    if width==390:
     page.locator('.experience').scroll_into_view_if_needed();page.screenshot(path=f'/mnt/data/v83-{name}-mobile-story.png')
     page.locator('.ingredients').scroll_into_view_if_needed();page.screenshot(path=f'/mnt/data/v83-{name}-mobile-ingredients.png')
    result={'name':name,'width':width,'metrics':metrics,'errors':errors}
    print(json.dumps(result,ensure_ascii=False)[:1700]);out.append(result)
   except Exception as e:
    print('FAILED',name,width,str(e));out.append({'name':name,'width':width,'error':str(e)})
   ctx.close()
 browser.close()
Path('/mnt/data/v83-test-report.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
