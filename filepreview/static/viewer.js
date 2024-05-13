// Using Ajax to get image urls because they can't be stored as JSON data
// in the viewer html element
document.addEventListener("DOMContentLoaded", function () {
  const viewer = document.getElementById("viewer");
  const imageElement = document.getElementById("currentImage");
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
          updateImage(0);
        }
      })
      .catch((error) => console.error("Error fetching images:", error));
  }

  function updateImage(index) {
    imageElement.src = images[index];
    document.getElementById("imageInfo").textContent = `Image ${index + 1} of ${
      images.length
    }`;
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
