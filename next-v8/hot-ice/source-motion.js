/* ZDRAVA v8.1 Motion Studio — fast, reversible JS. Native HTML is fully visible if CDNs fail. */
(()=>{
'use strict';
const doc=document;
const reduce=window.matchMedia('(prefers-reduced-motion: reduce)');
const mobile=window.matchMedia('(max-width: 550px)');
const desktop=window.matchMedia('(min-width: 1100px)');
const fine=window.matchMedia('(hover:hover) and (pointer:fine)');
const nav=doc.getElementById('nav');
const trigger=doc.getElementById('menu-trigger');
function closeMenu(){if(!nav||!trigger)return;nav.classList.remove('is-open');trigger.setAttribute('aria-expanded','false');trigger.setAttribute('aria-label','Открыть меню')}
if(nav&&trigger){trigger.addEventListener('click',()=>{const opened=nav.classList.toggle('is-open');trigger.setAttribute('aria-expanded',String(opened));trigger.setAttribute('aria-label',opened?'Закрыть меню':'Открыть меню')});nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));doc.addEventListener('keydown',e=>{if(e.key==='Escape')closeMenu()});doc.addEventListener('click',e=>{if(!nav.contains(e.target)&&!trigger.contains(e.target))closeMenu()})}
const progress=doc.querySelector('.progress span');const dock=doc.querySelector('.mobile-dock');const hero=doc.querySelector('.hero');const buy=doc.getElementById('buy');
let rafBusy=false;
function updateUI(){rafBusy=false;const max=doc.documentElement.scrollHeight-innerHeight;if(progress)progress.style.transform='scaleX('+(max>0?Math.min(1,Math.max(0,scrollY/max)):0)+')';if(dock){const h=hero?.getBoundingClientRect().bottom??400;const b=buy?.getBoundingClientRect().top??10000;dock.classList.toggle('is-visible',mobile.matches&&h<130&&b>innerHeight*.5)}}
function onScroll(){if(!rafBusy){rafBusy=true;requestAnimationFrame(updateUI)}}
window.addEventListener('scroll',onScroll,{passive:true});window.addEventListener('resize',onScroll,{passive:true});updateUI();
function track(name){try{window.dataLayer?.push({event:'zdrava_'+name});if(window.ZDRAVA_METRIKA_ID&&typeof window.ym==='function')window.ym(window.ZDRAVA_METRIKA_ID,'reachGoal',name)}catch(_) {}}
doc.addEventListener('click',e=>{const target=e.target.closest('[data-event]');if(target)track(target.dataset.event)});
if(buy&&'IntersectionObserver'in window){const observer=new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting)){track('buy_section');observer.disconnect()}},{threshold:.35});observer.observe(buy)}
const how=doc.querySelector('.how-content');const steps=Array.from(doc.querySelectorAll('.steps li'));const current=doc.querySelector('[data-current-step]');const meter=doc.querySelector('[data-story-progress]');const accent=doc.querySelector('.how-accent-wrap');
function setStep(index){if(!how||!steps.length)return;const active=Math.min(Math.max(index,0),steps.length-1);steps.forEach((el,i)=>el.classList.toggle('is-active',i===active));if(current)current.textContent=(active+1)+' / '+steps.length;if(meter)meter.style.transform='scaleX('+((active+1)/steps.length)+')';if(accent){accent.classList.toggle('is-step-2',active===1);accent.classList.toggle('is-step-3',active===2)}}
setStep(0);
if(reduce.matches)return;
const gsap=window.gsap;const ST=window.ScrollTrigger;
if(!gsap||!ST){ // Functional fallback. The page never relies on a CDN for content.
 if(fine.matches&&desktop.matches)setupPointer();
 return;
}
gsap.registerPlugin(ST);
// Extra movement on desktop only: no artificial smooth scrolling on phones or tablets.
if(desktop.matches&&fine.matches&&typeof window.Lenis==='function'){
 try{const lenis=new window.Lenis({duration:1.08,smoothWheel:true,autoRaf:false});lenis.on('scroll',ST.update);gsap.ticker.add(t=>lenis.raf(t*1000));gsap.ticker.lagSmoothing(0)}catch(_){/* use browser scrolling */}
}
// One opening sequence with editorial line masks and a precise product reveal.
const entry=gsap.timeline({defaults:{ease:'power3.out'}});
entry.from('.display .line',{yPercent:112,opacity:0,duration:1.22,stagger:.14,clearProps:'all'})
.from('.hero-copy .eyebrow',{y:12,opacity:0,duration:.7,clearProps:'all'},.10)
.from('.hero-copy .subtitle',{y:26,opacity:0,duration:.85,clearProps:'all'},.34)
.from('.hero-copy .actions',{y:22,opacity:0,duration:.85,clearProps:'all'},.50)
.from('.hero-note',{y:12,opacity:0,duration:.65,clearProps:'all'},.68)
.from('.art-product',{y:85,scale:.95,opacity:0,duration:1.45,ease:'expo.out',clearProps:'all'},.12)
.from('.art-prism',{x:-48,rotate:-16,opacity:0,duration:1.8,ease:'expo.out',clearProps:'all'},.10)
.from('.stage-seal,.art-small',{y:18,opacity:0,stagger:.14,duration:.8,clearProps:'all'},.78);
// Parallax only for decoration, never warp the packaging or lettering.
if(desktop.matches){
 const scrub={trigger:hero,start:'top top',end:'bottom top',scrub:1.4,invalidateOnRefresh:true};
 gsap.to('.art-prism',{y:-90,rotation:32,ease:'none',scrollTrigger:scrub});
 gsap.to('.art-orbit-line',{y:-47,rotation:-18,ease:'none',scrollTrigger:{...scrub,scrub:1.7}});
 gsap.to('.art-ring',{y:45,scale:1.09,ease:'none',scrollTrigger:{...scrub,scrub:1.1}});
 const aboutImage=doc.querySelector('.about-scene img');if(aboutImage)gsap.fromTo(aboutImage,{y:20},{y:-32,ease:'none',scrollTrigger:{trigger:'.about-scene',start:'top bottom',end:'bottom top',scrub:1.1}});
}
// Animated facts preserve their true value if JS is disabled.
if(desktop.matches){doc.querySelectorAll('.counter').forEach(el=>{const actual=Number(el.dataset.value);if(!Number.isFinite(actual))return;const state={n:actual};gsap.fromTo(state,{n:0},{n:actual,duration:1.12,ease:'power2.out',scrollTrigger:{trigger:el.closest('.how')||el,start:'top 78%',once:true},onUpdate:()=>{el.textContent=String(Math.round(state.n))},onComplete:()=>{el.textContent=String(actual)}})})}
// Repeated sections animate once, and never fade again when scrolling backward.
const selector='.section .kicker,.section .section-heading,.section .section-lead,.about-grid,.scenario,.ing,.steps li,.faq-list details,.buy .section-heading,.buy .actions';
const all=gsap.utils.toArray(selector);all.forEach(el=>{
 // Never fade/how-steps after activating our sticky scrollytelling.
 if(desktop.matches&&el.matches('.steps li'))return;
 gsap.from(el,{y:mobile.matches?13:35,autoAlpha:0,duration:mobile.matches?.58:.82,ease:'power2.out',clearProps:'all',scrollTrigger:{trigger:el,start:mobile.matches?'top 98%':'top 89%',once:true}});
});
// Desktop scroll narrative: one pin-like sticky product fact panel, three states.
if(desktop.matches&&how&&steps.length){
 how.classList.add('is-motion-story');setStep(0);
 steps.forEach((step,i)=>{ST.create({trigger:step,start:'top 60%',end:'bottom 43%',onEnter:()=>setStep(i),onEnterBack:()=>setStep(i)})});
 ST.create({trigger:how,start:'top 52%',end:'bottom 50%',onUpdate:self=>{ // left rail advances continuously, steps snap to readable positions
 if(meter){const phase=Math.min(1,Math.max(0,self.progress));meter.style.transform='scaleX('+(Math.max(1/steps.length,phase))+')'}
 }});
}
if(fine.matches&&desktop.matches)setupPointer();
function setupPointer(){
 const art=doc.querySelector('.hero-art');
 if(art){let scheduled=false;let px=0,py=0;art.addEventListener('pointermove',e=>{const r=art.getBoundingClientRect();px=(e.clientX-r.left-r.width/2)/r.width;py=(e.clientY-r.top-r.height/2)/r.height;if(!scheduled){scheduled=true;requestAnimationFrame(()=>{art.style.setProperty('--px',String(px));art.style.setProperty('--py',String(py));scheduled=false})}});art.addEventListener('pointerleave',()=>{art.style.setProperty('--px','0');art.style.setProperty('--py','0')})}
 if(hero){const onMove=e=>{const box=hero.getBoundingClientRect();hero.style.setProperty('--glow-x',((e.clientX-box.left)/box.width*100).toFixed(1)+'%');hero.style.setProperty('--glow-y',((e.clientY-box.top)/box.height*100).toFixed(1)+'%')};hero.addEventListener('pointermove',onMove,{passive:true})}
 doc.querySelectorAll('.scenario,.ing').forEach(card=>{card.addEventListener('pointermove',e=>{const r=card.getBoundingClientRect();card.style.setProperty('--mx',((e.clientX-r.left)/r.width*100).toFixed(1)+'%');card.style.setProperty('--my',((e.clientY-r.top)/r.height*100).toFixed(1)+'%')},{passive:true})});
}
})();


