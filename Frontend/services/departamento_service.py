"""
Servicio para manejo de departamentos
"""

import requests
from config.api_config import API_URL

def obtener_departamentos():
    """Obtener todos los departamentos"""
    try:
        response = requests.get(f"{API_URL}/obtener_departamentos")
        return response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener departamentos: {e}")
        return []

def insertar_departamento(nombre, presupuesto, descripcion):
    """Insertar un nuevo departamento"""
    try:
        data = {
            "nombre": nombre,
            "presupuesto": presupuesto,
            "descripcion": descripcion
        }
        print("Entrando a If 3.")
        response = requests.post(f"{API_URL}/nuevo_departamento", json=data)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al insertar departamento: {e}")
        return False

def obtener_departamentos_dict():
    """Obtener departamentos como diccionario {id: nombre}"""
    departamentos = obtener_departamentos()
    return {d[0]: d[1] for d in departamentos}

def obtener_departamentos_para_combobox():
    """Obtener departamentos formateados para ComboBox"""
    departamentos = obtener_departamentos()
    return [f"{d[0]} - {d[1]}" for d in departamentos]

def actualizar_departamento(departamento_id, nombre, presupuesto, descripcion):
    """Actualizar un departamento"""
    try:
        data = {
            "nombre": nombre,
            "presupuesto": presupuesto,
            "descripcion": descripcion
        }
        response = requests.put(f"{API_URL}/actualizar_departamento?departamento_id={departamento_id}", json=data)
        return response.status_code == 200
    except Exception as e:
        print(f"Error al actualizar departamento: {e}")
        return False

def eliminar_departamento(departamento_id):
    """Eliminar un departamento"""
    try:
        response = requests.delete(f"{API_URL}/eliminar_departamento?departamento_id={departamento_id}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error al eliminar departamento: {e}")
        return False
