const sentences = [
    "I see you", "We love books", "Birds can fly", "Dogs bark loud",
    "She eats cake", "They are happy", "He likes toys", "Cats chase mice",
    "I play with ball", "He drinks cold milk", "Birds sit on tree",
    "We read at night", "Dogs run very fast", "She sings sweet songs", "They live near school"
  ];
  
  let current = 0;
  let userSentence = [];
  let correct = sentences[current];
  
  const optionsEl = document.getElementById('word-options');
  const feedbackEl = document.getElementById('feedback');
  const sentenceAudio = document.getElementById('sentence-audio');
  
  function loadSentence() {
    userSentence = [];
    feedbackEl.textContent = "";
  
    correct = sentences[current];
    const words = correct.split(" ");
    const distractors = ["tree", "milk", "sun", "run", "sweet", "ball", "near", "cake", "fast"];
    const allWords = [...words];
  
    while (allWords.length < words.length + 3) {
      const extra = distractors[Math.floor(Math.random() * distractors.length)];
      if (!allWords.includes(extra)) allWords.push(extra);
    }
  
    allWords.sort(() => Math.random() - 0.5);
  
    optionsEl.innerHTML = "";
    allWords.forEach(word => {
      const btn = document.createElement("button");
      btn.className = "word-button";
      btn.textContent = word;
      btn.onclick = () => {
        if (userSentence.length < words.length) {
          userSentence.push(word);
          btn.disabled = true;
          btn.classList.add("selected-word");
          updateSelected();
        }
      };
      optionsEl.appendChild(btn);
    });
  
    updateSelected();
    playSentenceAudio(correct);
  }
  
  function updateSelected() {
    const selectedEl = document.getElementById('selected-sentence');
    selectedEl.textContent = userSentence.join(" ");
  }
  
  function checkSentence() {
    if (userSentence.join(" ") === correct) {
      feedbackEl.textContent = "✅ Correct!";
      speak("Correct!");
    } else {
      feedbackEl.textContent = "❌ Try again!";
      speak("Try again");
      loadSentence(); // Reset and allow new selection
    }
  }
  
  function nextSentence() {
    if (current < sentences.length - 1) {
      current++;
      loadSentence();
    } else {
      feedbackEl.textContent = "🎉 Game Over!";
      optionsEl.innerHTML = "";
      document.getElementById('selected-sentence').textContent = "";
    }
  }
  
  function prevSentence() {
    if (current > 0) {
      current--;
      loadSentence();
    }
  }
  
  function playSentenceAudio(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-US";
    speechSynthesis.speak(utterance);
  }
  
  function speak(msg) {
    const utterance = new SpeechSynthesisUtterance(msg);
    utterance.lang = "en-US";
    speechSynthesis.speak(utterance);
  }
  
  document.getElementById('submit-btn').onclick = checkSentence;
  document.getElementById('next-btn').onclick = nextSentence;
  document.getElementById('prev-btn').onclick = prevSentence;
  
  window.onload = loadSentence;
  