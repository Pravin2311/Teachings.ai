document.addEventListener('DOMContentLoaded', () => {
    const backgroundMusic = document.getElementById('background-music');
    const musicToggleButton = document.getElementById('music-toggle-button');

    if (!backgroundMusic || !musicToggleButton) {
        console.error("Music elements not found. Music control will not function.");
        return; 
    }

    // Check localStorage for preferred music state (on/off)
    const isMusicOn = localStorage.getItem('kidsAppMusicOn') === 'true';

    // Function to update the button symbol and actual music state
    function updateMusicState() {
        if (isMusicOn) {
            backgroundMusic.muted = false;
            backgroundMusic.play().catch(e => {
                console.log("Autoplay of music prevented. User interaction needed.");
            });
            musicToggleButton.textContent = '\uD83D\uDD0A'; // Unmuted speaker emoji (??)
        } else {
            backgroundMusic.muted = true;
            backgroundMusic.pause(); 
            musicToggleButton.textContent = '\uD83D\uDD07'; // Muted speaker emoji (??)
        }
    }

    // Initial state setup
    backgroundMusic.muted = !isMusicOn; 
    updateMusicState();

    // Toggle music on click
    musicToggleButton.addEventListener('click', () => {
        if (backgroundMusic.muted) {
            backgroundMusic.muted = false;
            backgroundMusic.play().then(() => {
                localStorage.setItem('kidsAppMusicOn', 'true');
                musicToggleButton.textContent = '\uD83D\uDD0A';
            }).catch(e => {
                console.error("Error playing music on unmute click:", e);
                backgroundMusic.muted = true;
                musicToggleButton.textContent = '\uD83D\uDD07';
            });
        } else {
            backgroundMusic.muted = true;
            backgroundMusic.pause();
            localStorage.setItem('kidsAppMusicOn', 'false');
            musicToggleButton.textContent = '\uD83D\uDD07';
        }
    });

    // Handle user interaction to allow autoplay (for cases where it was prevented initially)
    document.body.addEventListener('click', () => {
        if (backgroundMusic.paused && !backgroundMusic.muted && localStorage.getItem('kidsAppMusicOn') === 'true') {
            backgroundMusic.play().catch(e => {
                console.log("Music play initiated by user click, but still prevented:", e);
            });
        }
    }, { once: true }); 

    // --- Global Functions for Background Music Control ---
    window.pauseBackgroundMusic = () => {
        if (!backgroundMusic.muted) { 
            backgroundMusic.pause();
            backgroundMusic.setAttribute('data-paused-by-system', 'true'); 
        }
    };

    window.resumeBackgroundMusic = () => {
        if (backgroundMusic.getAttribute('data-paused-by-system') === 'true' && localStorage.getItem('kidsAppMusicOn') === 'true') {
            backgroundMusic.play().catch(e => {
                console.error("Error resuming background music:", e);
            });
            backgroundMusic.removeAttribute('data-paused-by-system');
        }
    };
});
