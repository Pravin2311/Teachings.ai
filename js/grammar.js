// js/grammar.js

// Word lists
const nounWords = ["dog", "cat", "school", "apple", "car", "tree", "ball", "book", "city", "flower"];
const verbWords = ["run", "jump", "eat", "read", "write", "play", "sleep", "drive", "draw", "sing"];

const wordContainer = document.getElementById("word-container");
const nounZone = document.getElementById("noun-zone");
const verbZone = document.getElementById("verb-zone");
const submitBtn = document.getElementById("submit-btn");
const tryAgainBtn = document.getElementById("try-again-btn");
const feedbackMessage = document.getElementById("feedback-message");

let currentWords = []; // active 8 words

// Shuffle helper
function shuffle(arr) {
  return [...arr].sort(() => Math.random() - 0.5);
}

// Generate a new round (4 nouns + 4 verbs)
function generateRound() {
  feedbackMessage.textContent = "";
  nounZone.innerHTML = "";
  verbZone.innerHTML = "";
  wordContainer.innerHTML = "";

  // Pick 4 random nouns + 4 random verbs
  const selectedNouns = shuffle(nounWords).slice(0, 4).map(w => ({ word: w, type: "noun" }));
  const selectedVerbs = shuffle(verbWords).slice(0, 4).map(w => ({ word: w, type: "verb" }));

  currentWords = shuffle([...selectedNouns, ...selectedVerbs]);

  // Create word bank
  currentWords.forEach(({ word, type }) => {
    const el = document.createElement("div");
    el.classList.add("draggable-word");
    el.textContent = word;
    el.dataset.type = type;
    el.setAttribute("draggable", "true");
    addDragListeners(el);
    wordContainer.appendChild(el);
  });
}

// Drag/drop setup
function addDragListeners(el) {
  el.addEventListener("dragstart", e => {
    e.dataTransfer.setData("text/plain", el.textContent);
    e.dataTransfer.setData("type", el.dataset.type);
    setTimeout(() => el.classList.add("touch-dragging"), 0);
  });

  el.addEventListener("dragend", () => {
    el.classList.remove("touch-dragging");
  });

  // Touch support
  el.addEventListener("touchstart", e => {
    if (e.touches.length !== 1) return;
    e.preventDefault();

    const t = e.touches[0];
    const ghost = el.cloneNode(true);
    ghost.classList.add("touch-dragging");
    ghost.style.position = "fixed";
    ghost.style.left = t.clientX + "px";
    ghost.style.top = t.clientY + "px";
    ghost.style.opacity = "0.85";
    ghost.style.pointerEvents = "none";
    document.body.appendChild(ghost);
    el.ghost = ghost;
  });

  el.addEventListener("touchmove", e => {
    if (!el.ghost) return;
    const t = e.touches[0];
    el.ghost.style.left = t.clientX + "px";
    el.ghost.style.top = t.clientY + "px";
  });

  el.addEventListener("touchend", e => {
    if (el.ghost) {
      document.body.removeChild(el.ghost);
      el.ghost = null;
    }
    const t = e.changedTouches[0];
    const zone = getDropZone(t.clientX, t.clientY);
    if (zone) zone.appendChild(el);
  });

  el.addEventListener("touchcancel", () => {
    if (el.ghost) {
      document.body.removeChild(el.ghost);
      el.ghost = null;
    }
  });
}

// Helper: get drop zone for touch
function getDropZone(x, y) {
  return [nounZone, verbZone].find(zone => {
    const rect = zone.getBoundingClientRect();
    return x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom;
  });
}

// Drop zones (mouse)
[nounZone, verbZone].forEach(zone => {
  zone.addEventListener("dragover", e => {
    e.preventDefault();
    zone.classList.add("over");
  });

  zone.addEventListener("dragleave", () => {
    zone.classList.remove("over");
  });

  zone.addEventListener("drop", e => {
    e.preventDefault();
    zone.classList.remove("over");

    const word = e.dataTransfer.getData("text/plain");
    const el = [...document.querySelectorAll(".draggable-word")].find(c => c.textContent === word);
    if (el) zone.appendChild(el);
  });
});

// Submit check
submitBtn.addEventListener("click", () => {
  let correct = 0;

  const checkZone = (zone, expectedType) => {
    [...zone.children].forEach(el => {
      if (el.classList.contains("draggable-word")) {
        el.classList.remove("correct", "incorrect"); // reset before marking
        if (el.dataset.type === expectedType) {
          el.classList.add("correct");  // ✅ turn green
          correct++;
        } else {
          el.classList.add("incorrect"); // ❌ turn red
        }
      }
    });
  };

  checkZone(nounZone, "noun");
  checkZone(verbZone, "verb");

  if (correct === currentWords.length) {
    feedbackMessage.textContent = "🎉 Great job! All 8 correct!";
    document.getElementById("audio-correct").play().catch(() => {});
  } else {
    feedbackMessage.textContent = `❌ You got ${correct} out of ${currentWords.length} correct.`;
    document.getElementById("audio-wrong").play().catch(() => {});
  }
});

// Try again → new 4+4 set
tryAgainBtn.addEventListener("click", generateRound);

// Init game
window.onload = generateRound;
