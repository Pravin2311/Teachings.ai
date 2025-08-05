const words = [
  { word: "dog", type: "noun" },
  { word: "run", type: "verb" },
  { word: "cat", type: "noun" },
  { word: "jump", type: "verb" },
  { word: "apple", type: "noun" },
  { word: "eat", type: "verb" },
  { word: "ball", type: "noun" },
  { word: "swim", type: "verb" }
];

function shuffle(array) {
  return array.sort(() => Math.random() - 0.5);
}

window.onload = function () {
  const shuffled = shuffle([...words]);
  const wordContainer = document.getElementById("word-container");

  shuffled.forEach(({ word }, index) => {
    const span = document.createElement("span");
    span.innerText = word;
    span.className = "word";
    span.setAttribute("draggable", true);
    span.setAttribute("data-word", word);
    span.setAttribute("data-index", index);
    wordContainer.appendChild(span);
  });

  document.querySelectorAll(".word").forEach(el => {
    el.addEventListener("dragstart", e => {
      e.dataTransfer.setData("text/plain", e.target.dataset.index);
    });
  });

  document.querySelectorAll(".drop-zone").forEach(zone => {
    zone.addEventListener("dragover", e => e.preventDefault());
    zone.addEventListener("drop", e => {
      e.preventDefault();
      const index = e.dataTransfer.getData("text/plain");
      const item = document.querySelector(`[data-index='${index}']`);
      if (item && !zone.contains(item)) {
        zone.appendChild(item);
      }
    });
  });

  document.getElementById("submit-btn").addEventListener("click", () => {
    let score = 0;

    document.querySelectorAll(".drop-zone").forEach(zone => {
      const zoneType = zone.getAttribute("data-type");
      zone.querySelectorAll(".word").forEach(wordEl => {
        const wordText = wordEl.innerText;
        const correct = words.find(w => w.word === wordText);
        if (correct && correct.type === zoneType) {
          wordEl.classList.remove("incorrect");
          wordEl.classList.add("correct");
          score++;
          document.getElementById("audio-correct").play();
        } else {
          wordEl.classList.remove("correct");
          wordEl.classList.add("incorrect");
          document.getElementById("audio-wrong").play();
        }
      });
    });

    document.getElementById("feedback-message").innerText =
      `✅ You got ${score} out of ${words.length} correct!`;
  });
};
