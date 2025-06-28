# 🌤️ Weather Prediction System with LLM

Microservice built with FastAPI that provides weather forecasts interpreted by Artificial Intelligence using a local LLM (Large Language Model).

## 🎯 Key Features

- **FastAPI backend** for high performance
- **Integration with OpenWeatherMap API** for accurate weather data
- **Analysis with local LLM** for intelligent interpretations and recommendations
- **JSON format** for easy integration
- **Flexible configuration** via environment variables
- **Simple and documented endpoints**

## 🚀 Available Endpoints

### 1. `/prediction` - Basic Forecast

Returns weather data in JSON format.

**Method:** GET  
**Parameters:**
- `lat` (float): Location latitude
- `lon` (float): Location longitude

**Example:**
```bash
curl "http://localhost:8000/prediction?lat=4.60971&lon=-74.08175"
```

**Response:**
```json
{
  "forecast": [
    {
      "date": "12/06 22:00",
      "temperature": "11.36°C",
      "description": "Mostly cloudy",
      "precipitation_probability": "8.0%"
    }
  ]
}
```

### 2. `/prediction-llm` - Forecast with AI Analysis

Combines weather data with interpretative analysis from a local LLM.

**Method:** GET  
**Parameters:**
- `lat` (float): Location latitude
- `lon` (float): Location longitude
- `llm_hash` (string, optional): LLM model hash ID

**Example:**
```bash
# With specific hash
curl "http://localhost:8000/prediction-llm?lat=4.60971&lon=-74.08175&llm_hash=your-hash-here"

# With default hash
curl "http://localhost:8000/prediction-llm?lat=4.60971&lon=-74.08175"
```

**Response:**
```json
{
  "success": true,
  "interpreted_prediction": {
    "response": "Based on the weather data...",
    "analysis": "LLM recommendations and analysis"
  },
  "weather_data": {
    "forecast": [...]
  },
  "message": "Prediction successfully generated with LLM analysis"
}
```

## 🛠️ Installation and Configuration

### Requirements
- Python 3.8+
- OpenWeatherMap API key (free)
- Local LLM running (for AI functionality)

### 1. Clone the repository
```bash
git clone https://github.com/Oriojas/Chainlink_Chromion_Hackatho_Backn.git
cd Chainlink_Chromion_Hackatho_Backn
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
# or using poetry
poetry install
```

### 3. Configure environment variables
Create a `.env` file based on `.env.example`:

```bash
# OpenWeatherMap API Key
OPENWEATHER_APP_KEY=your_api_key_here

# Server configuration
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000

# Local LLM configuration (optional)
LLM_BASE_URL=http://localhost:3001
LLM_HASH_ID=your-model-hash-here
LLM_TIMEOUT=30
```

### 4. Get OpenWeatherMap API Key
1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Register for free
3. Get your API key
4. Add it to the `.env` file

## 🚀 Usage

### Start the server
```bash
python main.py
```

The server will be available at: `http://localhost:8000`

### Interactive documentation
Visit `http://localhost:8000/docs` for automatic Swagger documentation.

## 🤖 LLM Configuration

### Requirements for AI functionality:
1. **Local LLM running** at `http://localhost:3001`
2. **Model hash** (specific to each execution)
3. **Functional endpoint:** `http://localhost:3001/{hash}/message`

### ⚠️ Important about the Hash:
- The hash **changes with each execution** of the LLM model
- You must **get the current hash** from your LLM interface
- Example: `dd1a3913-6f2b-060b-9d69-7efb4bce9f01`

### Hash Configuration:

#### Option 1: Environment variable (recommended)
```bash
LLM_HASH_ID=your-model-hash-here
```

#### Option 2: URL parameter
```bash
curl "http://localhost:8000/prediction-llm?lat=4.60971&lon=-74.08175&llm_hash=your-hash-here"
```

## 🧪 Testing

### Automated test suite
```bash
python test/test_weather_prediction.py
```

This test suite includes:
- ✅ FastAPI connection verification
- ✅ Basic endpoint `/prediction` test
- ✅ AI endpoint `/prediction-llm` test
- ✅ LLM connection verification
- ✅ Tests with multiple locations

