const shapes = [
    { word: "Circle", img: "assets/images/shapes/circle.jpg" },
    { word: "Square", img: "assets/images/shapes/square.jpg" },
    { word: "Triangle", img: "assets/images/shapes/triangle.jpg" },
    { word: "Rectangle", img: "assets/images/shapes/rectangle.jpg" },
    { word: "Oval", img: "assets/images/shapes/oval.jpg" },
    { word: "Star", img: "assets/images/shapes/star.jpg" },
    { word: "Heart", img: "assets/images/shapes/heart.jpg" },
    { word: "Hexagon", img: "assets/images/shapes/hexagon.jpg" },
    { word: "Diamond", img: "assets/images/shapes/diamond.jpg" },
    { word: "Crescent", img: "assets/images/shapes/crescent.jpg" },
    { word: "Pentagon", img: "assets/images/shapes/pentagon.jpg" },
    { word: "Octagon", img: "assets/images/shapes/octagon.jpg" }
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
  