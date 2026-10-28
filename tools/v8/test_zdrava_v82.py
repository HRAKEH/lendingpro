from pathlib import Path
import re, asyncio, base64, json, tinycss2, zipfile
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
root=Path('/mnt/data/zdrava-v82')
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
  rows=[]
  for site in ['hot-ice','mikozacid']:
   h=(root/site/'index.html').read_text()
   soup=BeautifulSoup(h,'html.parser')
   assert len(soup.select('h1'))==1
   assert len(soup.select('section[id]'))>=7
   assert len(soup.select('.chapter-rail a'))==6
   assert len(soup.select('.motion-ribbon-track'))==1
   assert len(soup.select('.formula-flow'))==1
   assert len(soup.select('.motion-trace'))==1
   assert 'noindex,nofollow' in h
   assert h.count('www.ozon.ru')>=3 and h.count('wildberries.ru')>=3
   css=(root/site/'source-design.css').read_text()
   errors=[n for n in tinycss2.parse_stylesheet(css,skip_comments=True,skip_whitespace=True) if n.type=='error']
   assert not errors, errors
   h=re.sub(r'https://cdn\.jsdelivr\.net/[^" ]+', 'data:text/javascript,',h)
   h=re.sub(r'https://fonts\.googleapis\.com/[^" ]+', 'data:text/css,',h)
   # replace local product source so it still loads through set_content
   img=base64.b64encode((root/site/'assets/product.png').read_bytes()).decode()
   h=h.replace('src="assets/product.png"','src="data:image/png;base64,'+img+'"')
   for width in [360,390,768,1440]:
    page=await browser.new_page(viewport={'width':width,'height':900},device_scale_factor=1,reduced_motion='reduce' if width==768 else 'no-preference')
    errs=[];page.on('pageerror',lambda x:errs.append(str(x)))
    try:
     await page.set_content(h,wait_until='domcontentloaded',timeout=18000)
     await page.wait_for_timeout(190)
     d=await page.evaluate('''() => ({scroll:document.documentElement.scrollWidth,inner:innerWidth, hero:!!document.querySelector('.kinetic-halo'), product:[...document.querySelectorAll('img.art-product')].every(e=>e.complete && e.naturalWidth>0), ribbon:!!document.querySelector('.motion-ribbon'), menu:!!document.querySelector('#menu-trigger'), href:[...document.querySelectorAll('.chapter-rail a')].every(a=>!!document.querySelector(a.getAttribute('href'))),rail:!!document.querySelector('.chapter-rail'), motions:document.querySelectorAll('.motion-trace path').length})''')
     assert d['scroll']<=width+1,(site,width,d)
     assert d['product'] and d['ribbon'] and d['href'] and d['motions'] and not errs,(site,width,d,errs)
     if width in (390,1440):
      await page.evaluate('window.scrollTo(0,0)');await page.wait_for_timeout(250)
      await page.screenshot(path=f'/mnt/data/zdrava-v82-{site}-{width}.png',full_page=False)
     # native details toggle
     faq=page.locator('.faq-list details').first
     await faq.locator('summary').click();assert await faq.get_attribute('open') is not None
     if width<820:
      await page.locator('#menu-trigger').click();assert await page.locator('#nav').evaluate('(n)=>n.classList.contains("is-open")')
      await page.locator('#menu-trigger').click()
     rows.append(dict(site=site,width=width,overflow=d['scroll']-width,jsErrors=len(errs),faqOpen=True))
    finally:await page.close()
  await browser.close()
  print(json.dumps(rows,ensure_ascii=False,indent=2))
if __name__=='__main__':asyncio.run(main())
