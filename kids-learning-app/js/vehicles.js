document.addEventListener('DOMContentLoaded', () => {
    const currentVehicleNameText = document.getElementById('current-vehicle-name');
    const vehicleImageContainer = document.getElementById('vehicle-image-container');
    const prevVehicleButton = document.getElementById('prev-vehicle');
    const nextVehicleButton = document.getElementById('next-vehicle');

    const canvas = document.getElementById('drawing-canvas');
    const ctx = canvas.getContext('2d', { willReadFrequently: true });

    const vehicles = [
        "Car", "Bus", "Truck", "Motorcycle", "Bicycle",
        "Train", "Airplane", "Boat", "Helicopter", "Submarine"
    ];
    let currentIndex = 0;
    let isDrawing = false;
    let isRevealed = false;

    // Base paths for assets
    const imageBasePath = 'assets/images/vehicles/';
    const audioNameBasePath = 'assets/audio/vehicles/'; 
    const audioSoundBasePath = 'assets/audio/vehicle_sounds/'; 
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

        // --- Add "Scratch Here" text ---
        ctx.globalCompositeOperation = 'source-over'; 
        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)'; 
        // CORRECTED: Using string concatenation instead of template literal
        ctx.font = 'bold ' + (canvas.width * 0.1) + 'px Poppins'; 
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('SCRATCH HERE', canvas.width / 2, canvas.height / 2); 
        ctx.globalCompositeOperation = 'destination-out'; 
    }

    function getMousePos(e) {
        const rect = canvas.getBoundingClientRect();
        return {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };
    }

    function getTouchPos(e) {
        const rect = canvas.getBoundingClientRect();
        return {
            x: e.touches[0].clientX - rect.left,
            y: e.touches[0].clientY - rect.top
        };
    }

    function startDrawing(e) {
        if (isRevealed) return; 
        isDrawing = true;
        ctx.beginPath();
        const pos = e.touches ? getTouchPos(e) : getMousePos(e);
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

        console.log('Revealed: ' + revealPercentage.toFixed(2) + '%');

        const REVEAL_THRESHOLD = 50; 

        if (revealPercentage >= REVEAL_THRESHOLD && !isRevealed) {
            isRevealed = true;
            canvas.style.opacity = '0'; 
            canvas.style.transition = 'opacity 1s ease-out'; 
            console.log('Image fully revealed!');
            playVehicleAudio(); 
        }
    }

    function stopDrawing() {
        isDrawing = false;
        if (!isRevealed) { 
            checkRevealProgress();
        }
    }

    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseleave', stopDrawing); 

    canvas.addEventListener('touchstart', startDrawing, { passive: false });
    canvas.addEventListener('touchmove', draw, { passive: false });
    canvas.addEventListener('touchend', stopDrawing);
    canvas.addEventListener('touchcancel', stopDrawing);

    function updateVehicleDisplay() {
        const currentVehicle = vehicles[currentIndex];
        currentVehicleNameText.textContent = currentVehicle;
        
        vehicleImageContainer.innerHTML = ''; 
        
        const img = document.createElement('img');
        const imageSrc = imageBasePath + currentVehicle.toLowerCase() + imageFormat;
        img.src = imageSrc;
        img.alt = 'Image for ' + currentVehicle;
        console.log('Attempting to load image: ' + imageSrc);
        img.onload = () => {
            console.log('Image loaded successfully: ' + imageSrc);
            vehicleImageContainer.appendChild(canvas);
            setupCanvas();
        };
        img.onerror = () => {
            vehicleImageContainer.textContent = 'Image for ' + currentVehicle + ' not found. Please add ' + currentVehicle.toLowerCase() + imageFormat + ' to the assets/images/vehicles/ folder.';
            console.error('Error loading image: ' + img.src);
            vehicleImageContainer.appendChild(canvas);
            setupCanvas();
        };
        vehicleImageContainer.appendChild(img);

        console.log('Displaying vehicle: ' + currentVehicle);
    }

    function playVehicleAudio() {
        const currentVehicle = vehicles[currentIndex];
        const vehicleNameAudioSrc = audioNameBasePath + currentVehicle.toLowerCase() + audioFormat;
        const vehicleSoundAudioSrc = audioSoundBasePath + currentVehicle.toLowerCase() + '_sound' + audioFormat; 

        console.log('Attempting to play vehicle name audio: ' + vehicleNameAudioSrc);
        const nameAudio = new Audio(vehicleNameAudioSrc);
        
        if (window.pauseBackgroundMusic) {
            window.pauseBackgroundMusic();
        }

        nameAudio.play().catch(e => {
            console.error('Error playing vehicle name audio for ' + currentVehicle + ':', e);
            if (window.resumeBackgroundMusic) {
                window.resumeBackgroundMusic();
            }
        });

        nameAudio.onended = () => {
            console.log('Vehicle name audio finished. Attempting to play vehicle sound: ' + vehicleSoundAudioSrc);
            const soundAudio = new Audio(vehicleSoundAudioSrc);
            soundAudio.play().catch(e => {
                console.error('Error playing vehicle sound for ' + currentVehicle + ':', e);
            }).finally(() => {
                if (window.resumeBackgroundMusic) {
                    window.resumeBackgroundMusic();
                }
            });
        };
    }

    prevVehicleButton.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + vehicles.length) % vehicles.length;
        updateVehicleDisplay();
    });

    nextVehicleButton.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % vehicles.length;
        updateVehicleDisplay();
    });

    // Initial display
    updateVehicleDisplay();
});
