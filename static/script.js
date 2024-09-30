let generate = document.querySelector(".generate");
let plotImage = document.querySelector("#plot-image");
let form = document.querySelector("#uploadForm");


generate.addEventListener("click", (event) => {
  event.preventDefault();
  fetch("/generate-dataset", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      // Now send this dataset to the /plot endpoint
      return fetch("/plot", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data), // Send the dataset to the server
      });
    })
    .then((response) => response.json())
    .then((plotData) => {
      // Update the page with the new plot
      plotImage.src = plotData.plot_url + "?t=" + new Date().getTime(); // Add timestamp to avoid caching
      plotImage.style.display = "block"; // Show the plot image
    })
    .catch((error) => console.error("Error:", error));
});
