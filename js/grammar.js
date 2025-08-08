const nounWords = ["dog", "cat", "school", "apple", "car", "tree", "ball", "book", "city", "flower"];
const verbWords = ["run", "jump", "eat", "read", "write", "play", "sleep", "drive", "draw", "sing"];
let currentWords = [];

const wordContainer = document.getElementById("word-container");
const nounZone = document.getElementById("noun-zone");
const verbZone = document.getElementById("verb-zone");
const feedbackMessage = document.getElementById("feedback-message");
const submitBtn = document.getElementById("submit-btn");
const tryAgainBtn = document.getElementById("try-again-btn");
const correctAudio = document.getElementById("audio-correct");
const wrongAudio = document.getElementById("audio-wrong");

function shuffle(array) {
  return [...array].sort(() => Math.random() - 0.5);
}

function generateWords() {
  wordContainer.innerHTML = "";
  nounZone.innerHTML = "<h2>Nouns</h2>";
  verbZone.innerHTML = "<h2>Verbs</h2>";
  feedbackMessage.textContent = "";
  tryAgainBtn.style.display = "none";

  const selectedNouns = shuffle(nounWords).slice(0, 4).map(word => ({ word, type: "noun" }));
  const selectedVerbs = shuffle(verbWords).slice(0, 4).map(word => ({ word, type: "verb" }));
  currentWords = shuffle([...selectedNouns, ...selectedVerbs]);

  currentWords.forEach(({ word, type }) => {
    const wordEl = document.createElement("div");
    wordEl.className = "draggable-word";
    wordEl.textContent = word;
    wordEl.dataset.type = type;
    addDragAndTouchListeners(wordEl);
    wordContainer.appendChild(wordEl);
  });
}

function addDragAndTouchListeners(el) {
  // Drag (mouse)
  el.draggable = true;

  el.addEventListener("dragstart", (e) => {
    e.dataTransfer.setData("text", el.textContent);
    el.classList.add("dragging");
    document.body.classList.add("dragging");
  });

  el.addEventListener("dragend", () => {
    el.classList.remove("dragging");
    document.body.classList.remove("dragging");
  });

  // Touch (mobile)
  el.addEventListener("touchstart", (e) => {
    el.classList.add("dragging");
    document.body.classList.add("dragging");
    const touch = e.touches[0];
    el.startX = touch.clientX - el.offsetLeft;
    el.startY = touch.clientY - el.offsetTop;
  });

  el.addEventListener("touchmove", (e) => {
    const touch = e.touches[0];
    el.style.position = "absolute";
    el.style.left = `${touch.clientX - el.startX}px`;
    el.style.top = `${touch.clientY - el.startY}px`;
    el.style.zIndex = 1000;

    const touchedZone = getClosestDropZone(touch.clientX, touch.clientY);
    if (touchedZone) touchedZone.classList.add("over");
  });

  el.addEventListener("touchend", (e) => {
    document.body.classList.remove("dragging");
    el.classList.remove("dragging");

    const touch = e.changedTouches[0];
    const dropZone = getClosestDropZone(touch.clientX, touch.clientY);
    if (dropZone) {
      dropZone.appendChild(el);
      dropZone.classList.remove("over");
      el.style.position = "static";
      el.style.zIndex = "unset";
    } else {
      el.style.position = "static";
      el.style.zIndex = "unset";
    }
  });
}

function getClosestDropZone(x, y) {
  const zones = [nounZone, verbZone];
  return zones.find(zone => {
    const rect = zone.getBoundingClientRect();
    return (
      x >= rect.left &&
      x <= rect.right &&
      y >= rect.top &&
      y <= rect.bottom
    );
  });
}

// Drop handling (mouse)
[nounZone, verbZone].forEach(zone => {
  zone.addEventListener("dragover", (e) => {
    e.preventDefault();
    zone.classList.add("over");
  });

  zone.addEventListener("dragleave", () => {
    zone.classList.remove("over");
  });

  zone.addEventListener("drop", (e) => {
    e.preventDefault();
    zone.classList.remove("over");

    const draggedText = e.dataTransfer.getData("text");
    const wordEl = [...document.querySelectorAll(".draggable-word")]
      .find(el => el.textContent === draggedText);
    if (wordEl) {
      zone.appendChild(wordEl);
      wordEl.style.position = "static";
    }
  });
});

submitBtn.addEventListener("click", () => {
  let correct = 0;
  let playedCorrect = false;
  let playedWrong = false;

  [...nounZone.children].forEach(el => {
    if (el.classList.contains("draggable-word")) {
      if (el.dataset.type === "noun") {
        el.classList.add("correct");
        el.classList.remove("incorrect");
        correct++;
        if (!playedCorrect) {
          correctAudio.play();
          playedCorrect = true;
        }
      } else {
        el.classList.add("incorrect");
        el.classList.remove("correct");
        if (!playedWrong) {
          wrongAudio.play();
          playedWrong = true;
        }
      }
    }
  });

  [...verbZone.children].forEach(el => {
    if (el.classList.contains("draggable-word")) {
      if (el.dataset.type === "verb") {
        el.classList.add("correct");
        el.classList.remove("incorrect");
        correct++;
        if (!playedCorrect) {
          correctAudio.play();
          playedCorrect = true;
        }
      } else {
        el.classList.add("incorrect");
        el.classList.remove("correct");
        if (!playedWrong) {
          wrongAudio.play();
          playedWrong = true;
        }
      }
    }
  });

  if (correct === currentWords.length) {
    feedbackMessage.textContent = "🎉 Great job! All correct!";
  } else {
    feedbackMessage.textContent = "❌ Oops! Try again with new words.";
  }

  tryAgainBtn.style.display = "inline-block";
});


tryAgainBtn.addEventListener("click", () => {
  generateWords();
});

generateWords();
