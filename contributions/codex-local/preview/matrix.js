// Decorative, local-only animation; stops when hidden or reduced motion is requested.
const motionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
let matrixPaused = motionQuery.matches;
const scenes = [...document.querySelectorAll(".matrix-canvas")].map(canvas => ({
  canvas, ctx: canvas.getContext("2d"), columns: [], width: 0, height: 0
}));
function resizeMatrix(scene) {
  const rect = scene.canvas.parentElement.getBoundingClientRect();
  if (!rect.width || !rect.height) return;
  const ratio = Math.min(devicePixelRatio || 1, 2);
  scene.width = rect.width; scene.height = rect.height;
  scene.canvas.width = rect.width * ratio; scene.canvas.height = rect.height * ratio;
  scene.ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  scene.columns = Array.from({length: Math.ceil(rect.width/27)}, (_,i) => ({
    x: i*27+9, offset: (i*97)%(rect.height+270), speed: 32+(i%7)*8
  }));
}
function paintMatrix(scene, seconds) {
  const {ctx,width,height} = scene;
  ctx.clearRect(0,0,width,height);
  ctx.font = "15px monospace";
  const glyphs = "01TI-LEX{}<>/+=*";
  const gap = Math.min(width, Math.max(350,width*.4));
  for (const [i,col] of scene.columns.entries()) {
    if (col.x > (width-gap)/2 && col.x < (width+gap)/2) continue;
    const head = (col.offset+seconds*col.speed)%(height+270);
    for (let row=0;row<13;row++) {
      const y=head-row*21;
      if (y<0||y>height) continue;
      ctx.fillStyle = row===0 ? "rgba(170,255,189,.85)" : "rgba(25,190,86,"+((1-row/13)*.6)+")";
      ctx.fillText(glyphs[(i+row+Math.floor(seconds*2))%glyphs.length],col.x,y);
    }
  }
}
let previous=0, elapsed=0;
function frame(now) {
  if (now-previous>=65) {
    if (!matrixPaused && !document.hidden) elapsed+=Math.min((now-previous)/1000,.12);
    previous=now;
    for (const scene of scenes) {
      if (!scene.canvas.parentElement.hidden) {
        if (!scene.width) resizeMatrix(scene);
        paintMatrix(scene,elapsed);
      }
    }
  }
  requestAnimationFrame(frame);
}
function updateMotionButtons() {
  document.querySelectorAll(".motion-control").forEach(button=>{
    button.textContent=matrixPaused?"Animer la pluie Matrix":"Suspendre la pluie Matrix";
    button.setAttribute("aria-pressed",String(matrixPaused));
  });
}
document.querySelectorAll(".motion-control").forEach(button=>button.onclick=()=>{
  matrixPaused=!matrixPaused; updateMotionButtons();
});
motionQuery.addEventListener("change",event=>{matrixPaused=event.matches;updateMotionButtons()});
window.addEventListener("resize",()=>scenes.forEach(resizeMatrix));
function showLogin() {
  document.querySelector("#boot").hidden=true;
  document.querySelector("#login").hidden=false;
  scenes.forEach(resizeMatrix);
}
document.querySelector("#skip-boot").onclick=()=>{clearTimeout(bootTimer);showLogin()};
const bootTimer=setTimeout(showLogin,motionQuery.matches?0:2800);
updateMotionButtons();
requestAnimationFrame(frame);
