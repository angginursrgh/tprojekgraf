const startInput = document.getElementById("start");
const endInput = document.getElementById("end");
const solveButton = document.getElementById("solve");
const resultDiv = document.getElementById("result");

solveButton.addEventListener("click", () => {
    const startNode = startInput.value;
    const endNode = endInput.value;

    fetch('http://127.0.0.1:5000/dijkstra', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ start: startNode, end: endNode })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log(data);  // Logging the received data for debugging
        resultDiv.innerHTML = `
            <p>Jarak terpendek: ${data.distance}</p>
            <p>Rute terpendek: ${data.path.join(' -> ')}</p>
        `;
    })
    .catch(error => {
        console.error('Error:', error);
        resultDiv.innerHTML = "<p>Terjadi kesalahan. Silakan coba lagi.</p>";
    });
});
