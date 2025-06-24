# 🌤️ Sistema de Predicción Climática con LLM

Microservicio basado en FastAPI que proporciona pronósticos meteorológicos interpretados por Inteligencia Artificial usando un LLM (Large Language Model) local.

## 🎯 Características Principales

- **FastAPI backend** para alto rendimiento
- **Integración con OpenWeatherMap API** para datos meteorológicos precisos
- **Análisis con LLM local** para interpretaciones y recomendaciones inteligentes
- **Formato JSON** para fácil integración
- **Configuración flexible** mediante variables de entorno
- **Endpoints simples y documentados**

## 🚀 Endpoints Disponibles

### 1. `/prediction` - Pronóstico Básico

Devuelve datos meteorológicos en formato JSON.

**Método:** GET  
**Parámetros:**
- `lat` (float): Latitud de la ubicación
- `lon` (float): Longitud de la ubicación

**Ejemplo:**
```bash
curl "http://localhost:8000/prediction?lat=4.60971&lon=-74.08175"
```

**Respuesta:**
```json
{
  "pronostico": [
    {
      "fecha": "12/06 22:00",
      "temperatura": "11.36°C",
      "descripcion": "Muy nuboso",
      "prob_precipitacion": "8.0%"
    }
  ]
}
```

### 2. `/prediction-llm` - Pronóstico con Análisis IA

Combina datos meteorológicos con análisis interpretativo de un LLM local.

**Método:** GET  
**Parámetros:**
- `lat` (float): Latitud de la ubicación
- `lon` (float): Longitud de la ubicación
- `llm_hash` (string, opcional): Hash ID del modelo LLM

**Ejemplo:**
```bash
# Con hash específico
curl "http://localhost:8000/prediction-llm?lat=4.60971&lon=-74.08175&llm_hash=tu-hash-aqui"

# Con hash por defecto
curl "http://localhost:8000/prediction-llm?lat=4.60971&lon=-74.08175"
```

**Respuesta:**
```json
{
  "success": true,
  "prediccion_interpretada": {
    "response": "Basándome en los datos meteorológicos...",
    "analysis": "Recomendaciones y análisis del LLM"
  },
  "datos_clima": {
    "pronostico": [...]
  },
  "mensaje": "Predicción generada exitosamente con análisis de LLM"
}
```

## 🛠️ Instalación y Configuración

### Requisitos
- Python 3.8+
- API key de OpenWeatherMap (gratuita)
- LLM local ejecutándose (para funcionalidad IA)

### 1. Clonar el repositorio
```bash
git clone https://github.com/Oriojas/Chainlink_Chromion_Hackatho_Backn.git
cd Chainlink_Chromion_Hackatho_Backn
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
# o usando poetry
poetry install
```

### 3. Configurar variables de entorno
Crea un archivo `.env` basado en `.env.example`:

```bash
# API Key de OpenWeatherMap
OPENWEATHER_APP_KEY=tu_api_key_aqui

# Configuración del servidor
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000

# Configuración del LLM local (opcional)
LLM_BASE_URL=http://localhost:3001
LLM_HASH_ID=tu-hash-del-modelo-aqui
LLM_TIMEOUT=30
```

