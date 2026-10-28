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
