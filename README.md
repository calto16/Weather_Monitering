# Real-Time Data Processing System for Weather Monitoring with Rollups and Aggregates

This project implements a real-time weather monitoring system that fetches data from the OpenWeather API, processes it, and provides various insights and alerts based on the collected data.

## Table of Contents

1. [How to Run the Project Locally](#how-to-run-the-project-locally)
2. [High-Level Design](#high-level-design)
3. [Design Choices and Technologies Used](#design-choices-and-technologies-used)
4. [Performance](#performance)
5. [API Design](#api-design)
6. [Security Considerations](#security-considerations)
7. [Scalability](#scalability)
8. [Future Enhancements](#future-enhancements)
9. [Troubleshooting](#troubleshooting)

## How to Run the Project Locally

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/weather-monitoring-system.git
   cd weather-monitoring-system
   ```

2. Set up a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up MongoDB:
   - Install MongoDB if you haven't already
   - Start the MongoDB service

5. Configure the application:
   - Open `app/core/config.py`
   - Update the `API_KEY` with your OpenWeather API key
   - Update the `SENDGRID_API_KEY` with your SendGrid API key
   - Modify other configuration variables as needed

6. Run the application:
   ```
   python -m app.main
   ```

7. Access the application at `http://localhost:8000`

## High-Level Design

The system consists of several components:

1. **Data Fetcher**: Continuously fetches weather data from the OpenWeather API for specified cities.
2. **Data Processor**: Processes the raw data, converts units, and stores it in the database.
3. **Database**: MongoDB stores raw weather data, processed data, and user alert thresholds.
4. **API Layer**: FastAPI-based RESTful API for data retrieval and user interactions.
5. **Aggregation Engine**: Computes rollups and aggregates (e.g., 24-hour summaries).
6. **Alert System**: Monitors data and sends email alerts based on user-defined thresholds.
7. **Web Interface**: Simple HTML/JavaScript frontend for data visualization and user interactions.

## Design Choices and Technologies Used

- **FastAPI**: Chosen for its high performance, easy-to-use async support, and automatic API documentation.
- **MongoDB**: Used for its flexibility with JSON-like documents and good performance for read-heavy workloads.
- **Python**: The primary programming language, known for its simplicity and rich ecosystem of libraries.
- **SendGrid**: Utilized for sending email alerts due to its reliable email delivery service.
- **OpenWeather API**: Selected as the data source for its comprehensive weather data and free tier availability.
- **Asynchronous Processing**: Implemented to handle concurrent API requests and data processing efficiently.

## Performance

- The system fetches weather data every 5 minutes for each city.
- MongoDB indexing is used to optimize query performance.
- Asynchronous operations allow for non-blocking I/O, improving overall system responsiveness.
- Aggregations are pre-computed and stored to reduce on-the-fly calculation time.

## API Design

The API follows RESTful principles and includes the following endpoints:

1. `GET /fetch_weather/{city}`: Retrieve the latest weather data for a specific city.
2. `GET /weather_summary/{city}`: Get a 24-hour summary of weather data for a city.
3. `POST /set_alert/`: Set a temperature alert threshold for a user and city.
4. `GET /remove_threshold/`: Remove an alert threshold for a user and city.
5. `GET /get_alert_thresholds/`: Retrieve all alert thresholds for a user.
6. `POST /send_email/`: Manually trigger an email alert (mainly for testing purposes).

All endpoints return JSON responses and use appropriate HTTP status codes.

## Security Considerations

- API keys are stored in configuration files and should be kept secret.
- Input validation is performed using Pydantic models to prevent injection attacks.
- CORS (Cross-Origin Resource Sharing) should be configured appropriately in a production environment.
- Rate limiting should be implemented to prevent API abuse.

## Scalability

- The modular design allows for easy scaling of individual components.
- MongoDB can be scaled horizontally for increased data volume.
- The asynchronous nature of the application supports handling multiple concurrent requests.
- For higher loads, consider implementing a message queue system for better load distribution.

## Future Enhancements

1. Implement user authentication and authorization.
2. Add support for more weather data sources.
3. Implement more complex aggregations and analytics.
4. Develop a more sophisticated frontend with interactive charts and maps.
5. Integrate with other notification systems (e.g., SMS, push notifications).

## Troubleshooting

- If you encounter database connection issues, ensure MongoDB is running and the connection string is correct.
- For API-related issues, check the OpenWeather API status and your API key validity.
- If email alerts are not working, verify your SendGrid API key and sender email address.
