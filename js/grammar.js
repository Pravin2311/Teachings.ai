// js/grammar.js
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

function shuffle(arr) {
  return [...arr].sort(() => Math.random() - 0.5);
}

function generateWords() {
  wordContainer.innerHTML = "";

  // Clear only draggable words from zones
  [...nounZone.children, ...verbZone.children]
    .forEach(child => {
      if (child.classList?.contains("draggable-word")) child.remove();
    });

  feedbackMessage.textContent = "";
  tryAgainBtn.style.display = "none";

  const selectedNouns = shuffle(nounWords).slice(0, 4).map(w => ({ word: w, type: "noun" }));
  const selectedVerbs = shuffle(verbWords).slice(0, 4).map(w => ({ word: w, type: "verb" }));
  currentWords = shuffle([...selectedNouns, ...selectedVerbs]);

  currentWords.forEach(({ word, type }) => {
    const el = document.createElement("div");
    el.className = "draggable-word";
    el.textContent = word;
    el.dataset.type = type;
    addDragListeners(el);
    wordContainer.appendChild(el);
  });
}

function addDragListeners(el) {
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

  // Touch
  el.addEventListener("touchstart", (e) => {
    if (e.touches.length !== 1) return;
    e.preventDefault();
    el.classList.add("dragging");
    document.body.classList.add("dragging");

    const t = e.touches[0];
    el.startX = t.clientX - el.offsetLeft;
    el.startY = t.clientY - el.offsetTop;

    const clone = el.cloneNode(true);
    clone.classList.add("touch-dragging");
    clone.style.left = `${el.offsetLeft}px`;
    clone.style.top = `${el.offsetTop}px`;
    document.body.appendChild(clone);
    el.clone = clone;
  });

  el.addEventListener("touchmove", (e) => {
    e.preventDefault();
    if (!el.clone) return;
    const t = e.touches[0];
    el.clone.style.left = `${t.clientX - el.startX}px`;
    el.clone.style.top = `${t.clientY - el.startY}px`;

    const zone = getDropZone(t.clientX, t.clientY);
    [nounZone, verbZone].forEach(z => {
      z.classList.toggle("over", z === zone);
    });
  });

  el.addEventListener("touchend", (e) => {
    document.body.classList.remove("dragging");
    el.classList.remove("dragging");
    if (el.clone) document.body.removeChild(el.clone);

    const t = e.changedTouches[0];
    const zone = getDropZone(t.clientX, t.clientY);
    if (zone) zone.appendChild(el);

    [nounZone, verbZone].forEach(z => z.classList.remove("over"));
    el.clone = null;
  });
}

function getDropZone(x, y) {
  const rects = [
    { el: nounZone, rect: nounZone.getBoundingClientRect() },
    { el: verbZone, rect: verbZone.getBoundingClientRect() }
  ];
  for (const { el, rect } of rects) {
    if (x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom) {
      return el;
    }
  }
  return null;
}

// Mouse drop
[nounZone, verbZone].forEach(zone => {
  zone.addEventListener("dragover", e => e.preventDefault());
  zone.addEventListener("drop", e => {
    e.preventDefault();
    const text = e.dataTransfer.getData("text");
    const el = [...wordContainer.children].find(w => w.textContent === text);
    if (el) zone.appendChild(el);
  });
});

// Submit
submitBtn.addEventListener("click", () => {
  let correct = 0;
  let playedCorrect = false;
  let playedWrong = false;

  const checkZone = (zone, expectedType) => {
    [...zone.children].forEach(child => {
      if (child.classList.contains("draggable-word")) {
        if (child.dataset.type === expectedType) {
          child.classList.add("correct");
          correct++;
          if (!playedCorrect) {
            correctAudio.play().catch(() => {});
            playedCorrect = true;
          }
        } else {
          child.classList.add("incorrect");
          if (!playedWrong) {
            wrongAudio.play().catch(() => {});
            playedWrong = true;
          }
        }
      }
    });
  };

  checkZone(nounZone, "noun");
  checkZone(verbZone, "verb");

  feedbackMessage.textContent = 
    correct === currentWords.length 
      ? "🎉 Great job! All correct!" 
      : `❌ Oops! ${correct} out of ${currentWords.length} correct.`;

  tryAgainBtn.style.display = "inline-block";
});

tryAgainBtn.addEventListener("click", generateWords);

// Init
generateWords();