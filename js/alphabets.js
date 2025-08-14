document.addEventListener('DOMContentLoaded', () => {
    const currentLetterText = document.getElementById('current-letter-text');
    const letterImageContainer = document.getElementById('letter-image-container');
    const prevLetterButton = document.getElementById('prev-letter');
    const nextLetterButton = document.getElementById('next-letter');

    const canvas = document.getElementById('drawing-canvas');
    const ctx = canvas.getContext('2d', { willReadFrequently: true });

    const alphabets = Array.from({ length: 26 }, (_, i) => String.fromCharCode(65 + i));
    let currentIndex = 0;
    let isDrawing = false;
    let isRevealed = false;

    const imageBasePath = 'assets/images/alphabets/';
    const audioBasePath = 'assets/audio/alphabets/';
    const audioFormat = '.mp3';
    const imageFormat = '.png';

    const exampleWords = {
        A: 'Apple', B: 'Ball', C: 'Cat', D: 'Dog', E: 'Elephant', F: 'Fish', G: 'Giraffe',
        H: 'Hat', I: 'Ice cream', J: 'Juice', K: 'Kite', L: 'Lion', M: 'Monkey', N: 'Nest',
        O: 'Orange', P: 'Penguin', Q: 'Queen', R: 'Rabbit', S: 'Sun', T: 'Tiger',
        U: 'Umbrella', V: 'Violin', W: 'Whale', X: 'Xylophone', Y: 'Yacht', Z: 'Zebra'
    };

    function setupCanvas() {
        canvas.width = letterImageContainer.clientWidth;
        canvas.height = letterImageContainer.clientHeight;

        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.lineWidth = canvas.width * 0.15;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';
        ctx.globalCompositeOperation = 'destination-out';

        canvas.style.opacity = '1';
        canvas.style.transition = 'none';
        isRevealed = false;

        // "Scratch Here" overlay
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
            if (data[i] < 50) transparentPixels++;
        }

        const sampledTotalPixels = Math.floor(totalPixels / sampleStep);
        const revealPercentage = (transparentPixels / sampledTotalPixels) * 100;

        if (revealPercentage >= 30 && !isRevealed) {
            isRevealed = true;
            canvas.style.opacity = '0';
            canvas.style.transition = 'opacity 1s ease-out';
            playLetterAudio();
        }
    }

    function stopDrawing() {
        isDrawing = false;
        if (!isRevealed) checkRevealProgress();
    }

    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseleave', stopDrawing);
    canvas.addEventListener('touchstart', startDrawing, { passive: false });
    canvas.addEventListener('touchmove', draw, { passive: false });
    canvas.addEventListener('touchend', stopDrawing);
    canvas.addEventListener('touchcancel', stopDrawing);

    function updateLetterDisplay() {
        const currentLetter = alphabets[currentIndex];
        currentLetterText.textContent = currentLetter;
        letterImageContainer.innerHTML = '';

        const img = document.createElement('img');
        img.src = imageBasePath + currentLetter + imageFormat;
        img.alt = `Letter ${currentLetter}: ${exampleWords[currentLetter]} - Learn ABC letters with Teachings.AI`;
        img.loading = 'lazy';

        img.onload = () => {
            letterImageContainer.appendChild(img);
            letterImageContainer.appendChild(canvas);
            setupCanvas();
            canvas.setAttribute('aria-label', `Scratch card for letter ${currentLetter}`);
        };

        img.onerror = () => {
            console.error('Error loading image: ' + img.src);
            const fallbackText = document.createElement('p');
            fallbackText.textContent = `Image for ${currentLetter} not found. Add ${currentLetter}${imageFormat} to assets/images/alphabets/`;
            letterImageContainer.appendChild(fallbackText);
            letterImageContainer.appendChild(canvas);
            setupCanvas();
            canvas.setAttribute('aria-label', `Scratch card for letter ${currentLetter}`);
        };

        letterImageContainer.appendChild(img);

        // Structured Data for SEO
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

        console.log('Displaying letter: ' + currentLetter);
    }

    function playLetterAudio() {
        const currentLetter = alphabets[currentIndex];
        const audioSrc = audioBasePath + currentLetter + audioFormat;
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

        // Audio structured data for SEO
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

    // Initial display
    updateLetterDisplay();
});
