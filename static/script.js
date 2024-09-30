let generate = document.querySelector(".generate");
let plotImage = document.querySelector("#plot-image");
let form = document.querySelector("#uploadForm")

generate.addEventListener("click", (event) => {
  fetch("/generate-dataset", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("New Dataset:", data);

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
      console.log("Plot URL:", plotData.plot_url);

      // Update the page with the new plot
      plotImage.src = plotData.plot_url + "?t=" + new Date().getTime(); // Add timestamp to avoid caching
      plotImage.style.display = "block"; // Show the plot image
    })
    .catch((error) => console.error("Error:", error));
});

// convergence.addEventListener("click", () => {
//   const kClusters = document.getElementById("k_clusters").value;
//   console.log(kClusters)
//   const initializationMethod = document.getElementById("initialization_method").value;
//   console.log(initializationMethod)


//   fetch("/plot", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//     body: JSON.stringify({
//       k: kClusters,
//       initialization_method: initializationMethod,
//     }),
//   })
//     .then((response) => response.json())
//     .then((convergenceData) => {
//       console.log("Convergence URL:", convergenceData.convergence_url);

//       // Update the page with the converged plot
//       plotImage.src = convergenceData.convergence_url + "?t=" + new Date().getTime(); // Add timestamp to avoid caching
//       plotImage.style.display = "block"; // Show the plot image
//     })
//     .catch((error) => console.error("Error:", error));
// });












// async function submitToBoth() {
//   const form = document.getElementById("uploadForm");
//   const formData = new FormData(form);

//   try {
//     // Send to /
//     const response1 = await fetch("/", {
//       method: "POST",
//       body: formData,
//     });

//     if (!response1.ok) {
//       throw new Error("Failed to submit to /");
//     }

//     // Optionally handle the response if needed
//     const result1 = await response1.json();
//     console.log("Response from /:", result1);

//     // Send to /generate
//     const response2 = await fetch("/generate", {
//       method: "POST",
//       body: formData,
//     });

//     if (!response2.ok) {
//       throw new Error("Failed to submit to /generate");
//     }

//     // Optionally handle the response if needed
//     const result2 = await response2.json();
//     console.log("Response from /generate:", result2);
//   } catch (error) {
//     console.error("Error:", error);
//   }
// }
