import os
import json
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Configuración inicial
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

BASE_URL = "https://api.openweathermap.org/data/2.5"

def obtener_pronostico_extendido(lat: float, lon: float) -> list:
    """Obtiene pronóstico para 5 días (3 horas intervalo)"""
    api_key = os.getenv('OPENWEATHER_APP_KEY')
    url = f"{BASE_URL}/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=es"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('list', [])
    except requests.exceptions.RequestException as e:
        print(f"Error pronóstico extendido: {e}")
        return []

def formatear_fecha(timestamp: int) -> str:
    """Formatea timestamp a fecha legible"""
    return datetime.fromtimestamp(timestamp).strftime('%d/%m %H:%M')

def procesar_clima_actual(datos: dict) -> dict:
    """Procesa datos del clima actual"""
    return {
        'ciudad': datos['name'],
        'temperatura': f"{datos['main']['temp']}°C",
        'sensacion_termica': f"{datos['main']['feels_like']}°C",
        'descripcion': datos['weather'][0]['description'].capitalize(),
        'humedad': f"{datos['main']['humidity']}%",
        'viento': f"{datos['wind']['speed']} m/s",
        'presion': f"{datos['main']['pressure']} hPa"
    }

def procesar_pronostico(pronostico: list) -> list:
    """Procesa datos del pronóstico extendido"""
    return [{
        'fecha': formatear_fecha(item['dt']),
        'temperatura': f"{item['main']['temp']}°C",
        'descripcion': item['weather'][0]['description'].capitalize(),
        'prob_precipitacion': f"{item.get('pop', 0)*100}%"
    } for item in pronostico]

def mostrar_resultados(pronostico: list) -> dict:
    """Devuelve los resultados del pronóstico extendido como un diccionario (JSON)."""
    return {
        'pronostico': [
            {
                'fecha': item['fecha'],
                'temperatura': item['temperatura'],
                'descripcion': item['descripcion'],
                'prob_precipitacion': item['prob_precipitacion']
            }
            for item in pronostico[:8]
        ]
    }

if __name__ == "__main__":
    # Coordenadas de Bogotá
    lat, lon = 4.60971, -74.08175

    # Obtener y procesar el pronóstico extendido
    pronostico = obtener_pronostico_extendido(lat, lon)
    if pronostico:
        datos_pronostico = procesar_pronostico(pronostico)
        resultados = mostrar_resultados(datos_pronostico)
        print(json.dumps(resultados, indent=2))

    with open('src/pronostico.json', 'w') as archivo:
        json.dump(resultados, archivo, indent=2)
