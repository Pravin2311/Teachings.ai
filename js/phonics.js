function playSound(letter) {
  // Stop all audio before playing new one
  document.querySelectorAll('audio').forEach(audio => {
    audio.pause();
    audio.currentTime = 0;
  });

  const audio = document.getElementById(`sound-${letter}`);
  if (audio) {
    audio.play().catch(e => console.log("Play failed:", e));
  }
}

let flipped = false;
document.getElementById('flipbook').addEventListener('click', function(e) {
  const rect = this.getBoundingClientRect();
  const relY = e.clientY - rect.top;
  if (relY < 50 || relY > rect.height - 50) return;
  flipped = !flipped;
  this.classList.toggle('flipped', flipped);
});

// Drag & Drop
let droppedSounds = [];
function allowDrop(e) {
  e.preventDefault();
  document.getElementById('drop-zone').classList.add('active');
}
function drop(e) {
  e.preventDefault();
  document.getElementById('drop-zone').classList.remove('active');
  const sound = e.dataTransfer.getData("text");
  droppedSounds.push(sound);
  updateDropZone();
}
function updateDropZone() {
  const zone = document.getElementById('drop-zone');
  zone.innerHTML = droppedSounds.join(' ');
}
function playBlendedWord() {
  const word = droppedSounds.join('');
  document.getElementById('result').innerHTML = `<strong>You made: ${word}</strong>`;
  sayWord(word);
}

// Read Word
function readWord(word) {
  sayWord(word);
}

function sayWord(word) {
  const sounds = word.split('');
  let time = 0;
  sounds.forEach(sound => {
    setTimeout(() => playSound(sound), time);
    time += 500;
  });
  setTimeout(() => speakText(word), time + 300);
}

function speakText(text) {
  // Stop any ongoing speech
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.8;
    utterance.pitch = 1.2;
    window.speechSynthesis.speak(utterance);
  }
}

// Make tiles draggable
document.addEventListener("DOMContentLoaded", () => {
  const tiles = document.querySelectorAll(".sound-tile");
  tiles.forEach(tile => {
    tile.addEventListener("dragstart", (e) => {
      e.dataTransfer.setData("text/plain", tile.textContent);
      e.dataTransfer.setData("text", tile.dataset.sound);
    });
  });
});