/* v8.2 Kinetic Editorial. Independent of GSAP, respects reduced motion. */
(()=>{
 'use strict';
 const doc=document,root=doc.documentElement;
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const fine=matchMedia('(hover:hover) and (pointer:fine)');
 const large=matchMedia('(min-width: 1100px)');
 const sec=[...doc.querySelectorAll('main > section[id]')].filter(x=>x.id!=='top');
 const rail=doc.querySelector('.chapter-rail');
 const hero=doc.querySelector('.hero');
 const buy=doc.getElementById('buy');
 const links=[...doc.querySelectorAll('.chapter-rail a')];
 const io='IntersectionObserver' in window;
 if(io){
  const draw=new IntersectionObserver((entries)=>{entries.forEach(({target,isIntersecting})=>{if(isIntersecting){target.classList.add('is-drawn');draw.unobserve(target)}})},{threshold:.2});
  doc.querySelectorAll('.about-scene').forEach(el=>draw.observe(el));
  const lines=new IntersectionObserver((entries)=>{entries.forEach(({target,isIntersecting})=>{if(isIntersecting){target.classList.add('is-inview');lines.unobserve(target)}})},{threshold:.08});
  doc.querySelectorAll('.section,.buy').forEach(el=>lines.observe(el));
 }else{doc.querySelectorAll('.about-scene').forEach(el=>el.classList.add('is-drawn'));doc.querySelectorAll('.section,.buy').forEach(el=>el.classList.add('is-inview'))}
 // Section rail: progressive enhancement for precise navigation and scroll orientation.
 let busy=false;
 function updateRail(){busy=false;if(!rail)return;
  const show=large.matches && (hero?.getBoundingClientRect().bottom??0)<110&&(buy?.getBoundingClientRect().top??0)>innerHeight*.36;
  rail.classList.toggle('is-visible',!!show);
  if(!show){links.forEach(a=>{a.classList.remove('is-active');a.removeAttribute('aria-current')});return}
  let active=sec[0]?.id;
  for(const s of sec){if(s.getBoundingClientRect().top<innerHeight*.47)active=s.id}
  links.forEach(a=>{const yes=a.getAttribute('href')==='#'+active;a.classList.toggle('is-active',yes);if(yes)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current')});
 }
 const onScroll=()=>{if(!busy){busy=true;requestAnimationFrame(updateRail)}};
 addEventListener('scroll',onScroll,{passive:true});addEventListener('resize',onScroll,{passive:true});updateRail();
 if(reduced.matches)return;
 // Kinetic affordance on fine-pointer desktops only; no layout-triggering transforms.
 if(fine.matches&&large.matches){
  doc.querySelectorAll('.scenario,.ing').forEach(card=>{
   let frame=0,tx=0,ty=0;
   card.addEventListener('pointermove',e=>{const r=card.getBoundingClientRect();tx=((e.clientX-r.left)/r.width-.5)*4;ty=((e.clientY-r.top)/r.height-.5)*-4;if(!frame)frame=requestAnimationFrame(()=>{frame=0;card.style.setProperty('--tilt-x',tx.toFixed(2)+'deg');card.style.setProperty('--tilt-y',ty.toFixed(2)+'deg')})},{passive:true});
   card.addEventListener('pointerleave',()=>{card.style.setProperty('--tilt-x','0deg');card.style.setProperty('--tilt-y','0deg')})
  });
  doc.querySelectorAll('.hero-copy .button,.buy .button').forEach(button=>{
   let frame=0,x=0,y=0;
   button.addEventListener('pointermove',e=>{const r=button.getBoundingClientRect();x=(e.clientX-r.left-r.width/2)*.075;y=(e.clientY-r.top-r.height/2)*.11;if(!frame)frame=requestAnimationFrame(()=>{frame=0;button.style.setProperty('--mag-x',x.toFixed(1)+'px');button.style.setProperty('--mag-y',y.toFixed(1)+'px')})},{passive:true});
   button.addEventListener('pointerleave',()=>{button.style.setProperty('--mag-x','0px');button.style.setProperty('--mag-y','0px')})
  });
 }
 // GSAP showcase layer: elegant scrubbing on the actual product, no bitmap edits.
 const gsap=window.gsap,ST=window.ScrollTrigger;
 if(gsap&&ST&&large.matches){
  gsap.to('.hero-art .kinetic-halo',{rotation:72,ease:'none',scrollTrigger:{trigger:hero,start:'top top',end:'bottom top',scrub:2}});
  gsap.to('.hero-art .art-product',{y:-25,rotation:1.2,ease:'none',scrollTrigger:{trigger:hero,start:'10% top',end:'bottom top',scrub:1.7}});
  gsap.utils.toArray('.scenario').forEach((el,i)=>{gsap.fromTo(el,{clipPath:'inset(0 0 14% 0 round 1px)'},{clipPath:'inset(0 0 0% 0 round 1px)',duration:.9,scrollTrigger:{trigger:el,start:'top 92%',once:true}})});
 }
})();

/* Product Story Engine 1.0: timeline is driven by actual scroll progress, not time. No external libraries. */
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
})();