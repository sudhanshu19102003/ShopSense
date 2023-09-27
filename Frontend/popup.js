// Wait for the DOM to be fully loaded
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
                // Displaying the result in the paragraph with id "title"
                document.getElementById("title").innerText = result["product_title"];
                // Displaying the result in the paragraph with id "summary"
                document.getElementById("summary").innerText = result["product_description"];

                // Update the rating value
                const newRating = result["top_comments"];
                document.getElementById("rating").innerText = newRating;

                // Trigger a custom event to notify other parts of the code about the rating change
                var ratingEvent = new Event("ratingUpdated");
                document.getElementById("rating").dispatchEvent(ratingEvent);

                // Trigger the progress bar update
                var progressBarEvent = new Event("progressBarUpdate");
                document.dispatchEvent(progressBarEvent);
            })
            .catch(error => {
                // Handle errors by displaying them in the paragraph with id "status"
                document.getElementById("error").innerText = "Error in scrapeing: " + error.message;
            });
    });

    // Adding an event listener to the "sendButton" element
    const addButton = document.getElementById("sendButton");
    const container = document.getElementById("container");
    const textInput = document.getElementById("inputfield");

    addButton.addEventListener("click", function () {
        const inputValue = textInput.value;

        if (inputValue.trim() !== "") {
            // Create a new div element and add it to the container
            const newDiv = document.createElement("div");
            newDiv.className = "summary"
            newDiv.textContent = inputValue;
            container.appendChild(newDiv);
            textInput.value = "";

            // Send the input to the Flask server
            fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ input: inputValue }),
            })
                .then(response => response.json())
                .then(data => {
                    // Display the server's response in a new div
                    const responseDiv = document.createElement("div");
                    responseDiv.className = "flex-container"
                    responseDiv.textContent = "Server Response: " + data.response;
                    container.appendChild(responseDiv);
                })
                .catch(error => {
                    document.getElementById("error").innerText = "Error in chat: " + error.message;
                });
        }
    });
});