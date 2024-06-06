document.addEventListener("DOMContentLoaded", function () {
  async function populateTable(filename = "", extension = "") {
    try {
      const response = await fetch(
        `/api/files?filename=${encodeURIComponent(
          filename
        )}&extension=${encodeURIComponent(extension)}`
      );
      if (!response.ok)
        throw new Error(`Network response was not ok: ${response.statusText}`);
      const data = await response.json();
      const tableBody = document.getElementById("files-table");

      if (!tableBody) {
        console.error('Table body with ID "files-table" not found');
        return;
      }

      // Clear the table before appending new rows
      tableBody.innerHTML = "";

      const fragment = document.createDocumentFragment();

      Object.keys(data).forEach((groupId) => {
        const groupUrl = data[groupId]?.group_url;
        const groupFiles = data[groupId]?.files || []; // default to empty array if undefined

        groupFiles.forEach((file, i) => {
          const tr = document.createElement("tr");

          if (i === 0) {
            const tdGroup = document.createElement("td");
            tdGroup.setAttribute("rowspan", groupFiles.length);
            const groupLink = document.createElement("a");
            groupLink.setAttribute("href", groupUrl);
            groupLink.classList.add("page-link");
            groupLink.textContent = groupId;
            tdGroup.appendChild(groupLink);
            tr.appendChild(tdGroup);
          }

          const tdFilename = document.createElement("td");
          const fileLink = document.createElement("a");
          fileLink.setAttribute("href", file?.file_url);
          fileLink.classList.add("page-link");
          fileLink.textContent = file?.filename;
          tdFilename.appendChild(fileLink);
          tr.appendChild(tdFilename);

          const tdFilesize = document.createElement("td");
          tdFilesize.textContent = file?.file_size;
          tr.appendChild(tdFilesize);

          const tdThumbnails = document.createElement("td");
          tdThumbnails.classList.add("thumbnails");
          const thumbnailUrls = file?.thumbnail_urls || [];
          thumbnailUrls.forEach((url) => {
            const img = document.createElement("img");
            img.setAttribute("src", url);
            tdThumbnails.appendChild(img);
          });
          tr.appendChild(tdThumbnails);

          fragment.appendChild(tr);
        });
      });

      tableBody.appendChild(fragment);
    } catch (error) {
      console.error("Failed to fetch and populate table:", error);
    }
  }

  const form = document.getElementById("filter-form");
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    const filename = document.getElementById("filename").value;
    const extension = document.getElementById("extension").value;
    populateTable(filename, extension);
  });

  populateTable();
});
