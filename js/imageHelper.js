/**
 * Create a <picture> element with WebP + PNG fallback
 * @param {string} basePath - Path without extension (e.g. "assets/images/animals/dog")
 * @param {string} altText - Alt text for accessibility
 * @param {string} [className] - Optional CSS class
 * @returns {HTMLElement} <picture> element
 */
function createPicture(basePath, altText, className = "") {
  const picture = document.createElement("picture");

  // WebP source
  const sourceWebP = document.createElement("source");
  sourceWebP.srcset = `${basePath}.webp`;
  sourceWebP.type = "image/webp";
  picture.appendChild(sourceWebP);

  // PNG fallback
  const img = document.createElement("img");
  img.src = `${basePath}.png`;
  img.alt = altText;
  if (className) img.className = className;
  picture.appendChild(img);

  return picture;
}
