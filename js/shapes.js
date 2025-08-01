const shapes = [
    { word: "Circle", img: "assets/images/shapes/circle.png" },
    { word: "Square", img: "assets/images/shapes/square.png" },
    { word: "Triangle", img: "assets/images/shapes/triangle.png" },
    { word: "Rectangle", img: "assets/images/shapes/rectangle.png" },
    { word: "Oval", img: "assets/images/shapes/oval.png" },
    { word: "Star", img: "assets/images/shapes/star.png" },
    { word: "Heart", img: "assets/images/shapes/heart.png" },
    { word: "Hexagon", img: "assets/images/shapes/hexagon.png" }
  ];
  
  let currentShape;
  
  function shuffle(array) {
    return array.sort(() => 0.5 - Math.random());
  }
  
  function loadGame() {
    const container = document.getElementById("game-container");
    container.innerHTML = "";
  
    currentShape = shapes[Math.floor(Math.random() * shapes.length)];
  
    const img = document.createElement("img");
    img.src = currentShape.img;
    img.className = "shape-img";
    container.appendChild(img);
  
    const options = document.createElement("div");
    options.className = "options";
  
    shuffle(shapes).slice(0, 3).concat(currentShape).sort(() => 0.5 - Math.random()).forEach(shape => {
      const btn = document.createElement("button");
      btn.className = "option-button";
      btn.textContent = shape.word;
      btn.onclick = () => handleAnswer(shape.word);
      options.appendChild(btn);
    });
  
    container.appendChild(options);
  }
  
  function handleAnswer(selected) {
    const feedback = document.getElementById("feedback");
    const correctSound = document.getElementById("audio-correct");
    const wrongSound = document.getElementById("audio-wrong");
  
    if (selected === currentShape.word) {
      feedback.textContent = "✅ Correct!";
      correctSound.play();
    } else {
      feedback.textContent = "❌ Try again!";
      wrongSound.play();
    }
  
    setTimeout(loadGame, 1500);
  }
  
  window.onload = loadGame;
  