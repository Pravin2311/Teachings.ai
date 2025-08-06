const plants = [
  {
    name: "Sunflower",
    image: "assets/images/plants/sunflower.png",
    audio: "assets/audio/plants/sunflower.mp3"
  },
  {
    name: "Rose",
    image: "assets/images/plants/rose.png",
    audio: "assets/audio/plants/rose.mp3"
  },
  {
    name: "Cactus",
    image: "assets/images/plants/cactus.png",
    audio: "assets/audio/plants/cactus.mp3"
  },
  {
    name: "Bamboo",
    image: "assets/images/plants/bamboo.png",
    audio: "assets/audio/plants/bamboo.mp3"
  },
  {
    name: "Fern",
    image: "assets/images/plants/fern.png",
    audio: "assets/audio/plants/fern.mp3"
  },
  {
    name: "Lotus",
    image: "assets/images/plants/lotus.png",
    audio: "assets/audio/plants/lotus.mp3"
  },
  {
    name: "Mango_tree",
    image: "assets/images/plants/mango_tree.png",
    audio: "assets/audio/plants/mango_tree.mp3"
  },
  {
    name: "Banana_plant",
    image: "assets/images/plants/banana_plant.png",
    audio: "assets/audio/plants/banana_plant.mp3"
  },
  {
    name: "Tulip",
    image: "assets/images/plants/tulip.png",
    audio: "assets/audio/plants/tulip.mp3"
  },
  {
    name: "Aloe_vera",
    image: "assets/images/plants/aloe_vera.png",
    audio: "assets/audio/plants/aloe_vera.mp3"
  },

  // Add more plants here
];

let currentIndex = 0;

const nameEl = document.getElementById('current-plant-name');
const imageEl = document.getElementById('plant-image');
const audioEl = document.getElementById('plant-audio');

function showPlant(index) {
  const plant = plants[index];
  nameEl.textContent = plant.name;
  imageEl.src = plant.image;
  audioEl.src = plant.audio;
  audioEl.play();
}

document.getElementById('prev-plant').addEventListener('click', () => {
  currentIndex = (currentIndex - 1 + plants.length) % plants.length;
  showPlant(currentIndex);
});

document.getElementById('next-plant').addEventListener('click', () => {
  currentIndex = (currentIndex + 1) % plants.length;
  showPlant(currentIndex);
});

window.onload = () => showPlant(currentIndex);
