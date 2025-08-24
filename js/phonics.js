    // Define your words with: word, image, sound sequence, full word audio
    const words = [
  { 
    word: "CAT", 
    img: "assets/images/animals/cat.png", 
    sounds: ["C", "A", "T"], 
    full: "assets/audio/animals/cat.mp3" 
  },
  { 
    word: "COW", 
    img: "assets/images/animals/cow.png", 
    sounds: ["C", "O", "W"], 
    full: "assets/audio/animals/cow.mp3" 
  },
  { 
    word: "DOG", 
    img: "assets/images/animals/dog.png", 
    sounds: ["D", "O", "G"], 
    full: "assets/audio/animals/dog.mp3" 
  },
  { 
    word: "OWL", 
    img: "assets/images/birds/owl.png", 
    sounds: ["O", "W", "L"], 
    full: "assets/audio/birds/owl.mp3" 
  },
  { 
    word: "BUS", 
    img: "assets/images/vehicles/bus.png", 
    sounds: ["B", "U", "S"], 
    full: "assets/audio/vehicles/bus.mp3" 
  },
  { 
    word: "CAR", 
    img: "assets/images/vehicles/car.png", 
    sounds: ["C", "A", "R"], 
    full: "assets/audio/vehicles/car.mp3" 
  },
  { 
    word: "HORSE", 
    img: "assets/images/animals/horse.png", 
    sounds: ["H", "O", "R", "S", "E"], 
    full: "assets/audio/animals/horse.mp3" 
  },
  { 
    word: "HEN", 
    img: "assets/images/birds/hen.png", 
    sounds: ["H", "E", "N"], 
    full: "assets/audio/birds/hen.mp3" 
  },
  { 
    word: "LION", 
    img: "assets/images/animals/lion.png", 
    sounds: ["L", "I", "O", "N"], 
    full: "assets/audio/animals/lion.mp3" 
  },
  { 
    word: "TIGER", 
    img: "assets/images/animals/tiger.png", 
    sounds: ["T", "I", "G", "E", "R"], 
    full: "assets/audio/animals/tiger.mp3" 
  },
  { 
    word: "DUCK", 
    img: "assets/images/birds/duck.png", 
    sounds: ["D", "U", "C", "K"], 
    full: "assets/audio/birds/duck.mp3" 
  },
  { 
    word: "APPLE", 
    img: "assets/images/fruits/apple.png", 
    sounds: ["A", "P", "P", "L", "E"], 
    full: "assets/audio/fruits/apple.mp3" 
  },
  { 
    word: "EARTH", 
    img: "assets/images/planets/earth.png", 
    sounds: ["E", "A", "R", "T", "H"], 
    full: "assets/audio/planets/earth.mp3" 
  },
  { 
    word: "MANGO", 
    img: "assets/images/fruits/mango.png", 
    sounds: ["M", "A", "N", "G", "O"], 
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
