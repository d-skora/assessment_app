// Call the API to fetch weather data on the location
function getWeatherForLocation(location_id) {
    if (!location_id) {
        return;
    }

    const options = {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json'
    },
    credentials: "same-origin",
    };

    // Make the fetch request with the provided options
    fetch(window.location.origin + '/' + location_id + '/get_weather', options)
        .then(response => {
            // Check if the request was successful
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            // Parse the response as JSON
            return response.json();
        })
        .then(data => {
            // Handle the JSON data
            console.log(data);
            updateWeather(data);
        })
        .catch(error => {
        // Handle any errors that occurred during the fetch
            console.error('Fetch error:', error);
        });
}

// Update colors to match weather
function updateWeather(data)
{
    const temp = document.querySelector(".temp_read");
    const background = document.querySelector(".background");

    temp.textContent = `${data.temp}`;
    background.classList.remove(...background.classList);
    background.classList.add('background');
    background.classList.add(data.weather);
}
