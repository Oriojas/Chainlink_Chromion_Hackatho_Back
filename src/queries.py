import os
import json
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, Any

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

def consultar_llm_local(datos_clima: Dict[str, Any], llm_hash: str = None) -> Dict[str, Any]:
    """
    Consulta el LLM local para generar una predicción interpretada basada en los datos del clima.

    Args:
        datos_clima (Dict): Datos del pronóstico del clima
        llm_hash (str, optional): Hash ID del modelo LLM. Si no se proporciona, usa la variable de entorno.

    Returns:
        Dict: Respuesta del LLM con la predicción interpretada
    """
    # Configuración del LLM desde variables de entorno
    llm_base_url = os.getenv('LLM_BASE_URL', 'http://localhost:3001')
    llm_hash_id = llm_hash or os.getenv('LLM_HASH_ID', 'dd1a3913-6f2b-060b-9d69-7efb4bce9f01')
    llm_timeout = int(os.getenv('LLM_TIMEOUT', '30'))

    # URL del LLM local con hash configurable
    llm_url = f"{llm_base_url}/{llm_hash_id}/message"

    # Crear un texto descriptivo del clima para enviar al LLM
    texto_clima = crear_texto_clima_para_llm(datos_clima)

    # Payload para el LLM
    payload = {
        "text": texto_clima,
        "userId": "weather_predictor",
        "userName": "Sistema de Predicción Climática"
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(llm_url, json=payload, headers=headers, timeout=llm_timeout)
        response.raise_for_status()

        # Retornar la respuesta del LLM
        return {
            "success": True,
            "prediccion_llm": response.json(),
            "datos_clima_originales": datos_clima
        }

    except requests.exceptions.RequestException as e:
        print(f"Error al consultar LLM local: {e}")
        return {
            "success": False,
            "error": str(e),
            "datos_clima_originales": datos_clima
        }

def crear_texto_clima_para_llm(datos_clima: Dict[str, Any]) -> str:
    """
    Crea un texto descriptivo del clima para enviar al LLM.

    Args:
        datos_clima (Dict): Datos del pronóstico del clima

    Returns:
        str: Texto descriptivo para el LLM
    """
    if "pronostico" not in datos_clima:
        return "No se pudo obtener información del clima para realizar una predicción."

    pronostico = datos_clima["pronostico"]

    # Crear un resumen del pronóstico para las próximas horas/días
    texto = "Basándote en la siguiente información meteorológica, por favor proporciona una predicción detallada y recomendaciones prácticas:\n\n"
    texto += "PRONÓSTICO EXTENDIDO:\n"

    for i, item in enumerate(pronostico[:8]):  # Primeros 8 registros (próximas 24 horas aprox)
        texto += f"- {item['fecha']}: {item['temperatura']}, {item['descripcion']}, "
        texto += f"Probabilidad de precipitación: {item['prob_precipitacion']}\n"

    texto += "\nPor favor, proporciona:\n"
    texto += "1. Un análisis del patrón climático general\n"
    texto += "2. Recomendaciones de vestimenta y actividades\n"
    texto += "3. Alertas o precauciones importantes\n"
    texto += "4. Predicción de tendencias para los próximos días\n"
    texto += "\nResponde de manera clara y útil para el usuario final."

    return texto

def obtener_prediccion_con_llm(lat: float, lon: float, llm_hash: str = None) -> Dict[str, Any]:
    """
    Función principal que obtiene el pronóstico del clima y lo procesa con el LLM.

    Args:
        lat (float): Latitud de la ubicación
        lon (float): Longitud de la ubicación
        llm_hash (str, optional): Hash ID del modelo LLM. Si no se proporciona, usa la variable de entorno.

    Returns:
        Dict: Predicción completa con datos del clima y análisis del LLM
    """
    # Obtener datos del clima
    pronostico = obtener_pronostico_extendido(lat, lon)
    if not pronostico:
        return {
            "success": False,
            "error": "No se pudo obtener el pronóstico del clima"
        }

    # Procesar datos del clima
    datos_pronostico = procesar_pronostico(pronostico)
    datos_clima = {"pronostico": datos_pronostico}

    # Consultar LLM para obtener predicción interpretada
    resultado_llm = consultar_llm_local(datos_clima, llm_hash)

    return resultado_llm

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
