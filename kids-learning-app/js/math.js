document.addEventListener('DOMContentLoaded', () => {
    const mathProblemText = document.getElementById('math-problem-text');
    const answerInput = document.getElementById('answer-input');
    const checkAnswerButton = document.getElementById('check-answer-button');
    const newProblemButton = document.getElementById('new-problem-button');
    const feedbackMessage = document.getElementById('feedback-message');

    let currentProblem = {}; // Stores {num1, num2, operator, answer}

    // Audio paths for feedback
    const correctAudioPath = 'assets/audio/math_feedback/correct.mp3';
    const incorrectAudioPath = 'assets/audio/math_feedback/incorrect.mp3';

    function generateProblem() {
        const num1 = Math.floor(Math.random() * 10) + 1; // 1-10
        const num2 = Math.floor(Math.random() * 10) + 1; // 1-10
        const operator = Math.random() < 0.5 ? '+' : '-'; // Randomly choose + or -
        let answer;
        let problemText;

        if (operator === '+') {
            answer = num1 + num2;
            problemText = num1 + ' + ' + num2 + ' = ?';
        } else {
            // Ensure subtraction results in a non-negative number
            if (num1 < num2) {
                // Swap numbers if num1 is smaller to avoid negative results for now
                answer = num2 - num1;
                problemText = num2 + ' - ' + num1 + ' = ?';
            } else {
                answer = num1 - num2;
                problemText = num1 + ' - ' + num2 + ' = ?';
            }
        }
        
        currentProblem = { num1, num2, operator, answer };
        mathProblemText.textContent = problemText;
        answerInput.value = ''; // Clear previous answer
        feedbackMessage.textContent = ''; // Clear previous feedback
        feedbackMessage.className = ''; // Remove feedback styling
        answerInput.focus(); // Focus on input for quick entry
    }

    function checkAnswer() {
        const userAnswer = parseInt(answerInput.value, 10);

        if (isNaN(userAnswer)) {
            feedbackMessage.textContent = 'Please enter a number!';
            feedbackMessage.className = 'incorrect';
            playFeedbackAudio(incorrectAudioPath);
            return;
        }

        if (userAnswer === currentProblem.answer) {
            feedbackMessage.textContent = 'Correct! \uD83C\uDF89'; // Party Popper emoji ??
            feedbackMessage.className = 'correct';
            playFeedbackAudio(correctAudioPath);
        } else {
            feedbackMessage.textContent = 'Try again! \uD83E\uDD14'; // Thinking Face emoji ??
            feedbackMessage.className = 'incorrect';
            playFeedbackAudio(incorrectAudioPath);
        }
    }

    function playFeedbackAudio(audioPath) {
        console.log('Attempting to play feedback audio: ' + audioPath);
        const audio = new Audio(audioPath);

        if (window.pauseBackgroundMusic) {
            window.pauseBackgroundMusic();
        }

        audio.play().catch(e => {
            console.error('Error playing feedback audio: ' + audioPath + ':', e);
        });

        audio.onended = () => {
            if (window.resumeBackgroundMusic) {
                window.resumeBackgroundMusic();
            }
        };
    }

    checkAnswerButton.addEventListener('click', checkAnswer);
    newProblemButton.addEventListener('click', generateProblem);
    
    // Allow checking answer on 'Enter' key press in the input field
    answerInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            checkAnswer();
        }
    });

    // Initial problem generation
    generateProblem();
});
