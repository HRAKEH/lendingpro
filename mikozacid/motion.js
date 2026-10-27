"use strict";
/* LandingPro v7: respectful motion, native JS, no third-party animation libraries.
   Images retain their original pixels and aspect ratio. */
(() => {
 const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
 const fine = window.matchMedia('(hover: hover) and (pointer: fine)');
 const root = document.documentElement;
 const header = document.querySelector('.site-header');
 const stage = document.querySelector('.photo-stage');
 const glass = stage?.querySelector('.glass-float');
 const interlude = document.querySelector('.motion-interlude__frame');
 const hero = document.querySelector('.hero');
 const buy = document.querySelector('.purchase-section');
 const dock = document.querySelector('.mobile-buy-dock');
 const clamp=(v,min,max)=>Math.min(max,Math.max(min,v));
 let scheduled=false;
 function onScroll(){
  scheduled=false;
  const doc=document.documentElement;
  const range=Math.max(1, doc.scrollHeight-innerHeight);
  root.style.setProperty('--scroll-progress',(scrollY/range).toFixed(4));
  header?.classList.toggle('is-scrolled',scrollY>25);
  if (dock){
   const heroOut=hero?.getBoundingClientRect().bottom<25;
   const buyRect=buy?.getBoundingClientRect();
   const buyShown=!!buyRect && buyRect.top<innerHeight && buyRect.bottom>0;
   dock.classList.toggle('is-active',Boolean(heroOut && !buyShown && innerWidth<=800));
  }
  if(!reduce.matches&&interlude){
   const b=interlude.getBoundingClientRect();
   if(b.top<innerHeight+70&&b.bottom>-70){
    const progress=clamp((innerHeight-b.top)/(innerHeight+b.height),0,1);
    interlude.style.setProperty('--interlude-img-y',`${((progress-.5)*-29).toFixed(2)}px`);
    interlude.style.setProperty('--interlude-parallax',`${((progress-.5)*16).toFixed(2)}px`);
   }
  }
 }
 function scrollTick(){if(!scheduled){scheduled=true;requestAnimationFrame(onScroll)}}
 addEventListener('scroll',scrollTick,{passive:true});addEventListener('resize',scrollTick,{passive:true});scrollTick();
 function enablePointer(){
  if(!fine.matches||reduce.matches||!stage)return;
  const move=e=>{
   const b=stage.getBoundingClientRect(),nx=clamp((e.clientX-b.left)/b.width,0,1),ny=clamp((e.clientY-b.top)/b.height,0,1);
   stage.style.setProperty('--light-x',(nx*100).toFixed(1)+'%');stage.style.setProperty('--light-y',(ny*100).toFixed(1)+'%');
   stage.style.setProperty('--sculpt-x',((nx-.5)*13).toFixed(2)+'px');stage.style.setProperty('--sculpt-y',((ny-.5)*9).toFixed(2)+'px');
   if(glass){glass.style.setProperty('--float-x',((nx-.5)*-5).toFixed(2)+'px');glass.style.setProperty('--float-y',((ny-.5)*-5).toFixed(2)+'px')}
  };
  stage.addEventListener('pointermove',move,{passive:true});
  stage.addEventListener('pointerleave',()=>{
   stage.style.setProperty('--light-x','50%');stage.style.setProperty('--light-y','40%');
   stage.style.setProperty('--sculpt-x','0px');stage.style.setProperty('--sculpt-y','0px');
   if(glass){glass.style.setProperty('--float-x','0px');glass.style.setProperty('--float-y','0px')}
  },{passive:true});
  for (const btn of document.querySelectorAll('.market-actions .btn,.purchase-links .btn')) {
   btn.addEventListener('pointermove',e=>{
    const b=btn.getBoundingClientRect(),x=(e.clientX-b.left)/b.width-.5,y=(e.clientY-b.top)/b.height-.5;
    btn.style.setProperty('--btn-x',(x*4).toFixed(2)+'px');btn.style.setProperty('--btn-y',(y*3).toFixed(2)+'px');
   },{passive:true});
   btn.addEventListener('pointerleave',()=>{btn.style.setProperty('--btn-x','0px');btn.style.setProperty('--btn-y','0px')},{passive:true});
  }
  for(const box of document.querySelectorAll('.ingredient')){
   box.addEventListener('pointermove',e=>{
    const b=box.getBoundingClientRect();box.style.setProperty('--spot-x',((e.clientX-b.left)/b.width*100).toFixed(1)+'%');box.style.setProperty('--spot-y',(e.clientY-b.top).toFixed(1)+'px');
   },{passive:true});
  }
 }
 enablePointer();
 reduce.addEventListener?.('change',()=>{
  if(reduce.matches){for(const p of [stage,interlude,glass]){p?.style.removeProperty('--sculpt-x');p?.style.removeProperty('--sculpt-y');p?.style.removeProperty('--interlude-img-y');p?.style.removeProperty('--float-x');p?.style.removeProperty('--float-y')}}
 });
})();
