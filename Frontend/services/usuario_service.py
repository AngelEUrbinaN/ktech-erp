"""
Servicio para manejo de usuarios
"""

import requests
from config.api_config import API_URL

def obtener_usuarios():
    """Obtener todos los usuarios"""
    try:
        response = requests.get(f"{API_URL}/obtener_usuarios")
        return response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener usuarios: {e}")
        return []

def insertar_usuario(correo, password, empleado_id):
    """Insertar un nuevo usuario"""
    try:
        data = {
            "correo": correo,
            "contrasena": password,
            "empleado_id": empleado_id
        }
        response = requests.post(f"{API_URL}/nuevo_usuario", json=data)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al insertar usuario: {e}")
        return False

def eliminar_usuario(usuario_id):
    """Eliminar un usuario"""
    try:
        response = requests.delete(f"{API_URL}/eliminar_usuario", params={"usuario_id": usuario_id})
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al eliminar usuario: {e}")
        return False

def actualizar_password_usuario(usuario_id, nueva_password):
    """Actualizar contraseña de un usuario"""
    try:
        data = {"contrasena": nueva_password}
        response = requests.patch(f"{API_URL}/actualizar_contrasena_usuario", params={"usuario_id": usuario_id}, json=data)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al actualizar contraseña: {e}")
        return False

def verificar_usuario_existente(empleado_id):
    """Verificar si un empleado ya tiene usuario"""
    usuarios = obtener_usuarios()
    for usuario in usuarios:
        if len(usuario) > 3 and usuario[3] == empleado_id:
            return True
    return False