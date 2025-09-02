document.addEventListener('DOMContentLoaded', () => {
    const currentAnimalNameText = document.getElementById('current-animal-name');
    const animalImageContainer = document.getElementById('animal-image-container');
    const prevAnimalButton = document.getElementById('prev-animal');
    const nextAnimalButton = document.getElementById('next-animal');

    const canvas = document.getElementById('drawing-canvas');
    const ctx = canvas.getContext('2d', { willReadFrequently: true });

    const organs = [
        "Brain", "Eye", "Heart", "Intestine", "Kidney",
        "Liver", "Lungs", "Lymph-Node", "Muscle", "Stomach",
        "Teeth", "Uterus"
    ];
    let currentIndex = 0;
    let isDrawing = false;
    let isRevealed = false;

    const imageBasePath = CDN + 'assets/images/organs/';
    const audioNameBasePath = CDN + 'assets/audio/organs/';
    const audioFormat = '.mp3';
    const imageFormat = '.png';

    function setupCanvas() {
        canvas.width = animalImageContainer.clientWidth || 300;
        canvas.height = animalImageContainer.clientHeight || 300;

        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Overlay
        ctx.fillStyle = 'rgba(0,0,0,0.7)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // "Scratch Here" text
        ctx.globalCompositeOperation = 'source-over';
        const fontSize = canvas.width * 0.07;
        ctx.font = `bold ${fontSize}px 'Poppins', sans-serif`;
        ctx.fillStyle = 'rgba(255,255,255,0.8)';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('SCRATCH HERE', canvas.width / 2, canvas.height / 2);

        // Switch to erase mode
        ctx.globalCompositeOperation = 'destination-out';
        ctx.lineWidth = Math.max(30, canvas.width * 0.02);
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';

        canvas.style.opacity = '1';
        canvas.style.transition = 'opacity 0.6s ease-out';
        isRevealed = false;
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

    function stopDrawing() {
        isDrawing = false;
        if (!isRevealed) checkRevealProgress();
    }

    function checkRevealProgress() {
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;
        let transparentPixels = 0;
        const totalPixels = data.length / 4;
        const sampleStep = 20;

        for (let i = 3; i < data.length; i += 4 * sampleStep) {
            if (data[i] < 50) transparentPixels++;
        }

        const revealPercentage = (transparentPixels / Math.floor(totalPixels / sampleStep)) * 100;

        if (revealPercentage > 50 && !isRevealed) {
            isRevealed = true;
            canvas.style.opacity = '0';
            playOrganAudio();
        }
    }

    // Scratch listeners
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseleave', stopDrawing);

    canvas.addEventListener('touchstart', startDrawing, { passive: false });
    canvas.addEventListener('touchmove', draw, { passive: false });
    canvas.addEventListener('touchend', stopDrawing);
    canvas.addEventListener('touchcancel', stopDrawing);

    function updateOrganDisplay() {
        const currentOrgan = organs[currentIndex];
        currentAnimalNameText.textContent = currentOrgan;

        // Reset container
        animalImageContainer.innerHTML = '';

        // Add organ image
        const img = new Image();
        img.src = imageBasePath + currentOrgan.toLowerCase().replace(/ /g, '-') + imageFormat;
        img.alt = currentOrgan;
        img.classList.add('organ-img'); // keep it CSS-positioned
        animalImageContainer.appendChild(img);

        // Add scratch canvas above
        animalImageContainer.appendChild(canvas);

        img.onload = () => {
            setupCanvas();
        };

        img.onerror = () => {
            console.error(`❌ Failed to load image: ${img.src}`);
            currentAnimalNameText.textContent = `Image not found: ${currentOrgan}`;
            setupCanvas();
        };
    }

    function playOrganAudio() {
        const currentOrgan = organs[currentIndex];
        const audioSrc = audioNameBasePath + currentOrgan.toLowerCase().replace(/ /g, '-') + audioFormat;
        const audio = new Audio(audioSrc);

        if (window.pauseBackgroundMusic) window.pauseBackgroundMusic();

        audio.play().catch(e => {
            console.error('Audio play error:', e);
            if (window.resumeBackgroundMusic) window.resumeBackgroundMusic();
        });

        audio.onended = () => {
            if (window.resumeBackgroundMusic) window.resumeBackgroundMusic();
        };
    }

    prevAnimalButton.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + organs.length) % organs.length;
        updateOrganDisplay();
    });

    nextAnimalButton.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % organs.length;
        updateOrganDisplay();
    });

    updateOrganDisplay();
    window.addEventListener('resize', () => {
        if (!isRevealed) setupCanvas();
    });
});
