document.addEventListener("DOMContentLoaded", function () {
    const summarizeButton = document.getElementById("summarize-btn");
    const loadingMessage = document.getElementById("loading-message");

    if (summarizeButton) {
        summarizeButton.addEventListener("click", function () {
            loadingMessage.style.display = "block"; // Show loading message
        });
    }
});
