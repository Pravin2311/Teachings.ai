// js/sentences.js

// List of simple sentences (3-4 words)
const sentences = [
  "I see you",
  "We love books",
  "Birds can fly",
  "Dogs bark loud",
  "She eats cake",
  "They are happy",
  "He likes toys",
  "Cats chase mice",
  "I play with ball",
  "He drinks cold milk",
  "Birds sit on tree",
  "We read at night",
  "Dogs run very fast",
  "She sings sweet songs",
  "They live near school"
];

let current = 0;
let userSentence = [];
let correctWords = [];

// DOM Elements
const optionsEl = document.getElementById('word-options');
const feedbackEl = document.getElementById('feedback');
const instructionEl = document.getElementById('instruction');
const sentenceAudio = document.getElementById('sentence-audio');
const audioCorrect = document.getElementById('audio-correct');
const audioWrong = document.getElementById('audio-wrong');

// Load the current sentence
function loadSentence() {
  userSentence = [];
  feedbackEl.textContent = "";
  optionsEl.innerHTML = "";

  const sentence = sentences[current];
  correctWords = sentence.split(" ");
  instructionEl.textContent = `Arrange the words in the correct order:`;

  // Shuffle the words
  const shuffled = [...correctWords];
  shuffleArray(shuffled);

  // Create buttons for each word
  shuffled.forEach(word => {
    const btn = document.createElement("button");
    btn.className = "word-button";
    btn.textContent = word;
    btn.onclick = () => selectWord(word, btn);
    optionsEl.appendChild(btn);
  });

  // Play audio of the full sentence
  playSentenceAudio(sentence);
}

// Handle word selection
function selectWord(word, button) {
  const expectedWord = correctWords[userSentence.length];

  if (word === expectedWord) {
    // ✅ Correct next word
    userSentence.push(word);
    button.disabled = true;
    button.classList.add("correct-word"); // Green

    // Update feedback
    updateSelectedSentence();

    // Check if sentence is complete
    if (userSentence.length === correctWords.length) {
      feedbackEl.innerHTML = "🎉 <strong>Well done! Sentence complete!</strong>";
      audioCorrect.play();
      speak("Well done! Sentence complete!");
      // Optional: auto-next after 2 seconds
      // setTimeout(nextSentence, 2000);
    } else {
      // Play soft chime or nothing
    }
  } else {
    // ❌ Wrong word
    button.classList.add("incorrect-word"); // Red
    audioWrong.play();
    speak("Try again");
    
    // Remove red after animation
    setTimeout(() => {
      button.classList.remove("incorrect-word");
    }, 800);
  }
}

// Update display of selected words
function updateSelectedSentence() {
  // You can add a "selected" area if desired
  // For now, we rely on button coloring and final feedback
}

// Shuffle array (Fisher-Yates)
function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

// Text-to-speech
function speak(text) {
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-US";
  utterance.rate = 0.9;
  utterance.pitch = 1;
  speechSynthesis.speak(utterance);
}

// Play full sentence audio
function playSentenceAudio(text) {
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-US";
  utterance.rate = 0.85;
  speechSynthesis.speak(utterance);
}

// Navigation
function nextSentence() {
  if (current < sentences.length - 1) {
    current++;
    loadSentence();
  } else {
    feedbackEl.innerHTML = "🎉 <strong>You've completed all sentences!</strong>";
    optionsEl.innerHTML = "";
    audioCorrect.play();
    speak("You've completed all sentences!");
  }
}

function prevSentence() {
  if (current > 0) {
    current--;
    loadSentence();
  }
}

// Event Listeners
document.getElementById('next-btn').onclick = nextSentence;
document.getElementById('prev-btn').onclick = prevSentence;
document.getElementById('submit-btn').style.display = 'none'; // Hide submit

// Start game
window.onload = loadSentence;