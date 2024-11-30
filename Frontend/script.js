document.addEventListener("DOMContentLoaded", function () {
    const imageFrame = document.getElementById("image-frame");
    const fileInput = document.getElementById("file-input");
    const previewImage = document.getElementById("preview-image");
    const uploadPrompt = document.getElementById("upload-prompt");
    const replaceButton = document.getElementById("replace-button");
    const sendButton = document.getElementById("send-button");
    const progressBar = document.getElementById("progress-bar");
    const progress = document.getElementById("progress");
    const resultDiv = document.getElementById("result");
    const genresContainer = document.getElementById("genres-container");

    // Trigger file input when clicking the frame
    imageFrame.addEventListener("click", function () {
        fileInput.click();
    });

    // Replace the image when clicking the replace button
    replaceButton.addEventListener("click", function () {
        fileInput.click();
    });

    // Show send button when an image is selected
    fileInput.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                previewImage.src = e.target.result;
                previewImage.classList.remove("hidden");
                uploadPrompt.classList.add("hidden");
                replaceButton.classList.remove("hidden");
                sendButton.classList.remove("hidden");
            };
            reader.readAsDataURL(file);
        }
    });

    // Handle sending the image to the backend
    sendButton.addEventListener("click", function () {
        const file = fileInput.files[0];
        if (!file) {
            alert("Please select an image first.");
            return;
        }

        // Reset results and progress bar
        genresContainer.innerHTML = "";
        resultDiv.classList.add("hidden");
        progressBar.classList.remove("hidden");
        progress.style.width = "0%";

        // Simulate progress bar
        let uploadProgress = 0;
        const uploadInterval = setInterval(() => {
            uploadProgress += 10;
            progress.style.width = `${uploadProgress}%`;

            if (uploadProgress >= 100) {
                clearInterval(uploadInterval);

                // Send the image to the backend
                const formData = new FormData();
                formData.append("image", file);

                fetch("http://127.0.0.1:5000/predict-genres", {
                    method: "POST",
                    body: formData,
                })
                    .then((response) => response.json())
                    .then((data) => {
                        progressBar.classList.add("hidden");
                        if (data.genres) {
                            resultDiv.classList.remove("hidden");
                            data.genres.forEach((genre) => {
                                const tag = document.createElement("div");
                                tag.className = "tag";
                                tag.textContent = genre;
                                genresContainer.appendChild(tag);
                            });
                        } else {
                            alert("Error: " + (data.error || "Unknown error"));
                        }
                    })
                    .catch((error) => {
                        progressBar.classList.add("hidden");
                        alert("Error: " + error.message);
                    });
            }
        }, 200);
    });
});
