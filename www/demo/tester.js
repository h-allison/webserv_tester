document.getElementById('submitBtn').addEventListener('click', function() {
    // 1. Get the value from the input field
    const bodyData = document.getElementById('requestBody').value;
    const statusElement = document.getElementById('status');

    statusElement.textContent = "Sending...";

    // 2. Define the path to your CGI script
    const cgiUrl = '/scripts/post_body.sh'; 

    // 3. Make the fetch request
    fetch(cgiUrl, {
        method: 'POST', // HTTP/1.0 uses POST for sending body data
        headers: {
            'Content-Type': 'text/plain', // Tells the server it's raw text
        },
        body: bodyData // This becomes the request body
    })
    .then(response => {
        if (response.ok) {
            statusElement.textContent = "Success! File created.";
            statusElement.style.color = "green";
        } else {
            statusElement.textContent = `Server responded with status: ${response.status}`;
            statusElement.style.color = "red";
        }
    })
    .catch(error => {
        console.error('Error:', error);
        statusElement.textContent = "Network error or server down.";
        statusElement.style.color = "red";
    });
});