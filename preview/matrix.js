// Pluie TI-LEX derrière le bureau : décor seulement, jamais un élément d'interface.
// Aucune donnée, aucun réseau. L'animation s'arrête quand l'onglet passe en arrière-plan
// et reste sur une image fixe si le système demande un mouvement réduit.
const canvas = document.querySelector("#matrix");
if (canvas) {
  const context = canvas.getContext("2d");
  const GLYPHS = "TILEX0123456789ABCDEFGHJKLMNPQRSTUVWXYZ/\\|<>[]{}=+*#";
  const SIZE = 16;
  const calm = matchMedia("(prefers-reduced-motion: reduce)");
  let columns = [], width = 0, height = 0, running = false, last = 0;

  const glyph = () => GLYPHS[Math.floor(Math.random() * GLYPHS.length)];
  const speed = () => 0.35 + Math.random() * 0.85;

  function draw(still) {
    context.fillStyle = "rgba(8,8,11,.14)";
    context.fillRect(0, 0, width, height);
    for (let index = 0; index < columns.length; index++) {
      const column = columns[index], x = index * SIZE;
      context.fillStyle = "#ff8a24";
      context.fillText(glyph(), x, column.y);
      context.fillStyle = "rgba(180,255,57,.5)";
      context.fillText(glyph(), x, column.y - SIZE);
      if (still) continue;
      column.y += column.speed * SIZE;
      if (column.y > height + SIZE) { column.y = -SIZE * Math.random() * 10; column.speed = speed() }
    }
  }

  function resize() {
    const ratio = Math.min(devicePixelRatio || 1, 2);
    width = canvas.clientWidth;
    height = canvas.clientHeight;
    canvas.width = Math.max(1, Math.round(width * ratio));
    canvas.height = Math.max(1, Math.round(height * ratio));
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    context.font = `600 ${SIZE}px Consolas, "DejaVu Sans Mono", monospace`;
    context.textBaseline = "top";
    const wanted = Math.ceil(width / SIZE);
    columns = Array.from({length: wanted}, (_, index) =>
      columns[index] || {y: Math.random() * height, speed: speed()});
    context.fillStyle = "#08080b";
    context.fillRect(0, 0, width, height);
    draw(true);
  }

  function loop(time) {
    if (!running) return;
    if (time - last > 55) { last = time; draw(false) }
    requestAnimationFrame(loop);
  }

  function start() { if (!running && !calm.matches) { running = true; last = 0; requestAnimationFrame(loop) } }
  function stop() { running = false }

  addEventListener("resize", resize);
  document.addEventListener("visibilitychange", () => document.hidden ? stop() : start());
  if (calm.addEventListener) calm.addEventListener("change", () => calm.matches ? stop() : start());
  resize();
  start();
}
