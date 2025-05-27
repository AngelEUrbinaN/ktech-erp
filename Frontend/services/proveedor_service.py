"""
Servicio para proveedores - COMPLETO
"""

import requests
from config.api_config import API_URL

def obtener_proveedores():
    """Obtener todos los proveedores"""
    try:
        response = requests.get(f"{API_URL}/obtener_proveedores")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error al obtener proveedores: {e}")
        return []

def obtener_proveedores_para_combobox():
    """Obtener proveedores formateados para combobox"""
    try:
        proveedores = obtener_proveedores()
        return [f"{proveedor[0]} - {proveedor[1]} ({proveedor[2]})" for proveedor in proveedores]
    except Exception as e:
        print(f"Error al formatear proveedores: {e}")
        return []

def insertar_proveedor(nombre, empresa, correo, telefono, direccion):
    """Insertar nuevo proveedor"""
    try:
        data = {
            "nombre": nombre,
            "empresa": empresa,
            "correo": correo,
            "telefono": telefono,
            "direccion": direccion
        }
        
        response = requests.post(f"{API_URL}/nuevo_proveedor", json=data)
        return response.status_code == 200
    except Exception as e:
        print(f"Error al insertar proveedor: {e}")
        return False

def actualizar_proveedor(proveedor_id, nombre, empresa, correo, telefono, direccion):
    """Actualizar proveedor existente"""
    try:
        data = {
            "nombre": nombre,
            "empresa": empresa,
            "correo": correo,
            "telefono": telefono,
            "direccion": direccion
        }
        
        response = requests.put(f"{API_URL}/actualizar_proveedor?proveedor_id={proveedor_id}", json=data)
        return response.status_code == 200
    except Exception as e:
        print(f"Error al actualizar proveedor: {e}")
        return False

def eliminar_proveedor(proveedor_id):
    """Eliminar proveedor"""
    try:
        response = requests.delete(f"{API_URL}/eliminar_proveedor?proveedor_id={proveedor_id}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error al eliminar proveedor: {e}")
        return False

def obtener_proveedor_por_id(proveedor_id):
    """Obtener proveedor específico por ID"""
    try:
        response = requests.get(f"{API_URL}/obtener_proveedor?proveedor_id={proveedor_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error al obtener proveedor por ID: {e}")
        return None