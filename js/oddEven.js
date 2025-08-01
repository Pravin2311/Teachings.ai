let currentNumber = 0;

function getRandomNumber() {
  return Math.floor(Math.random() * 100);
}

function nextQuestion() {
  currentNumber = getRandomNumber();
  document.getElementById('number-display').textContent = currentNumber;
}

function checkAnswer(userAnswer) {
  const feedback = document.getElementById('feedback-message');
  const isEven = currentNumber % 2 === 0;

  if ((userAnswer === 'even' && isEven) || (userAnswer === 'odd' && !isEven)) {
    feedback.textContent = "✅ Correct!";
    feedback.className = "correct";
    document.getElementById('audio-correct').play();
  } else {
    feedback.textContent = "❌ Try Again!";
    feedback.className = "wrong";
    document.getElementById('audio-wrong').play();
  }

  setTimeout(() => {
    feedback.textContent = "";
    nextQuestion();
  }, 1500);
}

// Initialize game on load
window.onload = () => {
  nextQuestion();
};
