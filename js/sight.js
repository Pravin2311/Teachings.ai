document.addEventListener("DOMContentLoaded", () => {
    const gameContainer = document.getElementById("game-container");
    const correctSound = document.getElementById("correct-sound");
    const wrongSound = document.getElementById("wrong-sound");
  
    const sightWords = ["the", "and", "you", "said", "come", "here", "look", "in", "is", "my", "can", "we", "it"];
    let currentWord = "";
  
    function startGame() {
      currentWord = getRandomWord();
      renderWord(currentWord);
    }
  
    function getRandomWord() {
      const index = Math.floor(Math.random() * sightWords.length);
      return sightWords[index];
    }
  
    function renderWord(word) {
      gameContainer.innerHTML = `<p class="prompt">Tap the word: <strong>${word}</strong></p>`;
      const options = shuffle([word, ...getWrongOptions(word)]);
  
      const buttonContainer = document.createElement("div");
      buttonContainer.className = "word-buttons";
  
      options.forEach(opt => {
        const btn = document.createElement("button");
        btn.className = "word-button";
        btn.innerText = opt;
        btn.onclick = () => checkAnswer(opt);
        buttonContainer.appendChild(btn);
      });
  
      gameContainer.appendChild(buttonContainer);
    }
  
    function getWrongOptions(correctWord) {
      let options = sightWords.filter(w => w !== correctWord);
      shuffle(options);
      return options.slice(0, 2);
    }
  
    function checkAnswer(selectedWord) {
      if (selectedWord === currentWord) {
        correctSound.play();
        gameContainer.innerHTML = `<p class="correct">✅ Correct! That’s "${selectedWord}".</p>`;
      } else {
        wrongSound.play();
        gameContainer.innerHTML = `<p class="wrong">❌ Try again!</p>`;
      }
  
      const nextBtn = document.createElement("button");
      nextBtn.className = "next-button";
      nextBtn.innerText = "Next";
      nextBtn.onclick = startGame;
      gameContainer.appendChild(nextBtn);
    }
  
    function shuffle(arr) {
      for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
      }
      return arr;
    }
  
    startGame();
  });
  