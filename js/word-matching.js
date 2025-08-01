document.addEventListener("DOMContentLoaded", () => {
    const data = [
      { word: "Lion", img: "assets/images/animals/lion.png" },
      { word: "Elephant", img: "assets/images/animals/elephant.png" },
      { word: "Peacock", img: "assets/images/birds/peacock.png" },
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
      { word: "Tiger", img: "assets/images/animals/tiger.png" },
      { word: "Bear", img: "assets/images/animals/bear.png" },
      // Add more items...
    ];
  
    const gameContainer = document.getElementById("game-container");
    const correctSound = document.getElementById("correct-sound");
    const wrongSound = document.getElementById("wrong-sound");
  
    function startGame() {
      gameContainer.innerHTML = "";
  
      const mode = Math.random() < 0.5 ? "imageToWord" : "wordToImage";
      const correct = getRandomItem(data);
      let options = shuffle([correct, ...getRandomOptions(correct, 2)]);
  
      if (mode === "imageToWord") {
        // Show image, ask for matching word
        const img = document.createElement("img");
        img.src = correct.img;
        img.className = "matching-image";
        gameContainer.appendChild(img);
  
        const buttons = document.createElement("div");
        buttons.className = "word-buttons";
        options.forEach(opt => {
          const btn = document.createElement("button");
          btn.className = "word-button";
          btn.innerText = opt.word;
          btn.onclick = () => checkAnswer(opt.word === correct.word);
          buttons.appendChild(btn);
        });
        gameContainer.appendChild(buttons);
      } else {
        // Show word, ask for matching image
        const wordPrompt = document.createElement("p");
        wordPrompt.className = "prompt";
        wordPrompt.innerHTML = `Tap the image for <strong>${correct.word}</strong>`;
        gameContainer.appendChild(wordPrompt);
  
        const imageRow = document.createElement("div");
        imageRow.className = "image-row";
        options.forEach(opt => {
          const img = document.createElement("img");
          img.src = opt.img;
          img.className = "option-image";
          img.onclick = () => checkAnswer(opt.word === correct.word);
          imageRow.appendChild(img);
        });
        gameContainer.appendChild(imageRow);
      }
    }
  
    function getRandomItem(arr) {
      return arr[Math.floor(Math.random() * arr.length)];
    }
  
    function getRandomOptions(exclude, count) {
      return shuffle(data.filter(item => item.word !== exclude.word)).slice(0, count);
    }
  
    function checkAnswer(isCorrect) {
      gameContainer.innerHTML = isCorrect 
        ? `<p class="correct">✅ Correct!</p>` 
        : `<p class="wrong">❌ Try Again!</p>`;
  
      (isCorrect ? correctSound : wrongSound).play();
  
      const next = document.createElement("button");
      next.className = "next-button";
      next.innerText = "Next";
      next.onclick = startGame;
      gameContainer.appendChild(next);
    }
  
    function shuffle(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
      return array;
    }
  
    startGame();
  });
  