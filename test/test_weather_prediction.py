#!/usr/bin/env python3
"""
Test Suite para el Sistema de Predicción Climática con LLM
Este archivo unifica todas las pruebas del sistema.
"""

import requests
import json
import sys
from typing import Dict, Any

class WeatherPredictionTester:
    """Clase principal para ejecutar todas las pruebas del sistema."""

    def __init__(self, base_url: str = "http://localhost:8000", llm_base_url: str = "http://localhost:3001"):
        self.base_url = base_url
        self.llm_base_url = llm_base_url
        self.llm_hash = None

    def configurar_llm(self):
        """Configura el hash del LLM para las pruebas."""
        print("🔧 CONFIGURACIÓN DEL LLM:")
        print("El hash del LLM es específico de cada ejecución del modelo.")
        print("Ejemplo: dd1a3913-6f2b-060b-9d69-7efb4bce9f01")

        llm_hash = input("Ingresa el hash de tu LLM (o presiona Enter para usar el valor por defecto): ").strip()
        if not llm_hash:
            self.llm_hash = None
            print("📝 Usando hash por defecto desde variables de entorno")
        else:
            self.llm_hash = llm_hash
            print(f"📝 Usando hash proporcionado: {llm_hash}")

    def probar_conexion_llm(self, hash_id: str = None, timeout: int = 30) -> Dict[str, Any]:
        """
        Prueba la conexión con el LLM local.

        Args:
            hash_id (str): Hash ID del modelo
            timeout (int): Timeout en segundos

        Returns:
            Dict: Resultado de la prueba
        """
        if not hash_id:
            return {
                "success": False,
                "error": "Se requiere el hash ID del modelo"
            }

        llm_url = f"{self.llm_base_url}/{hash_id}/message"

        payload = {
            "text": "Hola, ¿puedes responder a este mensaje de prueba?",
            "userId": "test_user",
            "userName": "Test Connection"
        }

        headers = {"Content-Type": "application/json"}

        try:
            print(f"🔗 Probando conexión con: {llm_url}")
            print(f"⏱️ Timeout configurado: {timeout} segundos")
            print("📤 Enviando mensaje de prueba...")

            response = requests.post(llm_url, json=payload, headers=headers, timeout=timeout)
            print(f"📊 Código de respuesta: {response.status_code}")

            if response.status_code == 200:
                try:
                    resultado = response.json()
                    return {
                        "success": True,
                        "url": llm_url,
                        "response_data": resultado,
                        "status_code": response.status_code
                    }
                except json.JSONDecodeError:
                    return {
                        "success": False,
                        "error": "La respuesta no es JSON válido",
                        "url": llm_url,
                        "response_text": response.text[:500],
                        "status_code": response.status_code
                    }
            else:
                return {
                    "success": False,
                    "error": f"Error HTTP {response.status_code}",
                    "url": llm_url,
                    "response_text": response.text[:500],
                    "status_code": response.status_code
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": f"Timeout después de {timeout} segundos",
                "url": llm_url
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Error de conexión - Verifica que el LLM esté ejecutándose",
                "url": llm_url
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Error de solicitud: {str(e)}",
                "url": llm_url
            }

    def probar_endpoint_original(self, lat: float, lon: float) -> Dict[str, Any]:
        """Prueba el endpoint original /prediction."""
        print("\n1️⃣ PROBANDO ENDPOINT ORIGINAL (/prediction):")

        try:
            response = requests.get(f"{self.base_url}/prediction",
                                  params={"lat": lat, "lon": lon},
                                  timeout=30)
            response.raise_for_status()
            resultado = response.json()

            pronostico = resultado.get("pronostico", [])
            print(f"   ✅ Datos obtenidos: {len(pronostico)} registros")
            if pronostico:
                print(f"   🌡️ Primer registro: {pronostico[0]['fecha']} - {pronostico[0]['temperatura']}")

            return {"success": True, "data": resultado}

        except Exception as e:
            print(f"   ❌ Error: {e}")
            return {"success": False, "error": str(e)}

    def probar_endpoint_llm(self, lat: float, lon: float) -> Dict[str, Any]:
        """Prueba el endpoint con LLM /prediction-llm."""
        print("\n2️⃣ PROBANDO ENDPOINT CON LLM (/prediction-llm):")

        url = f"{self.base_url}/prediction-llm"
        params = {"lat": lat, "lon": lon}

        if self.llm_hash:
            params["llm_hash"] = self.llm_hash
            print(f"   🔑 Usando hash del LLM: {self.llm_hash}")

        try:
            print(f"   🌐 URL: {url}")
            print("   📤 Enviando solicitud...")

            response = requests.get(url, params=params, timeout=60)
            response.raise_for_status()
            resultado = response.json()

            if resultado.get("success"):
                print("   ✅ Predicción generada exitosamente")

                # Mostrar datos del clima
                datos_clima = resultado.get("datos_clima", {})
                pronostico = datos_clima.get("pronostico", [])

                print(f"   📊 Datos del clima: {len(pronostico)} registros")
                if pronostico:
                    print(f"   🌡️ Primer registro: {pronostico[0]['fecha']} - {pronostico[0]['temperatura']}")

                # Mostrar info del LLM
                prediccion_llm = resultado.get("prediccion_interpretada", {})
                if isinstance(prediccion_llm, dict):
                    print("   🤖 Análisis del LLM generado correctamente")
                else:
                    print(f"   🤖 Respuesta del LLM: {str(prediccion_llm)[:100]}...")

            else:
                print(f"   ❌ Error en la predicción: {resultado.get('error', 'Error desconocido')}")

            return resultado

        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error de conexión: {e}")
            return {"success": False, "error": str(e)}
        except json.JSONDecodeError as e:
            print(f"   ❌ Error al decodificar JSON: {e}")
            return {"success": False, "error": "Respuesta inválida del servidor"}

    def mostrar_resultado_detallado(self, resultado: Dict[str, Any]):
        """Muestra un resultado detallado de las pruebas."""
        print("\n" + "="*60)
        print("RESULTADO DETALLADO")
        print("="*60)

        if resultado.get("success"):
            print("✅ ÉXITO")

            # Mostrar datos del clima si existen
            datos_clima = resultado.get("datos_clima", {})
            pronostico = datos_clima.get("pronostico", [])

            if pronostico:
                print(f"\n📊 PRONÓSTICO DEL CLIMA ({len(pronostico)} registros):")
                for i, item in enumerate(pronostico[:5]):  # Mostrar primeros 5
                    print(f"  {i+1}. {item['fecha']}: {item['temperatura']} - {item['descripcion']} (Lluvia: {item['prob_precipitacion']})")

            # Mostrar análisis del LLM si existe
            prediccion_llm = resultado.get("prediccion_interpretada", {})
            if prediccion_llm:
                print("\n🤖 ANÁLISIS DEL LLM:")
                if isinstance(prediccion_llm, dict):
                    for key, value in prediccion_llm.items():
                        if isinstance(value, str) and len(value) > 200:
                            print(f"  {key}: {value[:200]}...")
                        else:
                            print(f"  {key}: {value}")
                else:
                    print(f"  {prediccion_llm}")
        else:
            print("❌ ERROR")
            print(f"🚨 Error: {resultado.get('error', 'Error desconocido')}")

    def ejecutar_suite_completa(self):
        """Ejecuta todas las pruebas del sistema."""
        print("🌤️ SUITE DE PRUEBAS - SISTEMA DE PREDICCIÓN CLIMÁTICA CON LLM")
        print("="*70)

        # Configurar LLM
        self.configurar_llm()

        # Coordenadas de prueba
        coordenadas_prueba = [
            {"nombre": "Bogotá, Colombia", "lat": 4.60971, "lon": -74.08175},
            {"nombre": "Madrid, España", "lat": 40.4168, "lon": -3.7038},
        ]

        # Verificar servidor FastAPI
        print(f"\n🚀 VERIFICANDO SERVIDOR FASTAPI ({self.base_url})...")
        try:
            response = requests.get(f"{self.base_url}/docs", timeout=5)
            if response.status_code == 200:
                print("   ✅ Servidor FastAPI está ejecutándose")
            else:
                print("   ⚠️ Servidor responde pero puede tener problemas")
        except:
            print("   ❌ No se puede conectar al servidor FastAPI")
            print("   💡 Asegúrate de ejecutar: python main.py")
            return

        # Verificar LLM si se proporcionó hash
        if self.llm_hash:
            print(f"\n🤖 VERIFICANDO LLM ({self.llm_base_url})...")
            resultado_llm = self.probar_conexion_llm(self.llm_hash, timeout=10)
            if resultado_llm.get("success"):
                print("   ✅ LLM está funcionando correctamente")
            else:
                print(f"   ❌ Error en LLM: {resultado_llm.get('error')}")
                print("   ⚠️ Las pruebas de LLM pueden fallar")

        # Ejecutar pruebas para cada ubicación
        for i, coord in enumerate(coordenadas_prueba, 1):
            print(f"\n{'='*70}")
            print(f"PRUEBA {i}: {coord['nombre']} (lat: {coord['lat']}, lon: {coord['lon']})")
            print(f"{'='*70}")

            # Probar endpoint original
            resultado_original = self.probar_endpoint_original(coord['lat'], coord['lon'])

            # Probar endpoint con LLM
            resultado_llm = self.probar_endpoint_llm(coord['lat'], coord['lon'])

            # Mostrar resultado detallado si es exitoso
            if resultado_llm.get("success"):
                self.mostrar_resultado_detallado(resultado_llm)

            # Preguntar si continuar
            if i < len(coordenadas_prueba):
                continuar = input(f"\n¿Continuar con la siguiente ubicación? (s/n): ").lower().strip()
                if continuar != 's':
                    break

        # Resumen final
        print(f"\n{'='*70}")
        print("RESUMEN Y RECOMENDACIONES")
        print(f"{'='*70}")
        print("✅ Pruebas completadas")
        print("\n💡 COMANDOS ÚTILES:")
        print("• Endpoint original:")
        print("  curl 'http://localhost:8000/prediction?lat=4.60971&lon=-74.08175'")
        print("• Endpoint con LLM:")
        if self.llm_hash:
            print(f"  curl 'http://localhost:8000/prediction-llm?lat=4.60971&lon=-74.08175&llm_hash={self.llm_hash}'")
        else:
            print("  curl 'http://localhost:8000/prediction-llm?lat=4.60971&lon=-74.08175'")

        print("\n📋 VERIFICACIONES:")
        print("1. ✅ Servidor FastAPI ejecutándose en http://localhost:8000")
        if self.llm_hash:
            print(f"2. ✅ LLM ejecutándose en {self.llm_base_url}")
            print(f"3. ✅ Hash del LLM configurado: {self.llm_hash}")
        else:
            print("2. ⚠️ Hash del LLM no configurado (usando valor por defecto)")
        print("4. ✅ API key de OpenWeatherMap configurada")

def main():
    """Función principal."""
    print("🧪 INICIANDO SUITE DE PRUEBAS")

    # Configuración personalizada
    base_url = input("URL del servidor FastAPI (Enter para http://localhost:8000): ").strip()
    if not base_url:
        base_url = "http://localhost:8000"

    llm_base_url = input("URL del LLM (Enter para http://localhost:3001): ").strip()
    if not llm_base_url:
        llm_base_url = "http://localhost:3001"

    # Crear y ejecutar tester
    tester = WeatherPredictionTester(base_url, llm_base_url)
    tester.ejecutar_suite_completa()

if __name__ == "__main__":
    main()
