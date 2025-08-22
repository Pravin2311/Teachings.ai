// js/rhyming.js

document.addEventListener("DOMContentLoaded", () => {
  const gameContainer = document.getElementById("game-container");
  const instructionEl = document.getElementById("instruction");

  // Preload audio
  const correctAudio = document.getElementById("audio-correct") || createAudio("assets/audio/math_feedback/correct.mp3");
  const wrongAudio = document.getElementById("audio-wrong") || createAudio("assets/audio/math_feedback/incorrect.mp3");

  function createAudio(src) {
    const audio = document.createElement("audio");
    audio.src = src;
    audio.preload = "auto";
    audio.id = src.includes("correct") ? "audio-correct" : "audio-wrong";
    document.body.appendChild(audio);
    return audio;
  }

  // Rhyming word pairs
  const wordPairs = [
    ["cat", "hat"],
    ["dog", "log"],
    ["sun", "fun"],
    ["car", "star"],
    ["fish", "dish"],
    ["bed", "red"],
    ["light", "night"],
    ["goat", "boat"],
    ["tree", "bee"],
    ["moon", "spoon"]
  ];

  let currentPair = [];
  let shuffledWords = [];

  // Extract rhyme part (e.g., "at" from "cat", "hat")
  function getRhymePart(word1, word2) {
    // Simple logic: compare from end until mismatch
    let i = 1;
    while (
      i <= word1.length &&
      i <= word2.length &&
      word1[word1.length - i] === word2[word2.length - i]
    ) {
      i++;
    }
    return word1.slice(-i + 1); // Return common suffix
  }

  function getRandomWordNotIn(pair) {
    const allWords = wordPairs.flat();
    let word;
    do {
      word = allWords[Math.floor(Math.random() * allWords.length)];
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
    const rhymePart = getRhymePart(currentPair[0], currentPair[1]);
    const basePart = currentPair[0].slice(0, -rhymePart.length);

    // Update instruction
    instructionEl.innerHTML = `Find the word that rhymes with <strong>${currentPair[0]}</strong>:`;
    instructionEl.style.fontWeight = "600";

    // Highlight the rhyme part in the question word
    const highlightedWord = `<span class="word-highlight">${basePart}<strong>${rhymePart}</strong></span>`;
    gameContainer.innerHTML = `<p class="prompt">Can you find a word that rhymes with ${highlightedWord}?</p>`;

    const btnContainer = document.createElement("div");
    btnContainer.className = "word-buttons";

    shuffledWords.forEach(word => {
      const btn = document.createElement("button");
      btn.className = "word-button";
      btn.setAttribute("aria-label", `Choose ${word}`);

      // Highlight rhyme part in option (if it matches)
      if (word === currentPair[1]) {
        const optionBase = word.slice(0, -rhymePart.length);
        btn.innerHTML = `${optionBase}<strong>${rhymePart}</strong>`;
      } else {
        btn.textContent = word;
      }

      btn.onclick = () => checkAnswer(word);
      btnContainer.appendChild(btn);
    });

    gameContainer.appendChild(btnContainer);
  }

  function checkAnswer(selectedWord) {
    const isCorrect = selectedWord === currentPair[1];
    const audio = isCorrect ? correctAudio : wrongAudio;

    // Play feedback
    audio.currentTime = 0;
    audio.play();

    // Update UI
    const feedback = isCorrect
      ? `🎉 <strong>Yes!</strong> ${currentPair[0]} and <strong>${selectedWord}</strong> rhyme!`
      : `❌ <strong>Not quite.</strong> Try again!`;

    gameContainer.innerHTML = `<p class="feedback ${isCorrect ? 'correct' : 'wrong'}">${feedback}</p>`;

    // Next button
    const nextBtn = document.createElement("button");
    nextBtn.innerText = "Next";
    nextBtn.className = "next-button";
    nextBtn.onclick = startGame;
    gameContainer.appendChild(nextBtn);
  }

  function startGame() {
    // Reset container
    gameContainer.innerHTML = "";
    instructionEl.textContent = "Match the word with another that rhymes. Tap to begin!";

    // Pick a random pair
    const index = Math.floor(Math.random() * wordPairs.length);
    currentPair = wordPairs[index];

    // Create 3 options: correct + 2 distractors
    const options = [currentPair[1]];
    while (options.length < 3) {
      const word = getRandomWordNotIn(currentPair);
      if (!options.includes(word)) {
        options.push(word);
      }
    }
    shuffle(options);
    shuffledWords = options;

    // Render game
    renderWords();
  }

  // Start the game
  startGame();
});