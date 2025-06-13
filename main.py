import uvicorn
from fastapi import FastAPI
from typing import Optional
from src.queries import obtener_pronostico_extendido, procesar_pronostico

app = FastAPI()

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