### Manual testing
```bash
# Test basic endpoint
curl "http://localhost:8000/prediction?lat=4.60971&lon=-74.08175"

# Test LLM endpoint
curl "http://localhost:8000/prediction-llm?lat=4.60971&lon=-74.08175&llm_hash=your-hash"
```

## 📁 Project Structure

```
Chainlink_Chromion_Hackatho_Backn/
├── src/
│   ├── queries.py          # Weather and LLM query logic
│   ├── forecast.json       # Example output
│   └── __pycache__/        # Python cache
├── test/
│   └── test_weather_prediction.py  # Unified test suite
├── main.py                 # Main FastAPI application
├── .env.example           # Configuration template
├── .gitignore
├── LICENSE
├── README.md              # This file
├── poetry.lock
└── pyproject.toml         # Dependency configuration
```

## 🔧 Technical Features

### Weather Data Processing
- Gets extended forecast (5 days, 3-hour intervals)
- Formats dates and weather data
- Extracts relevant information (temperature, description, precipitation)

### LLM Integration
- Creates optimized descriptive text for the LLM
- Sends HTTP requests to the local LLM
- Handles connection errors and timeouts
- Returns structured responses

### LLM Analysis Requests
The system requests the LLM to provide:
- 📊 General weather pattern analysis
- 👕 Clothing and activity recommendations
- ⚠️ Important alerts or precautions
- 📈 Future trend predictions

## 🌍 Usage Examples

### Example Cities

#### Bogotá, Colombia
```bash
curl "http://localhost:8000/prediction-llm?lat=4.60971&lon=-74.08175"
```

#### Madrid, Spain
```bash
curl "http://localhost:8000/prediction-llm?lat=40.4168&lon=-3.7038"
```

#### Mexico City, Mexico
```bash
curl "http://localhost:8000/prediction-llm?lat=19.4326&lon=-99.1332"
```

## ⚠️ Error Handling

### Common Errors and Solutions

#### 1. Weather API error
```json
{
  "success": false,
  "error": "Could not retrieve weather forecast"
}
```
**Solution:** Verify your OpenWeatherMap API key.

#### 2. LLM connection error
```json
{
  "success": false,
  "error": "Error querying local LLM: [detail]"
}
```
**Solution:** Ensure the LLM is running and the hash is correct.

#### 3. LLM timeout
**Solution:** Increase the `LLM_TIMEOUT` value in environment variables.

## 🚨 Troubleshooting

### LLM not responding:
1. ✅ Verify the LLM is at `http://localhost:3001`
2. 🔑 **Confirm the model hash is correct** (most common error)
3. 🔗 Check the endpoint: `http://localhost:3001/{hash}/message`
4. 📋 Review logs for connection errors
5. 🧪 Test the LLM directly with curl

### Weather API not working:
1. 🔑 Verify your OpenWeatherMap API key
2. 📍 Confirm coordinates are valid (-90 to 90 lat, -180 to 180 lon)
3. 📊 Check your API call quota

### Server not starting:
1. 🐍 Verify Python 3.8+ is installed
2. 📦 Install dependencies: `pip install -r requirements.txt`
3. 🔧 Check the `.env` file

## 🔄 System Workflow

```
Client requests /prediction-llm
        ↓
Get weather data (OpenWeatherMap)
        ↓
Process weather data
        ↓
Create optimized text for LLM
        ↓
Query local LLM
        ↓
Combine responses
        ↓
Return complete result
```

## 🔜 Future Improvements

- 📚 LLM response caching
- 🔄 Multiple LLMs for comparison
- 😊 Weather sentiment analysis
- 🌐 Integration with more weather APIs
- 👤 User-specific prompt customization
- 📱 Mobile app API

## 🤝 Contribution

This project is part of the **Chainlink Chromion Hackathon**.

### AI Agent Repository
https://github.com/Oriojas/eliza-starter-orc.git

### How to contribute:
1. Fork the repository
2. Create a branch for your feature
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 📞 Support

If you encounter issues:
1. 📖 Review this documentation
2. 🧪 Run tests: `python test/test_weather_prediction.py`
3. 📋 Check server logs
4. 🐛 Report issues on GitHub

---

**Thank you for using the Weather Prediction System with LLM!** 🌤️🤖