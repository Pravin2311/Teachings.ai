const questions = [
    { type: "next", pattern: ["🍎", "🍌", "🍎", "🍌", "?"], options: ["🍎", "🍌", "🍇"], answer: "🍎" },
    { type: "complete", pattern: ["🐶", "🐶", "❓", "🐶", "🐶"], options: ["🐱", "🐶", "🐭"], answer: "🐶" },
    { type: "next", pattern: ["🟦", "🟩", "🟦", "🟩", "?"], options: ["🟥", "🟦", "🟨"], answer: "🟦" },
    { type: "complete", pattern: ["🌞", "🌛", "🌞", "❓", "🌞"], options: ["🌛", "🌞", "⭐"], answer: "🌛" },
    { type: "next", pattern: ["🐱", "🐭", "🐱", "🐭", "?"], options: ["🐶", "🐱", "🐭"], answer: "🐱" },
    { type: "complete", pattern: ["🍉", "🍉", "🍉", "❓", "🍉"], options: ["🍓", "🍍", "🍉"], answer: "🍉" },
    { type: "next", pattern: ["⭐", "🌟", "⭐", "🌟", "?"], options: ["⭐", "🌟", "✨"], answer: "⭐" },
    { type: "complete", pattern: ["🚗", "🚌", "🚗", "❓", "🚗"], options: ["🚌", "🚗", "🚕"], answer: "🚌" },
    { type: "next", pattern: ["👕", "👖", "👕", "👖", "?"], options: ["👖", "👕", "👗"], answer: "👕" },
    { type: "complete", pattern: ["🍔", "🍟", "🍔", "❓", "🍔"], options: ["🍟", "🍔", "🌭"], answer: "🍟" },
    { type: "next", pattern: ["🌈", "☀️", "🌈", "☀️", "?"], options: ["☀️", "🌈", "⛅"], answer: "🌈" },
    { type: "complete", pattern: ["🧁", "🎂", "🧁", "❓", "🧁"], options: ["🍰", "🎂", "🧁"], answer: "🎂" },
    { type: "next", pattern: ["⚽", "🏀", "⚽", "🏀", "?"], options: ["🏈", "⚽", "🏀"], answer: "⚽" },
    { type: "complete", pattern: ["🖍️", "✏️", "🖍️", "❓", "🖍️"], options: ["✏️", "🖍️", "🖊️"], answer: "✏️" },
    { type: "next", pattern: ["🎵", "🎶", "🎵", "🎶", "?"], options: ["🎶", "🎵", "🔔"], answer: "🎵" },
    { type: "complete", pattern: ["🏡", "🏢", "🏡", "❓", "🏡"], options: ["🏢", "🏡", "🏠"], answer: "🏢" },
    { type: "next", pattern: ["🍇", "🍓", "🍇", "🍓", "?"], options: ["🍓", "🍇", "🍒"], answer: "🍇" },
    { type: "complete", pattern: ["📕", "📘", "📕", "❓", "📕"], options: ["📘", "📕", "📗"], answer: "📘" },
    { type: "next", pattern: ["🐔", "🐣", "🐔", "🐣", "?"], options: ["🐣", "🐔", "🐤"], answer: "🐔" },
    { type: "complete", pattern: ["🎈", "🎉", "🎈", "❓", "🎈"], options: ["🎉", "🎈", "🎁"], answer: "🎉" }
  ];
  
  let currentQuestion = 0;

function loadQuestion() {
  const q = questions[currentQuestion];
  const patternArea = document.getElementById("pattern-question");
  const optionsArea = document.getElementById("pattern-options");
  const feedback = document.getElementById("feedback-message");

  feedback.textContent = "";

  // Load pattern
  const patternHTML = q.pattern.map(p => `<span>${p}</span>`).join(" ");
  patternArea.innerHTML = patternHTML;

  // Load options
  optionsArea.innerHTML = "";
  q.options.forEach(opt => {
    const btn = document.createElement("button");
    btn.className = "option";
    btn.textContent = opt;
    btn.onclick = () => checkAnswer(opt);
    optionsArea.appendChild(btn);
  });
}

function checkAnswer(selected) {
  const correctSound = document.getElementById("audio-correct");
  const incorrectSound = document.getElementById("audio-wrong");
  const feedback = document.getElementById("feedback-message");

  if (selected === questions[currentQuestion].answer) {
    correctSound.play();
    feedback.textContent = "✅ Correct!";
    feedback.className = "correct";
  } else {
    incorrectSound.play();
    feedback.textContent = "❌ Try again!";
    feedback.className = "incorrect";
    return;
  }

  setTimeout(() => {
    currentQuestion++;
    if (currentQuestion < questions.length) {
      loadQuestion();
    } else {
      document.getElementById("pattern-question").innerHTML = "<h3>🎉 Great job! You've completed all patterns!</h3>";
      document.getElementById("pattern-options").innerHTML = "";
      feedback.textContent = "";
    }
  }, 1500);
}

document.getElementById("next-pattern-btn").onclick = () => {
    currentQuestion++;
    if (currentQuestion < questions.length) {
      loadQuestion();
    } else {
      document.getElementById("pattern-question").innerHTML = "<h3>🎉 Great job! You've completed all patterns!</h3>";
      document.getElementById("pattern-options").innerHTML = "";
      document.getElementById("feedback-message").textContent = "";
    }
  };
  

if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", loadQuestion); else loadQuestion();