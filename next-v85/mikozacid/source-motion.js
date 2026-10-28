/* Progressive enhancement: content, links, and details remain usable without JS. */
(()=>{
 const doc=document;
 const reduce=window.matchMedia('(prefers-reduced-motion: reduce)');
 const mobile=window.matchMedia('(max-width: 550px)');
 const nav=doc.getElementById('nav');const trigger=doc.getElementById('menu-trigger');
 if(trigger&&nav){trigger.addEventListener('click',()=>{const open=nav.classList.toggle('is-open');trigger.setAttribute('aria-expanded',String(open));trigger.setAttribute('aria-label',open?'Закрыть меню':'Открыть меню')});nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{nav.classList.remove('is-open');trigger.setAttribute('aria-expanded','false')}));}
 const progress=doc.querySelector('.progress span');const dock=doc.querySelector('.mobile-dock');const hero=doc.querySelector('.hero');const buy=doc.getElementById('buy');
 const update=()=>{const total=doc.documentElement.scrollHeight-innerHeight;if(progress){progress.style.transform='scaleX('+(total?Math.min(1,scrollY/total):0)+')';}if(dock){const h=hero?hero.getBoundingClientRect():{bottom:400};const b=buy?buy.getBoundingClientRect():{top:10000};dock.classList.toggle('is-visible',mobile.matches&&h.bottom<130&&b.top>innerHeight*.5);}};
 window.addEventListener('scroll',update,{passive:true});window.addEventListener('resize',update,{passive:true});update();
 // Data attributes allow Yandex.Metrika and GA4 hooks after counters are configured.
 function track(name){try{window.dataLayer?.push({event:'zdrava_'+name});if(window.ZDRAVA_METRIKA_ID&&typeof window.ym==='function')window.ym(window.ZDRAVA_METRIKA_ID,'reachGoal',name);}catch(e){}}
 doc.addEventListener('click',e=>{const a=e.target.closest('[data-event]');if(a)track(a.dataset.event);});
 const target=doc.getElementById('buy');if(target&&'IntersectionObserver'in window){const o=new IntersectionObserver(es=>{if(es.some(e=>e.isIntersecting)){track('buy_section');o.disconnect()}},{threshold:.35});o.observe(target)}
 // Smooth scroll + entrance motion only on capable devices; native scroll works without CDNs.
 if(reduce.matches)return;
 if(!mobile.matches&&typeof window.Lenis==='function'){
  try{const lenis=new window.Lenis({duration:1.12,smoothWheel:true,touchMultiplier:1.1});if(window.gsap&&window.ScrollTrigger){lenis.on('scroll',window.ScrollTrigger.update);window.gsap.ticker.add(t=>lenis.raf(t*1000));window.gsap.ticker.lagSmoothing(0);}else{const raf=t=>{lenis.raf(t);requestAnimationFrame(raf)};requestAnimationFrame(raf)}}catch(e){}
 }
 const gsap=window.gsap,st=window.ScrollTrigger;
 if(gsap&&st){
  gsap.registerPlugin(st);
  gsap.from('.display .line',{y:45,autoAlpha:0,duration:.9,ease:'power3.out',stagger:.13,clearProps:'all'});
  gsap.from('.hero-copy .subtitle,.hero-copy .actions,.hero-note',{y:20,autoAlpha:0,duration:.8,ease:'power2.out',stagger:.13,delay:.36,clearProps:'all'});
  gsap.from('.art-product',{y:45,autoAlpha:0,scale:.94,duration:1.15,ease:'power3.out',clearProps:'all'});
  // Accurate numeric facts animate only once on desktop; HTML values remain correct without JS.
  if(!mobile.matches)doc.querySelectorAll('.counter').forEach(el=>{const actual=Number(el.dataset.value);const state={v:0};if(!Number.isFinite(actual))return;gsap.to(state,{v:actual,duration:.85,ease:'power1.out',scrollTrigger:el.closest('.how')?{trigger:el.closest('.how'),start:'top 78%',once:true}:undefined,onUpdate:()=>{el.textContent=String(Math.round(state.v))},onComplete:()=>{el.textContent=String(actual)}})});

  doc.querySelectorAll('.section .kicker,.section .section-heading,.section .section-lead,.scenario,.ing,.steps li').forEach((el,i)=>{gsap.from(el,{scrollTrigger:{trigger:el,start:'top 90%',once:true},y:24,autoAlpha:0,duration:.7,ease:'power2.out',clearProps:'all'})});
 }else if('IntersectionObserver'in window){
  const obs=new IntersectionObserver(es=>{es.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('is-in');obs.unobserve(entry.target)}})},{threshold:.08});
  doc.querySelectorAll('.scenario,.ing,.steps li').forEach(el=>{el.style.transition='opacity .55s ease,transform .55s ease';obs.observe(el);el.classList.add('is-in')});
 }
 if(window.matchMedia('(hover:hover) and (pointer:fine)').matches){const art=doc.querySelector('.hero-art');art?.addEventListener('pointermove',e=>{const r=art.getBoundingClientRect();art.style.setProperty('--px',String((e.clientX-r.left-r.width/2)/r.width));art.style.setProperty('--py',String((e.clientY-r.top-r.height/2)/r.height));});art?.addEventListener('pointerleave',()=>{art.style.setProperty('--px','0');art.style.setProperty('--py','0')});}
})();