document.addEventListener("DOMContentLoaded", function () {
  const viewer = document.getElementById("viewer");
  const imageElement = document.getElementById("currentImage");
  const imageIndicator = document.getElementById("image-indicator");
  const prevButton = document.getElementById("prev");
  const nextButton = document.getElementById("next");
  let images = [];
  let currentIndex = 0;

  function fetchImages() {
    const groupId = viewer.dataset.groupId;
    const filePath = viewer.dataset.filePath;
    fetch(`/api/images?group_id=${groupId}&file_path=${filePath}`)
      .then((response) => response.json())
      .then((data) => {
        images = data;
        if (images.length > 0) {
          createImageIndicators(images.length);
          updateImage(0);
          showViewerElements();
        } else {
          hideViewerElements();
        }
      })
      .catch((error) => {
        console.error("Error fetching images:", error);
        hideViewerElements();
      });
  }

  function createImageIndicators(count) {
    imageIndicator.innerHTML = "";
    for (let i = 0; i < count; i++) {
      const dot = document.createElement("div");
      dot.classList.add("dot");
      if (i === currentIndex) {
        dot.classList.add("active");
      }
      imageIndicator.appendChild(dot);
    }
  }

  function updateImage(index) {
    imageElement.src = images[index];
    currentIndex = index;
    updateImageIndicators();
  }

  function updateImageIndicators() {
    const dots = imageIndicator.querySelectorAll(".dot");
    dots.forEach((dot, index) => {
      dot.classList.toggle("active", index === currentIndex);
    });
  }

  function showViewerElements() {
    imageIndicator.style.display = "flex";
    viewer.style.display = "flex";
    prevButton.style.display = "block";
    imageElement.style.display = "block";
    nextButton.style.display = "block";
  }

  function hideViewerElements() {
    imageIndicator.style.display = "none";
    viewer.style.display = "none";
    prevButton.style.display = "none";
    imageElement.style.display = "none";
    nextButton.style.display = "none";
  }

  document.getElementById("prev").addEventListener("click", () => {
    currentIndex = currentIndex > 0 ? currentIndex - 1 : images.length - 1;
    updateImage(currentIndex);
  });

  document.getElementById("next").addEventListener("click", () => {
    currentIndex = currentIndex < images.length - 1 ? currentIndex + 1 : 0;
    updateImage(currentIndex);
  });

  fetchImages();
});
