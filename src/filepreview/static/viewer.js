// Add launch button when applicable
document.addEventListener("DOMContentLoaded", function () {
  const launchButton = document.getElementById("launchButton");

  function addLaunchEffect() {
    const md5 = launchButton.dataset.md5;
    fetch(`/api/program/${md5}`)
      .then((response) => response.json())
      .then((data) => {
        launchButton.textContent = `Open with ${data.program_name}`;
        launchButton.addEventListener("click", () => {
          const launchUrl = `/launch?application=${data.program_exe}&local_path=${data.local_path}`;
          fetch(launchUrl);
        });
        showLaunchButton();
      })
      .catch((error) => {
        console.error("Error fetching program:", error);
        hideLaunchButton();
      });
  }

  function showLaunchButton() {
    launchButton.style.display = "inline-block";
  }

  function hideLaunchButton() {
    launchButton.style.display = "none";
  }

  addLaunchEffect();
});

function launch(launchUrl) {
  fetch(launchUrl).then((response) => {
    if (response.ok) {
      console.log("Launch Succeeded");
    } else {
      console.error("Launch Failed");
    }
  });
}

// Show viewer with images loaded from AJAX query
// Hide viewer if there are no images
document.addEventListener("DOMContentLoaded", function () {
  const viewer = document.getElementById("viewer");
  const imageElement = document.getElementById("currentImage");
  const imageIndicator = document.getElementById("imageIndicator");
  const prevButton = document.getElementById("prev");
  const nextButton = document.getElementById("next");
  let images = [];
  let currentIndex = 0;

  function fetchImages() {
    const groupId = viewer.dataset.groupId;
    const directory = viewer.dataset.directory;
    const filename = viewer.dataset.filename;
    fetch(
      `/api/images?group_id=${groupId}&directory=${directory}&filename=${filename}`
    )
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

  prevButton.addEventListener("click", () => {
    currentIndex = currentIndex > 0 ? currentIndex - 1 : images.length - 1;
    updateImage(currentIndex);
  });

  nextButton.addEventListener("click", () => {
    currentIndex = currentIndex < images.length - 1 ? currentIndex + 1 : 0;
    updateImage(currentIndex);
  });

  fetchImages();
});
