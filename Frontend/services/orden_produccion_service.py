"""
Servicio para manejo de órdenes de producción - ACTUALIZADO
"""

import requests
from config.api_config import API_URL

def obtener_ordenes_produccion(filtro_estado=None):
    """Obtener todas las órdenes de producción, opcionalmente filtradas por estado"""
    try:
        params = {"estado": filtro_estado} if filtro_estado else {}
        response = requests.get(f"{API_URL}/obtener_ordenes_produccion", params=params)
        return response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener órdenes de producción: {e}")
        return []

def insertar_orden_produccion(producto_id, cantidad, fecha_inicio, fecha_fin, estado):
    """Insertar una nueva orden de producción"""
    try:
        data = {
            "producto_id": producto_id,
            "cantidad": cantidad,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "estado": estado
        }
        response = requests.post(f"{API_URL}/nueva_orden_produccion", json=data)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al insertar orden de producción: {e}")
        return False

def actualizar_estado_orden_produccion(orden_id, nuevo_estado):
    """Actualizar estado de una orden de producción"""
    try:
        data = {"estado": nuevo_estado}  # Usar 'estado' en lugar de 'nuevo_estado'
        response = requests.patch(f"{API_URL}/actualizar_estado_orden_produccion", params={"orden_id": orden_id}, json=data)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al actualizar estado de orden de producción: {e}")
        return False