document.addEventListener("DOMContentLoaded", () => {
    const gameContainer = document.getElementById("game-container");
    gameContainer.innerHTML = ""; // Remove loading
  
    // Add audio elements
    const correctAudio = document.createElement("audio");
    correctAudio.id = "audio-correct";
    correctAudio.src = "assets/audio/math_feedback/correct.mp3";
    correctAudio.preload = "auto";
    document.body.appendChild(correctAudio);
  
    const wrongAudio = document.createElement("audio");
    wrongAudio.id = "audio-wrong";
    wrongAudio.src = "assets/audio/math_feedback/incorrect.mp3";
    wrongAudio.preload = "auto";
    document.body.appendChild(wrongAudio);
  
    const wordPairs = [
      ["cat", "hat"],
      ["dog", "log"],
      ["sun", "fun"],
      ["car", "star"],
      ["fish", "dish"],
      ["bed", "red"]
    ];
  
    let currentPair = [];
    let shuffledWords = [];
  
    function startGame() {
      const index = Math.floor(Math.random() * wordPairs.length);
      currentPair = wordPairs[index];
      shuffledWords = [...currentPair, getRandomWordNotIn(currentPair)];
      shuffle(shuffledWords);
      renderWords();
    }
  
    function getRandomWordNotIn(pair) {
      let flatWords = wordPairs.flat();
      let word;
      do {
        word = flatWords[Math.floor(Math.random() * flatWords.length)];
      } while (pair.includes(word));
      return word;
    }
  
    function shuffle(arr) {
      for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
      }
    }
  
    function renderWords() {
      gameContainer.innerHTML = `<p class="prompt">Find the word that rhymes with <strong>${currentPair[0]}</strong>:</p>`;
      const buttons = shuffledWords.map(word => {
        const btn = document.createElement("button");
        btn.className = "word-button";
        btn.innerText = word;
        btn.onclick = () => checkAnswer(word);
        return btn;
      });
  
      const btnContainer = document.createElement("div");
      btnContainer.className = "word-buttons";
      buttons.forEach(btn => btnContainer.appendChild(btn));
      gameContainer.appendChild(btnContainer);
    }
  
    function checkAnswer(selectedWord) {
      const correct = selectedWord === currentPair[1];
      const audio = correct ? correctAudio : wrongAudio;
      const message = correct
        ? `🎉 Correct! ${currentPair[0]} rhymes with ${selectedWord}.`
        : `❌ Oops! Try again.`;
  
      audio.currentTime = 0;
      audio.play();
  
      gameContainer.innerHTML = `<p class="${correct ? "correct" : "wrong"}">${message}</p>`;
  
      const nextBtn = document.createElement("button");
      nextBtn.innerText = "Next";
      nextBtn.className = "next-button";
      nextBtn.onclick = startGame;
      gameContainer.appendChild(nextBtn);
    }
  
    startGame();
  });
  