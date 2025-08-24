document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("img").forEach(img => {
    // lazy loading if not set
    if (!img.hasAttribute("loading")) {
      img.setAttribute("loading", "lazy");
    }
    // async decode to prevent blocking rendering
    if (!img.hasAttribute("decoding")) {
      img.setAttribute("decoding", "async");
    }
  });
});
