const images = [
    { word: "Cicle", img: "assets/images/shapes/circle.png" },
    { word: "Triangle", img: "assets/images/shapes/triangle.png" },
    { word: "Square", img: "assets/images/shapes/square.png" },
    { word: "Parrot", img: "assets/images/birds/parrot.png" },
    { word: "Apple", img: "assets/images/fruits/apple.png" },
    { word: "Orange", img: "assets/images/fruits/orange.png" },
    { word: "Cherry", img: "assets/images/fruits/cherry.png" },
    { word: "Strawberry", img: "assets/images/fruits/strawberry.png" },
    { word: "Watermelon", img: "assets/images/fruits/watermelon.png" },
    { word: "Owl", img: "assets/images/birds/owl.png" },
    { word: "Hen", img: "assets/images/birds/hen.png" },
    { word: "Eagle", img: "assets/images/birds/eagle.png" },
    { word: "Cat", img: "assets/images/animals/cat.png" },
    { word: "Dog", img: "assets/images/animals/dog.png" },
    { word: "Horse", img: "assets/images/animals/horse.png" },
    { word: "Monkey", img: "assets/images/animals/Monkey.png" },
    { word: "Heart", img: "assets/images/shapes/heart.png" },
    { word: "Star", img: "assets/images/shapes/star.png" }
  ];
  
  const gameContainer = document.getElementById("game-container");
  const correctAudio = document.getElementById("audio-correct");
  const wrongAudio = document.getElementById("audio-wrong");
  
  function getRandomSet() {
    const count = Math.floor(Math.random() * 5) + 2;
    const item = images[Math.floor(Math.random() * images.length)];
    return Array(count).fill(item);
  }
  
  function loadGame() {
  const objectSet = getRandomSet();
  const correctCount = objectSet.length;
  const choices = shuffle([
    correctCount,
    correctCount + 1,
    correctCount - 1,
    correctCount + 2,
  ].filter(n => n > 0)).slice(0, 3);
  choices.push(correctCount);
  const uniqueChoices = shuffle([...new Set(choices)]);

  gameContainer.innerHTML = "";

  const imagesDiv = document.createElement("div");
  imagesDiv.className = "counting-images";
  objectSet.forEach(obj => {
    const img = document.createElement("img");
    img.src = obj.img;
    img.alt = obj.word;
    imagesDiv.appendChild(img);
  });

  const answerDiv = document.createElement("div");
  answerDiv.className = "answer-buttons";

  // ✅ Feedback message element
  const message = document.createElement("div");
  message.id = "feedback-message";
  message.style.fontSize = "24px";
  message.style.fontWeight = "bold";
  message.style.margin = "15px 0";

  uniqueChoices.forEach(choice => {
    const btn = document.createElement("button");
    btn.textContent = choice;
    btn.onclick = () => {
      if (choice === correctCount) {
        correctAudio.play();
        message.textContent = "✅ Correct!";
        message.style.color = "green";
        setTimeout(loadGame, 1000);
      } else {
        wrongAudio.play();
        message.textContent = "❌ Try Again!";
        message.style.color = "red";
      }
    };
    answerDiv.appendChild(btn);
  });

  gameContainer.appendChild(imagesDiv);
  gameContainer.appendChild(answerDiv);
  gameContainer.appendChild(message); // ✅ Append feedback message
}

  
  function shuffle(arr) {
    return arr.sort(() => Math.random() - 0.5);
  }
  
  window.onload = loadGame;
  