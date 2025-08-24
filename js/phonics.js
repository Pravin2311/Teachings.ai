    // Define your words with: word, image, sound sequence, full word audio
    const words = [
      { 
        word: "CAT", 
        img: "assets/images/animals/cat.png", 
        sounds: ["c", "a", "t"], 
        full: "assets/audio/animals/cat.mp3" 
      },
      { 
        word: "COW", 
        img: "assets/images/animals/cow.png", 
        sounds: ["c", "o", "w"], 
        full: "assets/audio/animals/cow.mp3" 
      },
      { 
        word: "DOG", 
        img: "assets/images/animals/dog.png", 
        sounds: ["d", "o", "g"], 
        full: "assets/audio/animals/dog.mp3" 
      },
      { 
        word: "OWL", 
        img: "assets/images/birds/owl.png", 
        sounds: ["o", "w", "l"], 
        full: "assets/audio/birds/owl.mp3" 
      },
      { 
        word: "BUS", 
        img: "assets/images/vehicles/bus.png", 
        sounds: ["b", "u", "s"], 
        full: "assets/audio/vehicles/bus.mp3" 
      },
      { 
        word: "CAR", 
        img: "assets/images/vehicles/car.png", 
        sounds: ["c", "a", "r"], 
        full: "assets/audio/vehicles/car.mp3" 
      },
      { 
        word: "HORSE", 
        img: "assets/images/animals/horse.png", 
        sounds: ["h", "o", "r", "s", "e"], 
        full: "assets/audio/animals/horse.mp3" 
      },
      { 
        word: "HEN", 
        img: "assets/images/birds/hen.png", 
        sounds: ["h", "e", "n"], 
        full: "assets/audio/birds/hen.mp3" 
      },
      { 
        word: "LION", 
        img: "assets/images/animals/lion.png", 
        sounds: ["l", "i", "o", "n"], 
        full: "assets/audio/animals/lion.mp3" 
      },
      { 
        word: "TIGER", 
        img: "assets/images/animals/tiger.png", 
        sounds: ["t", "i", "g", "e", "r"], 
        full: "assets/audio/animals/tiger.mp3" 
      },
      { 
        word: "DUCK", 
        img: "assets/images/birds/duck.png", 
        sounds: ["d", "u", "c", "k"], 
        full: "assets/audio/birds/duck.mp3" 
      },
      { 
        word: "APPLE", 
        img: "assets/images/fruits/apple.png", 
        sounds: ["a", "p", "p", "l", "e"], 
        full: "assets/audio/fruits/apple.mp3" 
      },
      { 
        word: "EARTH", 
        img: "assets/images/planets/earth.png", 
        sounds: ["e", "a", "r", "t", "h"], 
        full: "assets/audio/planets/earth.mp3" 
      },
      { 
        word: "MANGO", 
        img: "assets/images/fruits/mango.png", 
        sounds: ["m", "a", "n", "g", "o"], 
        full: "assets/audio/fruits/mango.mp3" 
      }
    ];

    let currentIndex = 0;

    function updateWord() {
      const w = words[currentIndex];
      document.getElementById("wordText").textContent = w.word;
      document.getElementById("wordImage").src = w.img;
      document.getElementById("wordImage").alt = w.word;
      document.getElementById("wordAudio").src = w.full;
      document.getElementById("current").textContent = currentIndex + 1;
    }

    function playSound(letter) {
      const audio = document.getElementById(`sound-${letter}`);
      if (audio) {
        audio.currentTime = 0;
        audio.play().catch(e => console.log("Audio failed:", e));
      }
    }

    function blendWord() {
      const wordData = words[currentIndex];
      const sounds = wordData.sounds;
      let time = 0;

      // Play each sound slowly
      sounds.forEach((sound, i) => {
        setTimeout(() => playSound(sound), time);
        time += 600; // 0.6 seconds between sounds
      });

      // Say full word after blending
      setTimeout(() => {
        const fullAudio = document.getElementById("wordAudio");
        fullAudio.currentTime = 0;
        fullAudio.play().catch(e => console.log("Word play failed:", e));
      }, time + 300);
    }

    function nextWord() {
      currentIndex = (currentIndex + 1) % words.length;
      updateWord();
    }

    // Initialize
    window.onload = updateWord;
