document.addEventListener("DOMContentLoaded", function () {
  async function populateTable() {
    const response = await fetch(`/data`);
    const data = await response.json();
    const tableBody = document.getElementById("files-table");

    Object.keys(data).forEach((groupId) => {
      const groupUrl = data[groupId]["group_url"];
      const groupFiles = data[groupId]["files"]; // list of file objects

      groupFiles.forEach((file, i) => {
        const tr = document.createElement("tr");

        if (i === 0) {
          const tdGroup = document.createElement("td");
          tdGroup.setAttribute("rowspan", groupFiles.length);
          const a = document.createElement("a");
          a.setAttribute("href", groupUrl);
          a.classList.add("page-link");
          a.textContent = groupId;
          tdGroup.appendChild(a);
          tr.appendChild(tdGroup);
        }

        const tdFilename = document.createElement("td");
        const a = document.createElement("a");
        a.setAttribute("href", file["file_url"]);
        a.classList.add("page-link");
        a.textContent = file["filename"];
        tdFilename.appendChild(a);
        tr.appendChild(tdFilename);

        const tdFilesize = document.createElement("td");
        tdFilesize.textContent = file["file_size"];
        tr.appendChild(tdFilesize);

        const tdThumbnails = document.createElement("td");
        tdThumbnails.classList.add("thumbnails");
        const thumbnailUrls = file["thumbnail_urls"];
        thumbnailUrls.forEach((url) => {
          const img = document.createElement("img");
          img.setAttribute("src", url);
          tdThumbnails.appendChild(img);
        });
        tr.appendChild(tdThumbnails);

        tableBody.appendChild(td);
      });
    });
  }

  populateTable();
});
