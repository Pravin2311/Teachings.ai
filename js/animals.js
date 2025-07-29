document.addEventListener('DOMContentLoaded', () => {
    const currentAnimalNameText = document.getElementById('current-animal-name');
    const animalImageContainer = document.getElementById('animal-image-container');
    const prevAnimalButton = document.getElementById('prev-animal');
    const nextAnimalButton = document.getElementById('next-animal');

    const canvas = document.getElementById('drawing-canvas');
    const ctx = canvas.getContext('2d', { willReadFrequently: true });

    const animals = [
        "Lion", "Elephant", "Monkey", "Zebra", "Giraffe",
        "Tiger", "Bear", "Kangaroo", "Dolphin", "Penguin",
        "Dog", "Cat", "Cow", "Horse", "Donkey" 
    ];
    let currentIndex = 0;
    let isDrawing = false;
    let isRevealed = false;

    // Base paths for assets
    const imageBasePath = 'assets/images/animals/';
    const audioNameBasePath = 'assets/audio/animals/'; 
    const audioSoundBasePath = 'assets/audio/animal_sounds/'; 
    const audioFormat = '.mp3'; 
    const imageFormat = '.png'; 

    function setupCanvas() {
        canvas.width = animalImageContainer.clientWidth;
        canvas.height = animalImageContainer.clientHeight;

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
            playAnimalAudio(); 
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

    function updateAnimalDisplay() {
        const currentAnimal = animals[currentIndex];
        currentAnimalNameText.textContent = currentAnimal;
        
        animalImageContainer.innerHTML = ''; 
        
        const img = document.createElement('img');
        const imageSrc = imageBasePath + currentAnimal.toLowerCase() + imageFormat;
        img.src = imageSrc;
        img.alt = 'Image for ' + currentAnimal;
        console.log('Attempting to load image: ' + imageSrc);
        img.onload = () => {
            console.log('Image loaded successfully: ' + imageSrc);
            animalImageContainer.appendChild(canvas);
            setupCanvas();
        };
        img.onerror = () => {
            animalImageContainer.textContent = 'Image for ' + currentAnimal + ' not found. Please add ' + currentAnimal.toLowerCase() + imageFormat + ' to the assets/images/animals/ folder.';
            console.error('Error loading image: ' + img.src);
            animalImageContainer.appendChild(canvas);
            setupCanvas();
        };
        animalImageContainer.appendChild(img);

        console.log('Displaying animal: ' + currentAnimal);
    }

    function playAnimalAudio() {
        const currentAnimal = animals[currentIndex];
        const animalNameAudioSrc = audioNameBasePath + currentAnimal.toLowerCase() + audioFormat;
        const animalSoundAudioSrc = audioSoundBasePath + currentAnimal.toLowerCase() + '_sound' + audioFormat; 

        console.log('Attempting to play animal name audio: ' + animalNameAudioSrc);
        const nameAudio = new Audio(animalNameAudioSrc);
        
        if (window.pauseBackgroundMusic) {
            window.pauseBackgroundMusic();
        }

        nameAudio.play().catch(e => {
            console.error('Error playing animal name audio for ' + currentAnimal + ':', e);
            if (window.resumeBackgroundMusic) {
                window.resumeBackgroundMusic();
            }
        });

        nameAudio.onended = () => {
            console.log('Animal name audio finished. Attempting to play animal sound: ' + animalSoundAudioSrc);
            const soundAudio = new Audio(animalSoundAudioSrc);
            soundAudio.play().catch(e => {
                console.error('Error playing animal sound for ' + currentAnimal + ':', e);
            }).finally(() => {
                if (window.resumeBackgroundMusic) {
                    window.resumeBackgroundMusic();
                }
            });
        };
    }

    prevAnimalButton.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + animals.length) % animals.length;
        updateAnimalDisplay();
    });

    nextAnimalButton.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % animals.length;
        updateAnimalDisplay();
    });

    // Initial display
    updateAnimalDisplay();
});
