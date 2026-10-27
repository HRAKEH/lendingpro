from pathlib import Path
from bs4 import BeautifulSoup
import re,zipfile,hashlib, subprocess, json, tinycss2
root=Path('/mnt/data/lendingpro-cinematic-v7');baseline=Path('/mnt/data/lendingpro-atmosphere-v6');records=[]
for product in ['mikozacid','hot-ice']:
 folder=root/product
 soup=BeautifulSoup((folder/'index.html').read_text(),'html.parser')
 assert soup.select_one('meta[name=robots]')['content']=='noindex,nofollow'
 assert len(soup.select('.hero h1 .motion-line__inner'))==2
 assert len(soup.select('.market-actions a'))==2
 assert len(soup.select('.purchase-links a'))==2
 assert len(soup.select('.mobile-buy-dock a'))==2
 assert len(soup.select('.motion-interlude .motion-interlude__product'))==1
 assert not re.search(r'(?<!\d)0[1-9] (?=\.|/|—|[-])',soup.get_text(' '))
 assert soup.select_one('script[src="motion.js"]')
 assert soup.select_one('link[href="motion.css"]')
 assert sum([bool(soup.select_one(f'a[href*="{host}"]')) for host in ['ozon.ru','wildberries.ru']])==2
 assert (baseline/product/'assets/product.png').read_bytes()==(folder/'assets/product.png').read_bytes(), 'package changed'
 assert (folder/'assets/texture.png').is_file()
 # all local links and scripts
 refs=[a.get('src','') for a in soup.select('[src]')]+[a.get('href','') for a in soup.select('link[href]')]
 missing=[]
 for ref in refs:
  if not ref or ref.startswith(('http','//','#','data:')):continue
  if not (folder/ref).is_file():missing.append(ref)
 assert not missing,(product,'missing',missing)
 output=subprocess.run(['node','--check',str(folder/'motion.js')],capture_output=True,text=True)
 assert output.returncode==0,output.stderr
 output=subprocess.run(['node','--check',str(folder/'script.js')],capture_output=True,text=True)
 assert output.returncode==0,output.stderr
 cssdata={}
 for path in list(folder.glob('*.css')):
  text=path.read_text()
  parsed=tinycss2.parse_stylesheet(text,skip_whitespace=True,skip_comments=True)
  errors=[x for x in parsed if x.type=='error']
  assert not errors,(path,errors)
  cssdata[path.name]={'bytes':len(text),'blocks':len(parsed)}
 newcss=(folder/'motion.css').read_text()
 for marker in ['prefers-reduced-motion','motion-interlude','scroll-track','motion-line','mobile-buy-dock','glass-float','pointer']:
  assert marker in newcss or marker in (folder/'motion.js').read_text(),marker
 assert all('url("assets/product.png")' not in (folder/'motion.css').read_text() for _ in [0])
 imgs={x.name:hashlib.sha256(x.read_bytes()).hexdigest()[:20] for x in [folder/'assets/product.png',folder/'assets/texture.png']}
 records.append({'product':product,'h1':' '.join(soup.select_one('h1').stripped_strings),'source_unchanged':True,'image_sha':imgs['product.png'],'css':cssdata,'new_motion_js_bytes':(folder/'motion.js').stat().st_size,'static_links_ok':True,'node_syntax_ok':True})
zip_path=Path('/mnt/data/lendingpro-timeweb-v7-cinematic-motion.zip')
with zipfile.ZipFile(zip_path) as z:
 assert z.testzip() is None
 names=set(z.namelist())
 for prod in ['mikozacid','hot-ice']:
  for n in ['index.html','styles.css','editorial.css','atmosphere.css','motion.css','script.js','motion.js','assets/product.png','assets/texture.png']:
   assert f'{prod}/{n}' in names
print(json.dumps({'status':'Static + JavaScript parser validated','zip_size':zip_path.stat().st_size,'zip_entries':len(names),'browsing':'blocked by environment; not claimed','records':records},ensure_ascii=False,indent=2))
Path('/mnt/data/lendingpro-v7-static-qa.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
