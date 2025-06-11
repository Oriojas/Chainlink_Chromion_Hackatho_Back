import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

# Configuración inicial
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

BASE_URL = "https://api.openweathermap.org/data/2.5"

def obtener_clima_actual(lat: float, lon: float) -> dict:
    """Obtiene el clima actual"""
    api_key = os.getenv('OPENWEATHER_APP_KEY')
    url = f"{BASE_URL}/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=es"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error clima actual: {e}")
        return None

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

def mostrar_resultados(clima_actual: dict, pronostico: list):
    """Muestra los resultados formateados"""
    print("\n--- CLIMA ACTUAL ---")
    for key, value in clima_actual.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

    print("\n--- PRONÓSTICO EXTENDIDO (5 días) ---")
    for item in pronostico[:8]:  # Mostramos las próximas 8 mediciones (24 horas aprox)
        print(f"\n{item['fecha']}:")
        print(f"  Temp: {item['temperatura']}")
        print(f"  Desc: {item['descripcion']}")
        print(f"  Lluvia: {item['prob_precipitacion']}")

def main():
    # Coordenadas de Bogotá
    lat, lon = 4.60971, -74.08175

    # Obtener datos
    clima_actual = obtener_clima_actual(lat, lon)
    pronostico = obtener_pronostico_extendido(lat, lon)

    if clima_actual and pronostico:
        datos_actual = procesar_clima_actual(clima_actual)
        datos_pronostico = procesar_pronostico(pronostico)
        mostrar_resultados(datos_actual, datos_pronostico)

if __name__ == "__main__":
    main()
