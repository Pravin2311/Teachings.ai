document.addEventListener('DOMContentLoaded', () => {
    const currentVegetableNameText = document.getElementById('current-vegetable-name');
    const vegetableImageContainer = document.getElementById('vegetable-image-container');
    const prevVegetableButton = document.getElementById('prev-vegetable');
    const nextVegetableButton = document.getElementById('next-vegetable');

    const canvas = document.getElementById('drawing-canvas');
    const ctx = canvas.getContext('2d', { willReadFrequently: true });

    const vegetables = [
        "Alexander Graham Bell", "Antoine Lavoisier", "Charles Darwin", "Gustave Eiffel", "Isaac Newton", "Leonardo Da Vinci",
        "Nikola Tesla", "Robert Oppenheimer", "Srinivas Ramanujam",  "Thomas Edison"
        
    ];
    let currentIndex = 0;
    let isDrawing = false;
    let isRevealed = false;

    // Base paths for assets
    const imageBasePath = 'assets/images/scientists/';
    const audioBasePath = 'assets/audio/scientists/'; 
    const audioFormat = '.mp3'; 
    const imageFormat = '.png'; 

    function setupCanvas() {
        canvas.width = vegetableImageContainer.clientWidth;
        canvas.height = vegetableImageContainer.clientHeight;

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
            playVegetableAudio(); 
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

    function updateVegetableDisplay() {
        const currentVegetable = vegetables[currentIndex];
        currentVegetableNameText.textContent = currentVegetable;
        
        vegetableImageContainer.innerHTML = ''; 
        
        const img = document.createElement('img');
        const imageSrc = imageBasePath + currentVegetable.toLowerCase() + imageFormat;
        img.src = imageSrc;
        img.alt = 'Image for ' + currentVegetable;
        console.log('Attempting to load image: ' + imageSrc);
        img.onload = () => {
            console.log('Image loaded successfully: ' + imageSrc);
            vegetableImageContainer.appendChild(canvas);
            setupCanvas();
        };
        img.onerror = () => {
            vegetableImageContainer.textContent = 'Image for ' + currentVegetable + ' not found. Please add ' + currentVegetable.toLowerCase() + imageFormat + ' to the assets/images/vegetables/ folder.';
            console.error('Error loading image: ' + img.src);
            vegetableImageContainer.appendChild(canvas);
            setupCanvas();
        };
        vegetableImageContainer.appendChild(img);

        console.log('Displaying vegetable: ' + currentVegetable);
    }

    function playVegetableAudio() {
        const currentVegetable = vegetables[currentIndex];
        const audioSrc = audioBasePath + currentVegetable.toLowerCase() + audioFormat;
        console.log('Attempting to play audio: ' + audioSrc);
        const audio = new Audio(audioSrc);
        
        if (window.pauseBackgroundMusic) {
            window.pauseBackgroundMusic();
        }

        audio.play().catch(e => {
            console.error('Error playing audio for ' + currentVegetable + ':', e);
        });

        audio.onended = () => {
            if (window.resumeBackgroundMusic) {
                window.resumeBackgroundMusic();
            }
        };
    }

    prevVegetableButton.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + vegetables.length) % vegetables.length;
        updateVegetableDisplay();
    });

    nextVegetableButton.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % vegetables.length;
        updateVegetableDisplay();
    });

    // Initial display
    updateVegetableDisplay();
});
