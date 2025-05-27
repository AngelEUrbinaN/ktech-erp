"""
Servicio para manejo de clientes
"""

import requests
from config.api_config import API_URL

def obtener_clientes():
    """Obtener todos los clientes"""
    try:
        response = requests.get(f"{API_URL}/obtener_clientes")
        return response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener clientes: {e}")
        return []

def insertar_cliente(nombre, correo, telefono, direccion):
    """Insertar un nuevo cliente"""
    try:
        data = {
            "nombre": nombre,
            "correo": correo,
            "telefono": telefono,
            "direccion": direccion
        }
        response = requests.post(f"{API_URL}/nuevo_cliente", json=data)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al insertar cliente: {e}")
        return False

def buscar_cliente_por_email(email):
    """Buscar cliente por email"""
    clientes = obtener_clientes()
    for c in clientes:
        if c[2].lower() == email.lower():
            return c
    return None

def obtener_clientes_para_combobox():
    """Obtener clientes en formato para ComboBox (ID - Nombre)"""
    try:
        response = requests.get(f"{API_URL}/obtener_clientes")
        if response.status_code == 200:
            clientes = response.json()
            # Formatear como "ID - Nombre"
            return [f"{cliente[0]} - {cliente[1]}" for cliente in clientes]
        return []
    except Exception as e:
        print(f"Error al obtener clientes para combobox: {e}")
        return []