from pathlib import Path
import re,base64,json
from playwright.sync_api import sync_playwright
src=Path('/mnt/data/zdrava-v8-motion')
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 for name in ['hot-ice','mikozacid']:
  for width in [360,390,768,1440]:
   page=browser.new_page(viewport={'width':width,'height':900},device_scale_factor=1,reduced_motion='reduce' if width==768 else 'no-preference')
   errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   # CDN unavailable in isolated runtime. This tests actual HTML/CSS/JS fallback with real product pixels.
   page.route('**/*',lambda route:route.abort())
   html=(src/name/'index.html').read_text()
   image=(src/name/'assets/product.png').read_bytes()
   data='data:image/png;base64,'+base64.b64encode(image).decode('ascii')
   html=html.replace('src="assets/product.png"','src="'+data+'"')
   try:
    page.set_content(html,wait_until='domcontentloaded',timeout=15000)
    page.wait_for_timeout(100)
    data=page.evaluate('''() => ({w:innerWidth, doc:document.documentElement.scrollWidth, h1:document.querySelector('h1')?.innerText, imgs:[...document.querySelectorAll('img')].map(i=>[i.complete,i.naturalWidth]), motion:!!document.querySelector('.art-prism'), buttons:[...document.querySelectorAll('a.button')].length, details:document.querySelectorAll('details').length, noscript: !!document.querySelector('noscript'), step:document.querySelector('[data-current-step]')?.innerText})''')
    if width in [390,1440]:
     page.screenshot(path=f'/mnt/data/motion-{name}-{width}.png',full_page=False)
    if width==390:
     page.get_by_role('button',name='Открыть меню').click()
     data['menuOpens']=page.locator('#nav').evaluate('(e)=>e.classList.contains("is-open")')
     page.get_by_role('button',name='Закрыть меню').click()
     data['menuCloses']=not page.locator('#nav').evaluate('(e)=>e.classList.contains("is-open")')
     page.locator('details').first.locator('summary').click()
     data['faqOpens']=page.locator('details').first.evaluate('(e)=>e.open')
    results.append({'name':name,'width':width,'data':data,'errors':errors})
   except Exception as e:
    results.append({'name':name,'width':width,'error':str(e)[:600]})
   finally: page.close()
 browser.close()
print(json.dumps(results,ensure_ascii=False,indent=2))
