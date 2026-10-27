from pathlib import Path
from bs4 import BeautifulSoup
import re,zipfile,subprocess,hashlib,io,json
import tinycss2
BASE=Path('/mnt/data/zdrava-v8-rebuild')
SOURCE=Path('/mnt/data/lendingpro-timeweb-v7-cinematic-motion.zip')
assert BASE.is_dir()
for slug in ('mikozacid','hot-ice'):
 html=(BASE/slug/'index.html').read_text(encoding='utf8')
 soup=BeautifulSoup(html,'html.parser')
 assert len(soup.select('h1'))==1
 assert len(soup.select('main'))==1
 assert len(soup.select('main section'))==7
 assert len(soup.select('.faq-list details'))==4
 assert len(soup.select('.steps li'))==3
 assert len(soup.select('.scenario'))==3
 assert len(soup.select('.ing'))==3
 assert len(soup.select('a[href*="ozon.ru"]'))==3
 assert len(soup.select('a[href*="wildberries.ru"]'))==3
 assert len(soup.title.string)<=60, (slug, soup.title.string)
 assert len(soup.select_one('meta[name="description"]').get('content'))<=160
 assert soup.select_one('meta[name="robots"]').get('content')=='noindex,nofollow'
 assert soup.select_one('html')['lang']=='ru'
 assert all(x.get('width') and x.get('height') for x in soup.select('img'))
 assert all((BASE/slug/x['src']).exists() for x in soup.select('img'))
 assert all(x['href'].startswith('https://') for x in soup.select('a[href^="https://"]'))
 assert len(re.findall('font-family:',html))>0
 assert not re.search(r'\b0[1-3]\b\s*</span>',html)
 assert 'Onest' in html and 'Golos Text' in html
 assert 'Manrope' not in html
 from PIL import Image
 im=Image.open(BASE/slug/'assets/product.png'); assert im.mode=='RGBA'
 with zipfile.ZipFile(SOURCE) as z:
  assert z.read(f'{slug}/assets/product.png') == (BASE/slug/'assets/product.png').read_bytes()
 ld=json.loads(soup.select_one('script[type="application/ld+json"]').text)
 assert [x['@type'] for x in ld['@graph']]==['Organization','Product','FAQPage']
 assert 'offers' not in ld['@graph'][1]
 assert len(ld['@graph'][2]['mainEntity'])==4
 css=soup.select_one('style').text
 assert not [x for x in tinycss2.parse_stylesheet(css) if x.type=='error']
 js=soup.find_all('script')[-1].text
 p=Path('/tmp')/(slug+'-inline-v8.js');p.write_text(js)
 r=subprocess.run(['node','--check',str(p)],capture_output=True,text=True)
 assert r.returncode==0, r.stderr
 print(f'{slug}: PASS | title chars {len(soup.title.string)} | product {im.size} | JSON-LD valid | no fake prices | JS/CSS valid | two fonts')
with zipfile.ZipFile('/mnt/data/zdrava-next-v8-timeweb.zip') as z:
 assert z.testzip() is None
 print('ZIP: PASS',len(z.namelist()),'files')
print('Note: Browser navigation blocked by container policy; actual rendered responsive/speed QA not claimed')
