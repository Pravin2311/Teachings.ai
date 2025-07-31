// js/script.js
document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".module-button");
  buttons.forEach(button => {
    button.addEventListener("click", () => {
      const id = button.id;
      if (id) {
        window.location.href = `${id}.html`;
      }
    });
  });
});
