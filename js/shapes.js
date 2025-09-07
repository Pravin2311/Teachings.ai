const version = "?v=2"; // increase this number each time you deploy new images

const shapes = [
  { word: "Circle",    img: CDN + "assets/images/shapes/circle.png" + version },
  { word: "Square",    img: CDN + "assets/images/shapes/square.png" + version },
  { word: "Triangle",  img: CDN + "assets/images/shapes/triangle.png" + version },
  { word: "Rectangle", img: CDN + "assets/images/shapes/rectangle.png" + version },
  { word: "Oval",      img: CDN + "assets/images/shapes/oval.png" + version },
  { word: "Star",      img: CDN + "assets/images/shapes/star.png" + version },
  { word: "Heart",     img: CDN + "assets/images/shapes/heart.png" + version },
  { word: "Hexagon",   img: CDN + "assets/images/shapes/hexagon.png" + version },
  { word: "Diamond",   img: CDN + "assets/images/shapes/diamond.png" + version },
  { word: "Crescent",  img: CDN + "assets/images/shapes/crescent.png" + version },
  { word: "Pentagon",  img: CDN + "assets/images/shapes/pentagon.png" + version },
  { word: "Octagon",   img: CDN + "assets/images/shapes/octagon.png" + version }
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
  