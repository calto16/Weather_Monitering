let temperatureUnit = 'Celsius';
let cityThresholds = {};
let email = localStorage.getItem("email") || "";

function askForEmail() {
    if (!email || !email.includes("@")) {
        email = prompt("Enter your email id to get alerts");

        if (email && email.includes("@")) {
            localStorage.setItem("email", email);  // Store valid email
        } else {
            alert("Please enter a valid email address.");
            email = ""; // Reset email if invalid
        }
    }
}

askForEmail();

if (email) {
    async function removeCityThreshold(city) {
        const response = await fetch(`/remove_threshold/?email=${email}&city=${city}`, {
            method: 'GET',
        });

        if (response.ok) {
            document.getElementById(`threshold-${city}`).value = ''; 
            document.getElementById(`alert-${city}`).style.display = 'none'; 
            alert(`Alert threshold removed for ${city}`);
        } else {
            const error = await response.json();
            alert(`Error: ${error.detail}`);
        }
    }

} else {
    alert("You need to set a valid email to receive alerts.");
}

function toggleUnit() {
    temperatureUnit = document.getElementById("unit-select").value;
    updateWeatherCards();  
}

async function fetchThresholds() {
    const cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"];
    const response = await fetch(`/get_alert_thresholds/?email=${email}`);
    let thresholds = await response.json();
    thresholds = thresholds.alert_thresholds;

    for (const city of cities) {
        if (thresholds.some(threshold => threshold.city == city)) {
            const threshold = thresholds.find(threshold => threshold.city == city).temperature_threshold;
            document.getElementById(`threshold-${city}`).value = threshold;
        } else {
            thresholds.push({ city: city, temperature_threshold: 1000 }); 
        }
    }
    cityThresholds = thresholds;
}

async function updateWeatherCards() {
    const cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"];
    console.log(email);
    for (const city of cities) {
        const response = await fetch(`/fetch_weather/${city}`);
        if (!response.ok) {
            console.error(`Failed to fetch weather data for ${city}`);
            continue;
        }
        const data = await response.json();

        const tempUnit = temperatureUnit === 'Celsius' ? data.temp : (data.temp + 273.15);
        const feelsLikeUnit = temperatureUnit === 'Celsius' ? data.feels_like : (data.feels_like + 273.15);
        document.getElementById(`weather-main-${city}`).textContent = `Condition: ${data.main}`;
        document.getElementById(`weather-temp-${city}`).textContent = `Temperature: ${tempUnit.toFixed(2)} °${temperatureUnit === 'Celsius' ? 'C' : 'K'}`;
        document.getElementById(`weather-feels-like-${city}`).textContent = `Feels Like: ${feelsLikeUnit.toFixed(2)} °${temperatureUnit === 'Celsius' ? 'C' : 'K'}`;
        document.getElementById(`weather-dt-${city}`).textContent = `Last Update: ${new Date(data.dt * 1000).toLocaleString()}`;

        const threshold = cityThresholds.find(threshold => threshold.city === city).temperature_threshold;
        console.log(threshold,data.temp);
        
        if (data.temp > threshold) {

            document.getElementById(`alert-${city}`).style.display = 'block';
            fetch('/send_email/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    city: city,
                    temperature: data.temp,
                    email: email, 
                }),
            });
        } else {
            document.getElementById(`alert-${city}`).style.display = 'none';
        }
    }
}


async function setCityThreshold(city) {
    const threshold = document.getElementById(`threshold-${city}`).value;
    const response = await fetch(`/fetch_weather/${city}`);
    const data = await response.json();

    await fetch('/set_alert/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email, 
            city: city,
            temperature_threshold: parseFloat(threshold),
        }),
    });
    alert(`Alert threshold set for ${city} `);
    if (data.temp > threshold) {
        document.getElementById(`alert-${city}`).style.display = 'block';
    } else {
        document.getElementById(`alert-${city}`).style.display = 'none';
    }
}


async function removeCityThreshold(city) {
    emailx = localStorage.getItem("email") || "";
    const response = await fetch(`/remove_threshold/?email=${emailx}&city=${city}`, {
        method: 'GET',
    });

    if (response.ok) {
        document.getElementById(`threshold-${city}`).value = ''; 
        document.getElementById(`alert-${city}`).style.display = 'none'; 
        alert(`Alert threshold removed for ${city}`);
    } else {
        const error = await response.json();
        alert(`Error: ${error.detail}`);
    }
}


async function getCitySummary(city) {
    const response = await fetch(`/weather_summary/${city}`);
    const summary = await response.json();

    const summaryElement = document.getElementById("summary-content");
    summaryElement.innerHTML = `
        <p><strong>City:</strong> ${summary.city}</p>
        <p><strong>Average Temperature:</strong> ${summary.average_temperature.toFixed(2)} °C</p>
        <p><strong>Max Temperature:</strong> ${summary.max_temperature.toFixed(2)} °C</p>
        <p><strong>Min Temperature:</strong> ${summary.min_temperature.toFixed(2)} °C</p>
        <p><strong>Dominant Weather Condition:</strong> ${summary.dominant_weather_condition}</p>
    `;
    document.getElementById("daily-summary").style.display = "block"; 
}


function logout() {
    localStorage.clear();
    window.location.reload();
}
reloadPage = () => {
    setTimeout(() => {
        window.location.reload();
    }, 5 * 60 * 1000); // Reload every 5 minutes ( Min * Sec * MilliSec )
};


window.onload = async () => {
    await fetchThresholds();
    updateWeatherCards();
    reloadPage();
};
