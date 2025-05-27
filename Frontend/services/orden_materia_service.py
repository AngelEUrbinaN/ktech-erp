"""
Servicio para manejo de órdenes de materiales
"""

import requests
from config.api_config import API_URL

def obtener_ordenes_materia():
    """Obtener todas las órdenes de materiales"""
    try:
        response = requests.get(f"{API_URL}/obtener_ordenes_materia")
        return response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener órdenes de materiales: {e}")
        return []

def insertar_orden_materia(materia_id, cantidad, fecha, estado):
    """Insertar una nueva orden de materiales"""
    try:
        data = {
            "materia_id": materia_id,
            "cantidad": cantidad,
            "fecha": fecha,
            "estado": estado
        }
        response = requests.post(f"{API_URL}/nueva_orden_materia", json=data)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al insertar orden de materiales: {e}")
        return False
    
def actualizar_estado_orden_materia(orden_id, nuevo_estado, cantidad_descontar=None):
    """Actualizar estado de una orden de materiales"""
    try:
        data = {"estado": nuevo_estado}  # Usar 'estado' en lugar de 'nuevo_estado'
        if cantidad_descontar and nuevo_estado == "Finalizado":
            data["cantidad_descontar"] = cantidad_descontar
        
        response = requests.patch(f"{API_URL}/actualizar_estado_orden_materia", params={"orden_id": orden_id}, json=data)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al actualizar estado de orden de materiales: {e}")
        return False