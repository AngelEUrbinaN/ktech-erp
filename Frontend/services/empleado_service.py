"""
Servicio para manejo de empleados
"""

import requests
from config.api_config import API_URL

def obtener_empleados():
    """Obtener todos los empleados"""
    try:
        response = requests.get(f"{API_URL}/obtener_empleados")
        return response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener empleados: {e}")
        return []

def insertar_empleado(nombre, correo, rfc, puesto, departamento_id, salario, fecha_contratacion):
    """Insertar un nuevo empleado"""
    try:
        data = {
            "nombre": nombre,
            "correo": correo,
            "RFC": rfc,
            "puesto": puesto,
            "departamento_id": departamento_id,
            "salario": salario,
            "fecha_contratacion": fecha_contratacion
        }
        response = requests.post(f"{API_URL}/nuevo_empleado", json=data)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al insertar empleado: {e}")
        return False

def actualizar_empleado(empleado_id, nombre, correo, rfc, puesto, departamento_id, salario, fecha_contratacion):
    """Actualizar un empleado existente"""
    try:
        data = {
            "nombre": nombre,
            "correo": correo,
            "RFC": rfc,
            "puesto": puesto,
            "departamento_id": departamento_id,
            "salario": salario,
            "fecha_contratacion": fecha_contratacion
        }
        response = requests.put(f"{API_URL}/actualizar_empleado", params={"empleado_id": empleado_id}, json=data)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al actualizar empleado: {e}")
        return False

def eliminar_empleado(empleado_id):
    """Eliminar un empleado"""
    try:
        response = requests.delete(f"{API_URL}/eliminar_empleado", params={"empleado_id": empleado_id})
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al eliminar empleado: {e}")
        return False