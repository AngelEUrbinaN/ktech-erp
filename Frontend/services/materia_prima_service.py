"""
Servicio para manejo de materias primas
"""

import requests
from config.api_config import API_URL

def obtener_materias():
    """Obtener todas las materias primas"""
    try:
        response = requests.get(f"{API_URL}/obtener_materias")
        return response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener materias primas: {e}")
        return []

def obtener_materias_para_combobox():
    """Obtener materias formateadas para combobox (ID - Nombre)"""
    try:
        materias = obtener_materias()
        return [f"{materia[0]} - {materia[1]}" for materia in materias]
    except Exception as e:
        print(f"Error al obtener materias para combobox: {e}")
        return []
def insertar_materia(nombre, descripcion, proveedor_id, stock):
    """Insertar una nueva materia prima"""
    try:
        data = {
            "nombre": nombre,
            "descripcion": descripcion,
            "proveedor_id": proveedor_id,
            "stock": stock
        }
        response = requests.post(f"{API_URL}/nueva_materia", json=data)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al insertar materia prima: {e}")
        return False

def actualizar_materia(materia_id, nombre, descripcion, proveedor_id, stock):
    """Actualizar una materia prima"""
    try:
        data = {
            "nombre": nombre,
            "descripcion": descripcion,
            "proveedor_id": proveedor_id,
            "stock": stock
        }
        response = requests.put(f"{API_URL}/actualizar_materia", params={"materia_id": materia_id}, json=data)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al actualizar materia prima: {e}")
        return False

def eliminar_materia(materia_id):
    """Eliminar una materia prima"""
    try:
        response = requests.delete(f"{API_URL}/eliminar_materia", params={"materia_id": materia_id})
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al eliminar materia prima: {e}")
        return False
    
def obtener_materias_para_combobox():
    """Obtener materias formateadas para combobox (ID - Nombre)"""
    try:
        materias = obtener_materias()
        return [f"{materia[0]} - {materia[1]}" for materia in materias]
    except Exception as e:
        print(f"Error al obtener materias para combobox: {e}")
        return []