from PIL import Image, ImageDraw, ImageFilter
import numpy as np, cv2
from pathlib import Path
out=Path('/mnt/data/lendingpro-trend-final'); out.mkdir(exist_ok=True)
for nm,file,poly in [
('mikozacid','IMG_0817.jpeg',[(534,229),(792,338),(790,353),(784,373),(763,415),(727,489),(684,583),(647,669),(612,740),(576,818),(539,873),(528,872),(515,903),(495,948),(489,955),(480,957),(468,953),(345,900),(330,891),(327,881),(329,872),(354,810),(351,797),(355,780),(373,732),(401,662),(436,567),(464,490),(492,405),(511,341),(523,293)]),
('hot-ice','IMG_0816.jpeg',[(281,34),(619,25),(622,46),(618,76),(610,107),(605,150),(598,189),(592,258),(586,369),(581,487),(573,611),(567,690),(559,743),(554,815),(551,844),(547,859),(533,868),(501,874),(420,873),(392,870),(376,863),(364,852),(359,833),(356,759),(349,733),(341,676),(336,612),(330,532),(322,409),(316,310),(306,214),(300,185),(289,122),(282,85)])
]:
  im=np.array(Image.open('/mnt/data/'+file).convert('RGB'))
  h,w=im.shape[:2]
  poly_np=np.array(poly,np.int32)
  mask0=np.zeros((h,w),np.uint8);cv2.fillPoly(mask0,[poly_np],255)
  # manually-drawn product silhouette protects package printed letters and panel, GrabCut only refines border strip.
  k=13 if nm=='mikozacid' else 9
  kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(k,k))
  interior=cv2.erode(mask0,kernel,iterations=1)>0
  exterior=cv2.dilate(mask0,kernel,iterations=1)==0
  gc=np.where(exterior,cv2.GC_BGD,np.where(interior,cv2.GC_FGD,cv2.GC_PR_FGD)).astype('uint8')
  bg=np.zeros((1,65),np.float64);fg=np.zeros((1,65),np.float64)
  cv2.grabCut(im,gc,None,bg,fg,4,cv2.GC_INIT_WITH_MASK)
  alpha=(np.where((gc==cv2.GC_FGD)|(gc==cv2.GC_PR_FGD),255,0)).astype('uint8')
  # preserve full interior exactly; edge feather anti-alias only
  alpha=np.maximum(alpha,(interior*255).astype('uint8'))
  alpha=cv2.GaussianBlur(alpha,(3,3),0.65)
  rgba=np.dstack([im,alpha]);ys,xs=np.where(alpha>1)
  left,right,top,bottom=max(0,xs.min()-2),min(w,xs.max()+3),max(0,ys.min()-2),min(h,ys.max()+3)
  cropped=Image.fromarray(rgba[top:bottom,left:right]);cropped.save(out/(nm+'-package.png'),optimize=True)
  print(nm,cropped.size,(left,top,right,bottom),'alpha nonzero',np.mean(alpha>1))
# checker preview
from PIL import ImageFont
canvas=Image.new('RGBA',(1200,820),'#f1f7f3')
for i,nm in enumerate(['mikozacid','hot-ice']):
 img=Image.open(out/(nm+'-package.png'))
 img.thumbnail((510,720),Image.Resampling.LANCZOS)
 bg=Image.new('RGBA',(580,780),'#e1eae3' if i==0 else '#d9f1f9')
 bg.alpha_composite(img,((580-img.width)//2,(780-img.height)//2))
 canvas.alpha_composite(bg,(i*610+10,20))
canvas.convert('RGB').save(out/'cutout-check.jpg',quality=90)
