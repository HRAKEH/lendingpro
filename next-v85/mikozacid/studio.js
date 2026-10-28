/* ZDRAVA v8.5: single purposeful scroll-directed studio sequence. No animation libraries required. */
(()=>{'use strict';
 const d=document,reduced=matchMedia('(prefers-reduced-motion: reduce)'),mobile=matchMedia('(max-width: 820px)');
 const nav=d.getElementById('nav'),trigger=d.getElementById('menu-trigger');
 trigger?.addEventListener('click',()=>{const open=nav.classList.toggle('is-open');trigger.setAttribute('aria-expanded',String(open));trigger.setAttribute('aria-label',open?'Закрыть меню':'Открыть меню')});
 nav?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('is-open');trigger?.setAttribute('aria-expanded','false')}));
 const hero=d.querySelector('.hero'),buy=d.getElementById('buy'),dock=d.querySelector('.mobile-dock');
 const stage=d.querySelector('[data-film]'); const panels=[...(stage?.querySelectorAll('.film__panel')||[])];
 const product=stage?.querySelector('.film__product');let current=0,active=0,raf=0;
 const clamp=n=>Math.max(0,Math.min(1,n));
 function activate(i){if(i===active)return;active=i;panels.forEach((p,j)=>{p.classList.toggle('is-current',i===j);p.setAttribute('aria-hidden',String(i!==j))})}
 function render(){raf=0;
  if(dock){dock.classList.toggle('is-visible',matchMedia('(max-width:550px)').matches&&(hero?.getBoundingClientRect().bottom??999)<130&&(buy?.getBoundingClientRect().top??999)>innerHeight*.5)}
  if(!stage || !product || reduced.matches || mobile.matches)return;
  const r=stage.getBoundingClientRect(),p=clamp(-r.top/Math.max(1,r.height-innerHeight));
  const i=Math.min(2,Math.floor(p*3.001));activate(i);
  current+=(p-current)*.19;
  const rotation=4*Math.sin(current*Math.PI*2-.4),scale=1+Math.sin(current*Math.PI)*.095;
  stage.style.setProperty('--film-p',current.toFixed(3));
  product.style.setProperty('--film-r',rotation.toFixed(2)+'deg');
  product.style.setProperty('--film-y',(-35*current+15).toFixed(1)+'px');
  product.style.setProperty('--film-scale',scale.toFixed(3));
  if(Math.abs(p-current)>.002)raf=requestAnimationFrame(render);
 }
 const schedule=()=>{if(!raf)raf=requestAnimationFrame(render)};
 addEventListener('scroll',schedule,{passive:true});addEventListener('resize',schedule,{passive:true});
 reduced.addEventListener?.('change',schedule);mobile.addEventListener?.('change',()=>{activate(0);current=0;product?.style.removeProperty('--film-r');product?.style.removeProperty('--film-y');product?.style.removeProperty('--film-scale');schedule()});schedule();
 function track(name){try{window.dataLayer?.push({event:'zdrava_'+name});if(window.ZDRAVA_METRIKA_ID&&typeof window.ym==='function')window.ym(window.ZDRAVA_METRIKA_ID,'reachGoal',name)}catch(_){}}
 d.addEventListener('click',e=>{const a=e.target.closest('[data-event]');if(a)track(a.dataset.event)});
 const full=d.querySelector('.expand');full?.addEventListener('toggle',()=>{if(full.open)track('full_composition_open')});
 if(buy&&'IntersectionObserver'in window){const ob=new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting)){track('buy_section');ob.disconnect()}},{threshold:.35});ob.observe(buy)}
})();
