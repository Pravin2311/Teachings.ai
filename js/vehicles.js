document.addEventListener('DOMContentLoaded', () => {
  const currentVehicleNameText = document.getElementById('current-vehicle-name');
  const vehicleImageContainer = document.getElementById('vehicle-image-container');
  const prevVehicleButton = document.getElementById('prev-vehicle');
  const nextVehicleButton = document.getElementById('next-vehicle');

  const canvas = document.getElementById('drawing-canvas');
  const ctx = canvas.getContext('2d', { willReadFrequently: true });

  // List of vehicles - ensure filenames match
  const vehicles = [
    "Car", "Bus", "Truck", "Motorcycle", "Bicycle",
    "Train", "Airplane", "Boat", "Helicopter", "Submarine"
  ];
  let currentIndex = 0;
  let isDrawing = false;
  let isRevealed = false;

  // Base paths for assets
  const imageBasePath = 'assets/images/vehicles/';
  const audioNameBasePath = 'assets/audio/vehicles/';     // e.g., car.mp3 (says "car")
  const audioSoundBasePath = 'assets/audio/vehicle_sounds/'; // e.g., car_sound.mp3 (engine sound)
  const audioFormat = '.mp3';
  const imageFormat = '.png';

  function setupCanvas() {
    canvas.width = vehicleImageContainer.clientWidth;
    canvas.height = vehicleImageContainer.clientHeight;

    ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.lineWidth = canvas.width * 0.15;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.globalCompositeOperation = 'destination-out';

    canvas.style.opacity = '1';
    canvas.style.transition = 'none';
    isRevealed = false;

    // Add "Scratch Here" text
    ctx.globalCompositeOperation = 'source-over';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
    ctx.font = 'bold ' + (canvas.width * 0.1) + 'px Poppins';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('SCRATCH HERE', canvas.width / 2, canvas.height / 2);
    ctx.globalCompositeOperation = 'destination-out';
  }

  function getMousePos(e) {
    const rect = canvas.getBoundingClientRect();
    return { x: e.clientX - rect.left, y: e.clientY - rect.top };
  }

  function getTouchPos(e) {
    const rect = canvas.getBoundingClientRect();
    return { x: e.touches[0].clientX - rect.left, y: e.touches[0].clientY - rect.top };
  }

  function startDrawing(e) {
    if (isRevealed) return;
    isDrawing = true;
    const pos = e.touches ? getTouchPos(e) : getMousePos(e);
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
  }

  function draw(e) {
    if (!isDrawing || isRevealed) return;
    e.preventDefault();
    const pos = e.touches ? getTouchPos(e) : getMousePos(e);
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
  }

  function checkRevealProgress() {
    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;
    let transparentPixels = 0;
    const totalPixels = data.length / 4;
    const sampleStep = 40;

    for (let i = 3; i < data.length; i += 4 * sampleStep) {
      if (data[i] < 50) {
        transparentPixels++;
      }
    }

    const sampledTotalPixels = Math.floor(totalPixels / sampleStep);
    const revealPercentage = (transparentPixels / sampledTotalPixels) * 100;
    const REVEAL_THRESHOLD = 50;

    if (revealPercentage >= REVEAL_THRESHOLD && !isRevealed) {
      isRevealed = true;
      canvas.style.opacity = '0';
      canvas.style.transition = 'opacity 1s ease-out';
      console.log('Image fully revealed!');
      playVehicleAudio(); // Play both name and sound
    }
  }

  function stopDrawing() {
    isDrawing = false;
    if (!isRevealed) {
      checkRevealProgress();
    }
  }

  // Mouse Events
  canvas.addEventListener('mousedown', startDrawing);
  canvas.addEventListener('mousemove', draw);
  canvas.addEventListener('mouseup', stopDrawing);
  canvas.addEventListener('mouseleave', stopDrawing);

  // Touch Events (with passive: false for preventDefault)
  canvas.addEventListener('touchstart', startDrawing, { passive: false });
  canvas.addEventListener('touchmove', draw, { passive: false });
  canvas.addEventListener('touchend', stopDrawing);
  canvas.addEventListener('touchcancel', stopDrawing);

  function updateVehicleDisplay() {
    const currentVehicle = vehicles[currentIndex];
    currentVehicleNameText.textContent = currentVehicle;

    // Clear container
    vehicleImageContainer.innerHTML = '';

    const img = document.createElement('img');
    const imageSrc = imageBasePath + currentVehicle.toLowerCase() + imageFormat;
    img.src = imageSrc;
    img.alt = 'Image for ' + currentVehicle;
    console.log('Attempting to load image: ' + imageSrc);

    img.onload = () => {
      console.log('Image loaded successfully: ' + imageSrc);
      vehicleImageContainer.appendChild(img);
      vehicleImageContainer.appendChild(canvas);
      setupCanvas();
    };

    img.onerror = () => {
      vehicleImageContainer.textContent = `Image for ${currentVehicle.toLowerCase()}${imageFormat} not found. Please add it to ${imageBasePath}`;
      console.error('Error loading image:', img.src);
      vehicleImageContainer.appendChild(canvas);
      setupCanvas();
    };

    // Append image first (even if it fails, canvas will show)
    vehicleImageContainer.appendChild(img);
  }

  function playVehicleAudio() {
    const currentVehicle = vehicles[currentIndex].toLowerCase();

    // 1. Play NAME (e.g., "This is a car")
    const nameAudioSrc = audioNameBasePath + currentVehicle + audioFormat;
    const nameAudio = new Audio(nameAudioSrc);

    // Optional: Pause background music
    if (typeof window.pauseBackgroundMusic === 'function') {
      window.pauseBackgroundMusic();
    }

    nameAudio.play().catch(e => {
      console.error(`Error playing name audio for ${currentVehicle}:`, e);
      resumeMusicFallback();
    });

    nameAudio.onended = () => {
      // 2. Play SOUND (e.g., car engine, siren)
      const soundAudioSrc = audioSoundBasePath + currentVehicle + '_sound' + audioFormat;
      const soundAudio = new Audio(soundAudioSrc);

      soundAudio.play().catch(e => {
        console.error(`Error playing sound effect for ${currentVehicle}:`, e);
      }).finally(() => {
        resumeMusicFallback();
      });
    };
  }

  function resumeMusicFallback() {
    if (typeof window.resumeBackgroundMusic === 'function') {
      window.resumeBackgroundMusic();
    }
  }

  // Navigation
  prevVehicleButton.addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + vehicles.length) % vehicles.length;
    updateVehicleDisplay();
  });

  nextVehicleButton.addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % vehicles.length;
    updateVehicleDisplay();
  });

  // Initial load
  updateVehicleDisplay();
});