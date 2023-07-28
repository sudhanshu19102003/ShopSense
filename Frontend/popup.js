// scrape_script.js
document.addEventListener("DOMContentLoaded", function () {
    // Get the current tab's URL using the Chrome tabs API
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const link = tabs[0].url; // Get the URL of the active tab
        const data = {
            website_link: link
        };

        // Sending a POST request to the server
        fetch("http://127.0.0.1:5000/scrape", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            // Displaying the result in the paragraph with id "status"
            document.getElementById("status").innerText = JSON.stringify(result);
        })
        .catch(error => {
            document.getElementById("status").innerText = "Error: " + error.message;
        });
    });
});
