function hideImages() {
  const paragraphs = document.querySelectorAll("p");
  paragraphs.forEach((paragraph) => {
    const images = paragraph.querySelectorAll("img");
    images.forEach((img) => {
      if (img.style.display === "none") {
        img.style.display = "";
      } else {
        img.style.display = "none";
      }
    });
  });
}
