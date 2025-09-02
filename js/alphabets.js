document.addEventListener('DOMContentLoaded', () => {
  const currentLetterText = document.getElementById('current-letter-text');
  const letterImageContainer = document.getElementById('letter-image-container');
  const prevLetterButton = document.getElementById('prev-letter');
  const nextLetterButton = document.getElementById('next-letter');
  const canvas = document.getElementById('drawing-canvas');

  if (!currentLetterText || !letterImageContainer || !canvas) {
    console.error('Missing required DOM elements (current-letter-text / letter-image-container / drawing-canvas).');
    return;
  }

  const ctx = canvas.getContext('2d', { willReadFrequently: true });
  const DPR = window.devicePixelRatio || 1;

  const alphabets = Array.from({ length: 26 }, (_, i) => String.fromCharCode(65 + i));
  let currentIndex = 0;
  let isDrawing = false;
  let isRevealed = false;

  // CDN fallback: if you don't set global CDN, use empty string (local relative paths)
  const CDN_BASE = (typeof CDN !== 'undefined' && CDN) ? CDN : '';
  const imageBasePath = CDN_BASE + 'assets/images/alphabets/';
  const audioBasePath = CDN_BASE + 'assets/audio/alphabets/';
  const audioFormat = '.mp3?v=2'; // keep for cache-busting if you use a CDN
  const imageFormats = ['.jpeg', '.png', '.webp']; // try these in order

  const exampleWords = {
    A: 'Apple', B: 'Ball', C: 'Cat', D: 'Dog', E: 'Elephant', F: 'Fish', G: 'Goat',
    H: 'Hen', I: 'Ice cream', J: 'Joker', K: 'Kite', L: 'Lion', M: 'Mango', N: 'Nest',
    O: 'Owl', P: 'Parrot', Q: 'Queen', R: 'Rose', S: 'Sun', T: 'Tiger',
    U: 'Umbrella', V: 'Van', W: 'Watch', X: 'Xmas tree', Y: 'Yak', Z: 'Zebra'
  };

  // Stroke-based fallback metrics (used if getImageData is blocked)
  let strokeCount = 0;
  let strokeLength = 0;
  let lastPos = null;

  function setupCanvas(widthCssPx, heightCssPx) {
    // position canvas as overlay
    if (getComputedStyle(letterImageContainer).position === 'static') {
      letterImageContainer.style.position = 'relative';
    }
    canvas.style.position = 'absolute';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.touchAction = 'none';

    // Set actual pixel size using devicePixelRatio for crisp drawing
    canvas.width = Math.round(widthCssPx * DPR);
    canvas.height = Math.round(heightCssPx * DPR);
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0); // scale so drawing coordinates are CSS pixels

    // Clear & draw dark overlay
    ctx.clearRect(0, 0, widthCssPx, heightCssPx);
    ctx.globalCompositeOperation = 'source-over';
    ctx.fillStyle = 'rgba(0,0,0,0.75)';
    ctx.fillRect(0, 0, widthCssPx, heightCssPx);

    // Prepare eraser stroke
    ctx.globalCompositeOperation = 'destination-out';
    ctx.lineWidth = Math.max(8, widthCssPx * 0.12);
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.strokeStyle = 'rgba(0,0,0,1)';

    // Draw "SCRATCH HERE" overlay text then switch back to eraser mode
    ctx.globalCompositeOperation = 'source-over';
    ctx.fillStyle = 'rgba(255,255,255,0.9)';
    ctx.font = 'bold ' + Math.round(widthCssPx * 0.08) + 'px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('SCRATCH HERE', widthCssPx / 2, heightCssPx / 2);
    ctx.globalCompositeOperation = 'destination-out';

    // reset reveal metrics
    isRevealed = false;
    strokeCount = 0;
    strokeLength = 0;
    lastPos = null;
    canvas.style.opacity = '1';
    canvas.style.transition = 'none';
  }

  function getPosFromEvent(e) {
    const rect = canvas.getBoundingClientRect();
    if (e.touches && e.touches.length) {
      return { x: e.touches[0].clientX - rect.left, y: e.touches[0].clientY - rect.top };
    } else if (e.changedTouches && e.changedTouches.length) {
      return { x: e.changedTouches[0].clientX - rect.left, y: e.changedTouches[0].clientY - rect.top };
    }
    return { x: e.clientX - rect.left, y: e.clientY - rect.top };
  }

  function startDrawing(e) {
    if (isRevealed) return;
    isDrawing = true;
    ctx.beginPath();
    const pos = getPosFromEvent(e);
    ctx.moveTo(pos.x, pos.y);
    lastPos = pos;
    strokeCount++;
    e.preventDefault();
  }

  function draw(e) {
    if (!isDrawing || isRevealed) return;
    e.preventDefault();
    const pos = getPosFromEvent(e);
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
    if (lastPos) {
      const dx = pos.x - lastPos.x, dy = pos.y - lastPos.y;
      strokeLength += Math.sqrt(dx * dx + dy * dy);
      lastPos = pos;
    }
  }

  function stopDrawing() {
    if (!isDrawing) return;
    isDrawing = false;
    lastPos = null;
    checkRevealProgressSafe();
  }

  function checkRevealProgressSafe() {
    // Try the reliable pixel-check (may throw if canvas is tainted)
    try {
      const w = canvas.width; // pixels
      const h = canvas.height;
      const imageData = ctx.getImageData(0, 0, w, h); // may throw SecurityError if tainted
      const data = imageData.data;
      let transparentSamples = 0;
      const totalPixels = data.length / 4;
      const sampleStep = 60; // sample less for performance
      for (let i = 3; i < data.length; i += 4 * sampleStep) {
        if (data[i] < 50) transparentSamples++;
      }
      const sampledTotal = Math.max(1, Math.floor(totalPixels / sampleStep));
      const revealPercentage = (transparentSamples / sampledTotal) * 100;
      if (revealPercentage >= 30) {
        reveal();
        return;
      }
    } catch (err) {
      // likely security/cors taint or other error — fall back
      console.warn('getImageData failed (canvas may be tainted). Using stroke fallback.', err);
    }

    // Stroke-based fallback — heuristics tuned for common sizes
    const strokeDistanceThreshold = Math.max(600, canvas.width / DPR * 40); // css px based estimate
    const strokeCountThreshold = 12;
    if (strokeCount >= strokeCountThreshold || strokeLength >= strokeDistanceThreshold) {
      reveal();
    }
  }

  function reveal() {
    if (isRevealed) return;
    isRevealed = true;
    canvas.style.transition = 'opacity 0.9s ease-out';
    canvas.style.opacity = '0';
    playLetterAudio();
  }

  // Event listeners: use pointer events when available, else mouse+touch
  if (window.PointerEvent) {
    canvas.addEventListener('pointerdown', startDrawing);
    canvas.addEventListener('pointermove', draw);
    canvas.addEventListener('pointerup', stopDrawing);
    canvas.addEventListener('pointercancel', stopDrawing);
    canvas.addEventListener('pointerleave', stopDrawing);
  } else {
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseleave', stopDrawing);
    canvas.addEventListener('touchstart', startDrawing, { passive: false });
    canvas.addEventListener('touchmove', draw, { passive: false });
    canvas.addEventListener('touchend', stopDrawing);
    canvas.addEventListener('touchcancel', stopDrawing);
  }

  // Load image with fallback formats and crossOrigin to avoid tainting (requires server CORS)
  function loadImageWithFallback(letter) {
    return new Promise(async (resolve, reject) => {
      for (const fmt of imageFormats) {
        const url = imageBasePath + letter + fmt;
        const img = new Image();
        img.crossOrigin = 'anonymous'; // require the server to send Access-Control-Allow-Origin: *
        img.decoding = 'async';
        const p = new Promise((res, rej) => {
          img.onload = () => res(img);
          img.onerror = () => rej(url);
        });
        img.src = url;
        try {
          const loaded = await p;
          console.log('Loaded image:', url);
          resolve(loaded);
          return;
        } catch (errUrl) {
          console.warn('Image failed to load:', errUrl);
        }
      }
      reject(new Error('All image formats failed'));
    });
  }

  async function updateLetterDisplay() {
    const currentLetter = alphabets[currentIndex];
    currentLetterText.textContent = currentLetter;
    letterImageContainer.innerHTML = '';

    try {
      const img = await loadImageWithFallback(currentLetter);
      img.alt = `Letter ${currentLetter}: ${exampleWords[currentLetter]} - Learn ABC letters with Teachings.AI`;
      img.loading = 'lazy';
      // ensure image fills container
      img.style.display = 'block';
      img.style.width = '100%';
      img.style.height = 'auto';
      letterImageContainer.appendChild(img);
      letterImageContainer.appendChild(canvas);
      // Use the container's CSS size for the canvas; image may still be loading layout, so read container size
      const rect = letterImageContainer.getBoundingClientRect();
      setupCanvas(rect.width, rect.height);
      canvas.setAttribute('aria-label', `Scratch card for letter ${currentLetter}`);

    } catch (err) {
      console.error('Could not load image for', currentLetter, err);
      const fallbackText = document.createElement('p');
      fallbackText.textContent = `Image for ${currentLetter} not found. Add ${currentLetter}.[jpeg|png|webp] to assets/images/alphabets/`;
      letterImageContainer.appendChild(fallbackText);
      letterImageContainer.appendChild(canvas);
      const rect = letterImageContainer.getBoundingClientRect();
      setupCanvas(rect.width || 300, rect.height || 200);
    }

    // Add structured data (SEO)
    const oldScript = document.getElementById('ld-json-letter');
    if (oldScript) oldScript.remove();
    const ldJson = {
      "@context": "https://schema.org",
      "@type": "LearningResource",
      "name": `Learn letter ${currentLetter} - ABC for kids`,
      "educationalLevel": "Preschool",
      "learningResourceType": "Interactive Scratch Card",
      "inLanguage": "en",
      "url": window.location.href,
      "description": `Interactive ABC learning for kids. Letter ${currentLetter} with image, pronunciation and example word: ${exampleWords[currentLetter]}.`
    };
    const script = document.createElement('script');
    script.id = 'ld-json-letter';
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(ldJson);
    document.head.appendChild(script);

    console.log('Displaying letter:', currentLetter);
  }

  function playLetterAudio() {
    const currentLetter = alphabets[currentIndex];
    const audioSrc = audioBasePath + currentLetter + audioFormat;
    console.log('Playing audio:', audioSrc);
    const audio = new Audio(audioSrc);
    audio.setAttribute('aria-label', `Pronunciation of letter ${currentLetter}: ${exampleWords[currentLetter]}`);

    const hiddenText = document.createElement('span');
    hiddenText.style.position = 'absolute';
    hiddenText.style.left = '-9999px';
    hiddenText.textContent = `Audio pronunciation for letter ${currentLetter}: ${exampleWords[currentLetter]}`;
    document.body.appendChild(hiddenText);

    if (window.pauseBackgroundMusic) window.pauseBackgroundMusic();
    audio.play().catch(e => console.error('Error playing audio for ' + currentLetter, e));

    audio.onended = () => {
      document.body.removeChild(hiddenText);
      if (window.resumeBackgroundMusic) window.resumeBackgroundMusic();
    };

    // Add Audio structured data
    const oldAudioScript = document.getElementById('ld-json-audio');
    if (oldAudioScript) oldAudioScript.remove();
    const audioLdJson = {
      "@context": "https://schema.org",
      "@type": "AudioObject",
      "name": `Pronunciation of letter ${currentLetter}`,
      "description": `Audio pronunciation of letter ${currentLetter}: ${exampleWords[currentLetter]}`,
      "contentUrl": audioSrc,
      "inLanguage": "en"
    };
    const audioScript = document.createElement('script');
    audioScript.id = 'ld-json-audio';
    audioScript.type = 'application/ld+json';
    audioScript.textContent = JSON.stringify(audioLdJson);
    document.head.appendChild(audioScript);
  }

  prevLetterButton.addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + alphabets.length) % alphabets.length;
    updateLetterDisplay();
  });

  nextLetterButton.addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % alphabets.length;
    updateLetterDisplay();
  });

  // Window resize: re-setup canvas to match resized container
  window.addEventListener('resize', () => {
    setTimeout(() => {
      const img = letterImageContainer.querySelector('img');
      if (img) {
        const rect = letterImageContainer.getBoundingClientRect();
        setupCanvas(rect.width, rect.height);
      }
    }, 60);
  });

  // initial
  updateLetterDisplay();
});
