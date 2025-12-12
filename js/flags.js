// js/flags.js
document.addEventListener('DOMContentLoaded', () => {
  const nameText = document.getElementById('current-vegetable-name');
  const container = document.getElementById('vegetable-image-container');
  const prevBtn = document.getElementById('prev-vegetable');
  const nextBtn = document.getElementById('next-vegetable');
  const canvas = document.getElementById('drawing-canvas');
  const ctx = canvas.getContext('2d', { willReadFrequently: true });

  // exact labels that match filenames in your flags folder
  const items = [
    "India", "China", "United States", "Brazil", "Japan",
    "Turkiye", "Maxico", "Canada", "Russia", "France",
    "Europe Union", "Germany", "Greenland", "Italy", "Portugal",
    "Switzerland", "United Arab Emirates", "United Kingdom", "Israel", "Olympic"
  ];

  let index = 0;
  let isDrawing = false;
  let isRevealed = false;

  // use CDN if provided, otherwise site-relative path
  const CDN_BASE = (typeof CDN !== 'undefined' && CDN) ? CDN : '';
  const imageBasePath = CDN_BASE + 'assets/images/flags/';
  const audioBasePath = CDN_BASE + 'assets/audio/country/';
  const imageExt = '.png';
  const audioExt = '.mp3';

  // stroke-fallback variables (for CORS-blocked pixel reading)
  let allowPixelRead = true;
  let strokeAccumulator = 0;
  let lastPos = null;

  function setupCanvas() {
    const w = container.clientWidth || 300;
    const h = container.clientHeight || 200;

    // support devicePixelRatio if you want crisp lines (optional)
    const dpr = window.devicePixelRatio || 1;
    canvas.width = Math.max(1, Math.floor(w * dpr));
    canvas.height = Math.max(1, Math.floor(h * dpr));
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = 'rgba(0,0,0,0.75)';
    ctx.fillRect(0, 0, w, h);

    ctx.globalCompositeOperation = 'destination-out';
    ctx.lineWidth = Math.max(14, Math.round(w * 0.12));
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    // "SCRATCH HERE"
    ctx.globalCompositeOperation = 'source-over';
    ctx.fillStyle = 'rgba(255,255,255,0.9)';
    ctx.font = 'bold ' + Math.round(w * 0.09) + 'px Poppins, system-ui, Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('SCRATCH HERE', w / 2, h / 2);
    ctx.globalCompositeOperation = 'destination-out';

    // reset fallback counters
    strokeAccumulator = 0;
    lastPos = null;
    allowPixelRead = true;
    isRevealed = false;
    canvas.style.opacity = '1';
    canvas.style.transition = 'none';
  }

  function toCanvasPos(e) {
    const rect = canvas.getBoundingClientRect();
    return { x: e.clientX - rect.left, y: e.clientY - rect.top };
  }

  function start(e) {
    if (isRevealed) return;
    isDrawing = true;
    ctx.beginPath();
    const pos = e.touches ? toCanvasPos(e.touches[0]) : toCanvasPos(e);
    ctx.moveTo(pos.x, pos.y);
    lastPos = pos;
  }

  function move(e) {
    if (!isDrawing || isRevealed) return;
    e.preventDefault();
    const pos = e.touches ? toCanvasPos(e.touches[0]) : toCanvasPos(e);
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();

    if (!allowPixelRead && lastPos) {
      strokeAccumulator += Math.hypot(pos.x - lastPos.x, pos.y - lastPos.y);
      lastPos = pos;
    } else {
      lastPos = pos;
    }
  }

  function tryPixelReveal() {
    try {
      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const data = imageData.data;
      const total = data.length / 4;
      const sampleStep = Math.max(10, Math.floor(total / 30000)); // cap samples
      let transparent = 0, sampled = 0;
      for (let i = 3; i < data.length; i += 4 * sampleStep) {
        sampled++;
        if (data[i] < 50) transparent++;
      }
      if (sampled === 0) return 0;
      return (transparent / sampled) * 100;
    } catch (err) {
      console.warn('getImageData blocked — enabling stroke fallback', err);
      allowPixelRead = false;
      return null;
    }
  }

  function end() {
    if (!isDrawing) return;
    isDrawing = false;

    if (isRevealed) return;

    const p = tryPixelReveal();
    if (p !== null) {
      console.log('Pixel reveal %:', p.toFixed(2));
      if (p >= 50) reveal(true);
      return;
    }

    // stroke fallback threshold (tune as needed)
    const threshold = (canvas.width + canvas.height) * 1.5;
    console.log('Stroke fallback:', strokeAccumulator, 'threshold:', threshold);
    if (strokeAccumulator >= threshold) reveal(true);
  }

  function reveal(playAudio = false) {
    isRevealed = true;
    canvas.style.opacity = '0';
    canvas.style.transition = 'opacity 1s ease-out';
    if (playAudio) playAudioForCurrent();
  }

  // event hookup
  canvas.addEventListener('pointerdown', (e) => { start(e); canvas.setPointerCapture && canvas.setPointerCapture(e.pointerId); });
  canvas.addEventListener('pointermove', (e) => move(e));
  canvas.addEventListener('pointerup', (e) => { end(); canvas.releasePointerCapture && canvas.releasePointerCapture(e.pointerId); });
  canvas.addEventListener('pointercancel', end);
  canvas.addEventListener('pointerleave', end);

  // update display
  function updateDisplay() {
    const name = items[index];
    nameText.textContent = name;
    container.innerHTML = ''; // clear
    const img = document.createElement('img');

    // exact filename (preserve caps & spaces)
    const filename = name + imageExt; // e.g. "United States.png"
    const url = imageBasePath + encodeURIComponent(filename);
    console.log('Trying image URL ->', url);

    img.src = url;
    img.alt = 'Flag of ' + name;
    img.style.width = '100%';
    img.style.height = '100%';
    img.style.objectFit = 'contain';
    img.draggable = false;
    img.crossOrigin = 'anonymous'; // hint for CORS support

    img.onload = () => {
      console.log('Image loaded:', url);
      // append image then canvas (canvas overlay)
      container.appendChild(img);
      container.appendChild(canvas);
      setupCanvas();
      // optional: pre-check HEAD to diagnose server response
      fetch(url, { method: 'HEAD' }).then(r => console.log('HEAD status', r.status)).catch(() => {});
    };

    img.onerror = (err) => {
      console.error('Image failed:', url, err);
      // helpful on-screen message
      const msg = document.createElement('div');
      msg.style.position = 'absolute';
      msg.style.top = '50%';
      msg.style.left = '50%';
      msg.style.transform = 'translate(-50%,-50%)';
      msg.style.background = 'rgba(255,255,255,0.95)';
      msg.style.padding = '8px 12px';
      msg.style.borderRadius = '8px';
      msg.textContent = `Image not found: ${filename} — check ${imageBasePath}`;
      container.appendChild(msg);
      container.appendChild(canvas);
      setupCanvas();

      // Quick diagnostic log: try fetch to show status/cors error in console
      fetch(url).then(r => console.log('Fetch GET status', r.status)).catch(e => console.warn('Fetch GET error', e));
    };
  }

  function playAudioForCurrent() {
    const name = items[index];
    const audioFile = name + audioExt;
    const src = audioBasePath + encodeURIComponent(audioFile);
    console.log('Attempt audio ->', src);
    const a = new Audio(src);
    if (window.pauseBackgroundMusic) try { window.pauseBackgroundMusic(); } catch(e){}
    a.play().catch(e => console.warn('Audio play failed', e));
    a.onended = () => { if (window.resumeBackgroundMusic) try { window.resumeBackgroundMusic(); } catch(e){} };
  }

  prevBtn.addEventListener('click', () => { index = (index - 1 + items.length) % items.length; updateDisplay(); });
  nextBtn.addEventListener('click', () => { index = (index + 1) % items.length; updateDisplay(); });

  // initial start
  updateDisplay();
});
