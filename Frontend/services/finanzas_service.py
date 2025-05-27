"""
Servicio para finanzas
"""

import requests
from config.api_config import API_URL

def obtener_ingresos_finalizados():
    """Obtener ingresos (ventas finalizadas)"""
    try:
        response = requests.get(f"{API_URL}/obtener_ingresos_finalizados")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error al obtener ingresos: {e}")
        return []

def obtener_egresos_finalizados():
    """Obtener egresos (compras finalizadas)"""
    try:
        response = requests.get(f"{API_URL}/obtener_egresos_finalizados")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error al obtener egresos: {e}")
        return []

def calcular_resumen_ingresos():
    """Calcular resumen de ingresos"""
    try:
        response = requests.get(f"{API_URL}/resumen_ingresos")
        if response.status_code == 200:
            data = response.json()
            return data.get('total_ventas', 0), data.get('monto_total', 0.0)
        return 0, 0.0
    except Exception as e:
        print(f"Error al calcular resumen de ingresos: {e}")
        return 0, 0.0

def calcular_resumen_egresos():
    """Calcular resumen de egresos"""
    try:
        response = requests.get(f"{API_URL}/resumen_egresos")
        if response.status_code == 200:
            data = response.json()
            return data.get('total_compras', 0), data.get('monto_total', 0.0)
        return 0, 0.0
    except Exception as e:
        print(f"Error al calcular resumen de egresos: {e}")
        return 0, 0.0