### 4. Obtener API Key de OpenWeatherMap
1. Visita [OpenWeatherMap](https://openweathermap.org/api)
2. Regístrate gratuitamente
3. Obtén tu API key
4. Agrégala al archivo `.env`

## 🚀 Uso

### Iniciar el servidor
```bash
python main.py
```

El servidor estará disponible en: `http://localhost:8000`

### Documentación interactiva
Visita `http://localhost:8000/docs` para la documentación automática de Swagger.

## 🤖 Configuración del LLM

### Requisitos para funcionalidad IA:
1. **LLM local ejecutándose** en `http://localhost:3001`
2. **Hash del modelo** (específico para cada ejecución)
3. **Endpoint funcional:** `http://localhost:3001/{hash}/message`

### ⚠️ Importante sobre el Hash:
- El hash **cambia en cada ejecución** del modelo LLM
- Debes **obtener el hash actual** desde la interfaz de tu LLM
- Ejemplo: `dd1a3913-6f2b-060b-9d69-7efb4bce9f01`

### Configuración del Hash:

#### Opción 1: Variable de entorno (recomendado)
```bash
LLM_HASH_ID=tu-hash-del-modelo-aqui
```

#### Opción 2: Parámetro en la URL
```bash
curl "http://localhost:8000/prediction-llm?lat=4.60971&lon=-74.08175&llm_hash=tu-hash-aqui"
```

## 🧪 Pruebas

### Suite de pruebas automatizada
```bash
python test/test_weather_prediction.py
```

Esta suite de pruebas incluye:
- ✅ Verificación de conexión con FastAPI
- ✅ Prueba del endpoint básico `/prediction`
- ✅ Prueba del endpoint con IA `/prediction-llm`
- ✅ Verificación de conexión con LLM
- ✅ Pruebas con múltiples ubicaciones

### Pruebas manuales
```bash
# Probar endpoint básico
curl "http://localhost:8000/prediction?lat=4.60971&lon=-74.08175"

# Probar endpoint con LLM
curl "http://localhost:8000/prediction-llm?lat=4.60971&lon=-74.08175&llm_hash=tu-hash"
```

## 📁 Estructura del Proyecto

```
Chainlink_Chromion_Hackatho_Backn/
├── src/
│   ├── queries.py          # Lógica de consultas meteorológicas y LLM
│   ├── pronostico.json     # Ejemplo de salida
│   └── __pycache__/        # Cache de Python
├── test/
│   └── test_weather_prediction.py  # Suite de pruebas unificada
├── main.py                 # Aplicación FastAPI principal
├── .env.example           # Plantilla de configuración
├── .gitignore
├── LICENSE
├── README.md              # Este archivo
├── poetry.lock
└── pyproject.toml         # Configuración de dependencias
```

## 🔧 Funcionalidades Técnicas

### Procesamiento de Datos Climáticos
- Obtiene pronóstico extendido (5 días, intervalos de 3 horas)
- Formatea fechas y datos meteorológicos
- Extrae información relevante (temperatura, descripción, precipitación)

### Integración con LLM
- Crea texto descriptivo optimizado para el LLM
- Envía solicitudes HTTP al LLM local
- Maneja errores de conexión y timeouts
- Devuelve respuestas estructuradas

### Análisis Solicitado al LLM
El sistema solicita al LLM:
- 📊 Análisis del patrón climático general
- 👕 Recomendaciones de vestimenta y actividades
- ⚠️ Alertas o precauciones importantes
- 📈 Predicción de tendencias futuras

## 🌍 Ejemplos de Uso

### Ciudades de Ejemplo

#### Bogotá, Colombia
```bash
curl "http://localhost:8000/prediction-llm?lat=4.60971&lon=-74.08175"
```

#### Madrid, España
```bash
curl "http://localhost:8000/prediction-llm?lat=40.4168&lon=-3.7038"
```

#### Ciudad de México, México
```bash
curl "http://localhost:8000/prediction-llm?lat=19.4326&lon=-99.1332"
```

## ⚠️ Manejo de Errores

### Errores Comunes y Soluciones

#### 1. Error de API del clima
```json
{
  "success": false,
  "error": "No se pudo obtener el pronóstico del clima"
}
```
**Solución:** Verifica tu API key de OpenWeatherMap.

#### 2. Error de conexión con LLM
```json
{
  "success": false,
  "error": "Error al consultar LLM local: [detalle]"
}
```
**Solución:** Verifica que el LLM esté ejecutándose y el hash sea correcto.

#### 3. Timeout del LLM
**Solución:** Aumenta el valor de `LLM_TIMEOUT` en las variables de entorno.

## 🚨 Solución de Problemas

### LLM no responde:
1. ✅ Verifica que el LLM esté en `http://localhost:3001`
2. 🔑 **Confirma que el hash del modelo sea correcto** (error más común)
3. 🔗 Verifica el endpoint: `http://localhost:3001/{hash}/message`
4. 📋 Revisa los logs para errores de conexión
5. 🧪 Prueba el LLM directamente con curl

### API del clima no funciona:
1. 🔑 Verifica tu API key de OpenWeatherMap
2. 📍 Confirma que las coordenadas sean válidas (-90 a 90 lat, -180 a 180 lon)
3. 📊 Revisa tu cuota de API calls

### Servidor no inicia:
1. 🐍 Verifica que Python 3.8+ esté instalado
2. 📦 Instala las dependencias: `pip install -r requirements.txt`
3. 🔧 Verifica el archivo `.env`

## 🔄 Flujo de Trabajo del Sistema

```
Cliente solicita /prediction-llm
        ↓
Obtener datos climáticos (OpenWeatherMap)
        ↓
Procesar datos meteorológicos
        ↓
Crear texto optimizado para LLM
        ↓
Consultar LLM local
        ↓
Combinar respuestas
        ↓
Retornar resultado completo
```

## 🔜 Mejoras Futuras

- 📚 Caché de respuestas del LLM
- 🔄 Múltiples LLMs para comparación
- 😊 Análisis de sentimientos del clima
- 🌐 Integración con más APIs meteorológicas
- 👤 Personalización de prompts por usuario
- 📱 API para aplicaciones móviles

## 🤝 Contribución

Este proyecto forma parte del **Chainlink Chromion Hackathon**.

### Repositorio del Agente IA
https://github.com/Oriojas/eliza-starter-orc.git

### Cómo contribuir:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

MIT License - Ver archivo [LICENSE](LICENSE) para más detalles.

## 📞 Soporte

Si tienes problemas:
1. 📖 Revisa esta documentación
2. 🧪 Ejecuta las pruebas: `python test/test_weather_prediction.py`
3. 📋 Revisa los logs del servidor
4. 🐛 Reporta issues en GitHub

---

**¡Gracias por usar el Sistema de Predicción Climática con LLM!** 🌤️🤖