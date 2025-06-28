import uvicorn
from fastapi import FastAPI
from typing import Optional
from src.queries import obtener_pronostico_extendido, procesar_pronostico, obtener_prediccion_con_llm

app = FastAPI()

@app.get("/")
def root():
    """
    Endpoint raíz que muestra un mensaje de bienvenida.

    Returns:
        dict: Mensaje de bienvenida y descripción de la API.
    """
    return {
        "mensaje": "Bienvenido a la API de pronóstico del clima",
        "descripcion": "Esta API proporciona pronósticos del clima y análisis utilizando modelos LLM.",
        "endpoints": {
            "/prediction": "Obtiene el pronóstico del clima en formato JSON.",
            "/prediction-llm": "Obtiene el pronóstico del clima analizado por un LLM."
        }
    }


@app.get("/prediction")
def get_prediction(lat: float, lon: float):
    """
    Endpoint que devuelve el pronóstico del clima en formato JSON.

    Args:
        lat (float): Latitud de la ubicación.
        lon (float): Longitud de la ubicación.

    Returns:
        dict: Pronóstico extendido en formato JSON.
    """
    pronostico = obtener_pronostico_extendido(lat, lon)
    if pronostico:
        datos_pronostico = procesar_pronostico(pronostico)
        return {"pronostico": datos_pronostico}
    return {"error": "No se pudo obtener el pronóstico"}

@app.get("/prediction-llm")
def get_prediction_with_llm(lat: float, lon: float, llm_hash: Optional[str] = None):
    """
    Endpoint que obtiene el pronóstico del clima y lo analiza con un LLM local.

    Args:
        lat (float): Latitud de la ubicación.
        lon (float): Longitud de la ubicación.
        llm_hash (Optional[str]): Hash ID del modelo LLM. Si no se proporciona, usa la variable de entorno.

    Returns:
        dict: Predicción del clima interpretada por el LLM junto con los datos originales.
    """
    resultado = obtener_prediccion_con_llm(lat, lon, llm_hash)

    if resultado.get("success"):
        return {
            "success": True,
            "prediccion_interpretada": resultado.get("prediccion_llm"),
            # "datos_clima": resultado.get("datos_clima_originales"),
            "mensaje": "Predicción generada exitosamente con análisis de LLM"
        }
    else:
        return {
            "success": False,
            "error": resultado.get("error", "Error desconocido"),
            "datos_clima": resultado.get("datos_clima_originales")
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
