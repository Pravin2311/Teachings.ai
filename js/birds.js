document.addEventListener('DOMContentLoaded', () => {
    const currentBirdNameText = document.getElementById('current-bird-name');
    const birdImageContainer = document.getElementById('bird-image-container');
    const prevBirdButton = document.getElementById('prev-bird');
    const nextBirdButton = document.getElementById('next-bird');

    const canvas = document.getElementById('drawing-canvas');
    const ctx = canvas.getContext('2d', { willReadFrequently: true });

    const birds = [
        "Sparrow", "Eagle", "Penguin", "Owl", "Parrot",
        "Duck", "Flamingo", "Peacock", "Hummingbird", "Pigeon"
    ];
    let currentIndex = 0;
    let isDrawing = false;
    let isRevealed = false;

    // Base paths for assets
    const imageBasePath = 'assets/images/birds/';
    const audioNameBasePath = 'assets/audio/birds/'; 
    const audioSoundBasePath = 'assets/audio/bird_sounds/'; 
    const audioFormat = '.mp3'; 
    const imageFormat = '.png'; 

    function setupCanvas() {
        canvas.width = birdImageContainer.clientWidth;
        canvas.height = birdImageContainer.clientHeight;

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
            playBirdAudio(); 
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

    function updateBirdDisplay() {
        const currentBird = birds[currentIndex];
        currentBirdNameText.textContent = currentBird;
        
        birdImageContainer.innerHTML = ''; 
        
        const img = document.createElement('img');
        const imageSrc = imageBasePath + currentBird.toLowerCase() + imageFormat;
        img.src = imageSrc;
        img.alt = 'Image for ' + currentBird;
        console.log('Attempting to load image: ' + imageSrc);
        img.onload = () => {
            console.log('Image loaded successfully: ' + imageSrc);
            birdImageContainer.appendChild(canvas);
            setupCanvas();
        };
        img.onerror = () => {
            birdImageContainer.textContent = 'Image for ' + currentBird + ' not found. Please add ' + currentBird.toLowerCase() + imageFormat + ' to the assets/images/birds/ folder.';
            console.error('Error loading image: ' + img.src);
            birdImageContainer.appendChild(canvas);
            setupCanvas();
        };
        birdImageContainer.appendChild(img);

        console.log('Displaying bird: ' + currentBird);
    }

    function playBirdAudio() {
        const currentBird = birds[currentIndex];
        const birdNameAudioSrc = audioNameBasePath + currentBird.toLowerCase() + audioFormat;
        const birdSoundAudioSrc = audioSoundBasePath + currentBird.toLowerCase() + '_sound' + audioFormat; 

        console.log('Attempting to play bird name audio: ' + birdNameAudioSrc);
        const nameAudio = new Audio(birdNameAudioSrc);
        
        if (window.pauseBackgroundMusic) {
            window.pauseBackgroundMusic();
        }

        nameAudio.play().catch(e => {
            console.error('Error playing bird name audio for ' + currentBird + ':', e);
            if (window.resumeBackgroundMusic) {
                window.resumeBackgroundMusic();
            }
        });

        nameAudio.onended = () => {
            console.log('Bird name audio finished. Attempting to play bird sound: ' + birdSoundAudioSrc);
            const soundAudio = new Audio(birdSoundAudioSrc);
            soundAudio.play().catch(e => {
                console.error('Error playing bird sound for ' + currentBird + ':', e);
            }).finally(() => {
                if (window.resumeBackgroundMusic) {
                    window.resumeBackgroundMusic();
                }
            });
        };
    }

    prevBirdButton.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + birds.length) % birds.length;
        updateBirdDisplay();
    });

    nextBirdButton.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % birds.length;
        updateBirdDisplay();
    });

    // Initial display
    updateBirdDisplay();
});
