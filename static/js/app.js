document.addEventListener('DOMContentLoaded', () => {
    const fetchButton = document.getElementById('fetchButton');
    const dataContainer = document.getElementById('dataContainer');

    fetchButton.addEventListener('click', () => {
        const source = document.querySelector('input[name="source"]:checked').value;
        
        // Log for debugging purposes
        console.log(`Fetching data from source: ${source}`);

        fetch('/fetch-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ source: source })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Log the received data for debugging purposes
            console.log('Received data:', data);
            
            // Handle case when there is an error in the data
            if (data.error) {
                dataContainer.textContent = `Error: ${data.error}`;
            } else {
                // Display data in the container
                dataContainer.textContent = JSON.stringify(data, null, 2);
            }
        })
        .catch(error => {
            // Log any error that occurs
            console.error('Error fetching data:', error);
            dataContainer.textContent = 'An error occurred while fetching data.';
        });
    });
});
