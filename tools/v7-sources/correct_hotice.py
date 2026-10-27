from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import numpy as np, os, zipfile, shutil
from pathlib import Path
src=Path('/mnt/data/lendingpro-trend-final/hot-ice-package.png')
out=Path('/mnt/data/hot-ice-package-color-corrected.png')
im=Image.open(src).convert('RGBA')
a=np.array(im,dtype=np.float32)
orig=a[:,:,:3].copy()
alpha=a[:,:,3]
H,W=alpha.shape
r,g,b=orig[:,:,0],orig[:,:,1],orig[:,:,2]
Y=(.22*r+.72*g+.06*b)
chrom=np.maximum(np.maximum(r,g),b)-np.minimum(np.minimum(r,g),b)
y=np.indices((H,W))[0]
# Brighten and neutralize lilac-grey cast in pale body, preserving black typography.
white_mask=(np.clip((Y-124)/75,0,1) * np.clip((45-chrom)/33,0,1) *
            np.clip((y-160)/33,0,1) * np.clip((733-y)/50,0,1) * (alpha/255.0))
# luminance-dependent white material, slightly cool neutral (rather than purple)
light=Y+(.40*(255-Y))
target=np.stack([light+1,light+3,light+6],axis=2)
corrected=orig*(1-white_mask[:,:,None])+target*white_mask[:,:,None]
# Make blue ink and print band a little richer without changing their contours.
# Dominant blue pixels: blue >= green+20 and green >= red+22, plus chroma.
rr,gg,bb=corrected[:,:,0],corrected[:,:,1],corrected[:,:,2]
blue_mask=np.clip((gg-rr-12)/26,0,1)*np.clip((bb-gg-12)/30,0,1)*np.clip((np.maximum(bb,gg)-65)/70,0,1)*(alpha/255.)
# Reduce purple and intensify cyan-blue, subtle to protect anti-aliasing.
blue=np.stack([rr*.96,gg*1.055,bb*1.05],axis=2)
corrected=corrected*(1-blue_mask[:,:,None]*.7)+blue*(blue_mask[:,:,None]*.7)
# Cap retains original shaded plastic; slight cooling rather than flattening.
cap_mask=np.clip((y-729)/65,0,1)*(alpha/255.)*.38
cap=np.stack([corrected[:,:,0]*.99+2,corrected[:,:,1]*1.012+2,corrected[:,:,2]*1.025+2],axis=2)
corrected=corrected*(1-cap_mask[:,:,None])+cap*cap_mask[:,:,None]
a[:,:,:3]=np.clip(corrected,0,255)
result=Image.fromarray(a.astype(np.uint8),'RGBA')
result.save(out,optimize=True)
# Show the difference over approved pale blue canvas while keeping a transparent export.
bg=(242,248,253,255)
def sample_tube(tube,base):
    canvas=Image.new('RGBA',(600,1000),base)
    new=tube.copy();new.thumbnail((420,890),Image.Resampling.LANCZOS)
    canvas.alpha_composite(new,((600-new.width)//2,(1000-new.height)//2))
    return canvas.convert('RGB')
before=sample_tube(im,bg)
after=sample_tube(result,bg)
comp=Image.new('RGB',(1200,1000),'white');comp.paste(before,(0,0));comp.paste(after,(600,0))
comp.save('/mnt/data/hot-ice-before-after.jpg',quality=93,optimize=True)
# Repack original ZIP byte-for-byte unchanged except hot-ice product.png.
orig_zip=Path('/mnt/data/lendingpro-timeweb-v4-with-original-packages.zip')
new_zip=Path('/mnt/data/lendingpro-timeweb-v5-hot-ice-color-corrected.zip')
with zipfile.ZipFile(orig_zip,'r') as inp, zipfile.ZipFile(new_zip,'w') as res:
    for entry in inp.infolist():
        bs=out.read_bytes() if entry.filename=='hot-ice/assets/product.png' else inp.read(entry.filename)
        res.writestr(entry,bs)
print('Corrected',out,out.stat().st_size)
print('Archive',new_zip,new_zip.stat().st_size)
with zipfile.ZipFile(new_zip) as z:
 print('Zip test',z.testzip(),'files',len(z.namelist()))
