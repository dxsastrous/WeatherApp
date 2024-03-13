document.addEventListener('DOMContentLoaded', () => {
    const cityInfo = document.getElementById('cityinfo');
    const apikey = 'N8LQGH9JV8CL48S9KN54QASFD';
    const myCity = 'Guildford';
    const webapi = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast?aggregateHours=24&contentType=json&unitGroup=metric&locationMode=single&key=N8LQGH9JV8CL48S9KN54QASFD&locations=Guildford';

    // Function to fetch weather data and update the cityInfo element
    const fetchWeatherData = () => {
        fetch(webapi)
            .then(response => response.json())
            .then(data => {
                if (data.location && data.location.currentConditions) {
                    let todayCondition = `Now: ${data.location.currentConditions.temp}&#8451; ${data.location.values[0].conditions}`;
                    let tmrCondition = `Tomorrow: ${data.location.values[1].temp}&#8451; ${data.location.values[1].conditions}`;
                    cityInfo.innerHTML = `${myCity} ${todayCondition}; ${tmrCondition}`;
                } else {
                    cityInfo.innerHTML = `Failed to fetch weather data: Invalid response format`;
                }
            })
            .catch(error => {
                cityInfo.innerHTML = `Failed to fetch weather data: ${error}`;
            });
    };

    // Call fetchWeatherData function initially
    fetchWeatherData();

    // Set interval to update weather data every 10 minutes (600000 milliseconds)
    setInterval(fetchWeatherData, 600000);

    // Notification delete functionality
    const deleteNotification = () => {
        const deleteButtons = document.querySelectorAll('.notification .delete');
        deleteButtons.forEach(deleteButton => {
            deleteButton.addEventListener('click', () => {
                const notification = deleteButton.parentNode;
                notification.parentNode.removeChild(notification);
            });
        });
    };

    // Call deleteNotification function to enable delete functionality
    deleteNotification();
});
