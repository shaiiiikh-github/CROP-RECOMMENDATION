document.getElementById('crop-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Get form data
    const soilType = document.getElementById('soil-type').value;
    const phLevel = document.getElementById('ph-level').value;
    const temperature = document.getElementById('temperature').value;
    const rainfall = document.getElementById('rainfall').value;
    const waterAvailability = document.getElementById('water-availability').value;

    // Send data to the backend
    fetch('/api/recommend-crops', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            soilType: soilType,
            phLevel: phLevel,
            temperature: temperature,
            rainfall: rainfall,
            waterAvailability: waterAvailability
        })
    })
    .then(response => response.json())
    .then(data => {
        // Display the recommendations
        const recommendations = document.getElementById('recommendations');
        recommendations.innerHTML = '<h3>Recommended Crops:</h3>';
        data.forEach(crop => {
            recommendations.innerHTML += `<p>${crop.crop}: ${crop.suitability}</p>`;
        });
    })
    .catch(error => console.error('Error:', error));
});

