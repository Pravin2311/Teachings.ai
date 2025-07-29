document.addEventListener('DOMContentLoaded', () => {
    const currentColorNameText = document.getElementById('current-color-name');
    const colorImageContainer = document.getElementById('color-image-container');
    const prevColorButton = document.getElementById('prev-color');
    const nextColorButton = document.getElementById('next-color');

    const canvas = document.getElementById('drawing-canvas');
    const ctx = canvas.getContext('2d', { willReadFrequently: true });

    const colors = [
        "Red", "Blue", "Yellow", "Green", "Orange",
        "Purple", "Pink", "Brown", "Black", "White"
    ];
    let currentIndex = 0;
    let isDrawing = false;
    let isRevealed = false;

    // Base paths for assets
    const imageBasePath = 'assets/images/colors/';
    const audioBasePath = 'assets/audio/colors/'; 
    const audioFormat = '.mp3'; 
    const imageFormat = '.png'; 

    function setupCanvas() {
        canvas.width = colorImageContainer.clientWidth;
        canvas.height = colorImageContainer.clientHeight;

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
            playColorAudio(); 
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

    function updateColorDisplay() {
        const currentColor = colors[currentIndex];
        currentColorNameText.textContent = currentColor;
        
        colorImageContainer.innerHTML = ''; 
        
        const img = document.createElement('img');
        const imageSrc = imageBasePath + currentColor.toLowerCase() + imageFormat;
        img.src = imageSrc;
        img.alt = 'Image for ' + currentColor;
        console.log('Attempting to load image: ' + imageSrc);
        img.onload = () => {
            console.log('Image loaded successfully: ' + imageSrc);
            colorImageContainer.appendChild(canvas);
            setupCanvas();
        };
        img.onerror = () => {
            colorImageContainer.textContent = 'Image for ' + currentColor + ' not found. Please add ' + currentColor.toLowerCase() + imageFormat + ' to the assets/images/colors/ folder.';
            console.error('Error loading image: ' + img.src);
            colorImageContainer.appendChild(canvas);
            setupCanvas();
        };
        colorImageContainer.appendChild(img);

        console.log('Displaying color: ' + currentColor);
    }

    function playColorAudio() {
        const currentColor = colors[currentIndex];
        const audioSrc = audioBasePath + currentColor.toLowerCase() + audioFormat;
        console.log('Attempting to play audio: ' + audioSrc);
        const audio = new Audio(audioSrc);
        
        if (window.pauseBackgroundMusic) {
            window.pauseBackgroundMusic();
        }

        audio.play().catch(e => {
            console.error('Error playing audio for ' + currentColor + ':', e);
        });

        audio.onended = () => {
            if (window.resumeBackgroundMusic) {
                window.resumeBackgroundMusic();
            }
        };
    }

    prevColorButton.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + colors.length) % colors.length;
        updateColorDisplay();
    });

    nextColorButton.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % colors.length;
        updateColorDisplay();
    });

    // Initial display
    updateColorDisplay();
});
