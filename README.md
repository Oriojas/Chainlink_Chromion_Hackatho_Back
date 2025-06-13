# Chainlink_Chromion_Hackatho_Backn
Chainlink Chromion Hackathon

## IA agent to
https://github.com/Oriojas/eliza-starter-orc.git

## Weather Prediction Microservice

A FastAPI-based service that provides weather forecasts in JSON format using OpenWeatherMap API.

### Features
- FastAPI backend for high performance
- OpenWeatherMap API integration
- JSON-formatted weather forecasts
- Environment variable configuration
- Simple endpoint structure

### Requirements
- Python 3.8+
- pip package manager
- OpenWeatherMap API key (free tier available)

### Installation
1. Clone the repository:
   git clone https://github.com/yourusername/Chainlink_Chromion_Hackatho_Back.git
   cd Chainlink_Chromion_Hackatho_Back

2. Install dependencies:
   pip install -r requirements.txt

3. Configure environment:
   Create .env file in src/ directory with:
   OPENWEATHER_APP_KEY=your_api_key_here

### Usage
To start the service:
python src/main.py

The API will be available at:
http://127.0.0.1:8000

### API Endpoints
#### GET /prediction
Parameters:
- lat (float): Latitude coordinate
- lon (float): Longitude coordinate

Example request:
curl "http://127.0.0.1:8000/prediction?lat=4.60971&lon=-74.08175"

Example response:
```json
{
  "pronostico": [
    {
      "fecha": "12/06 22:00",
      "temperatura": "11.36°C",
      "descripcion": "Muy nuboso",
      "prob_precipitacion": "8.0%"
    },
    ...
  ]
}
```

### Project Structure
```bash
Chainlink_Chromion_Hackatho_Back/
├── src/
│   ├── main.py            # FastAPI application
│   ├── queries.py         # Weather data handling
│   ├── pronostico.json    # Sample output
│   └── .env               # Configuration
├── README.md
└── pyproject.toml
```

### Code Overview
#### src/queries.py
- obtener_pronostico_extendido(lat, lon): Fetches 5-day forecast
- procesar_pronostico(data): Formats API response

#### src/main.py
- FastAPI app with /prediction endpoint
- Calls queries.py functions
- Returns JSON response

### Testing
Test the endpoint with:
curl "http://localhost:8000/prediction?lat=4.60971&lon=-74.08175"

Sample output available in:
src/pronostico.json

### License
MIT License
