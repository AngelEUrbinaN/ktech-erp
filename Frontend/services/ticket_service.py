"""
Servicio para tickets de atención al cliente
"""

import requests
from config.api_config import API_URL

def obtener_tickets(filtro_estado=None):
    """Obtener todos los tickets con filtro opcional"""
    try:
        url = f"{API_URL}/obtener_tickets"
        if filtro_estado:
            url += f"?estado={filtro_estado}"
        
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error al obtener tickets: {e}")
        return []

def insertar_ticket(cliente_id, venta_id, descripcion, fecha, estado):
    """Insertar nuevo ticket"""
    try:
        data = {
            "cliente_id": cliente_id,
            "venta_id": venta_id,
            "descripcion": descripcion,
            "fecha": fecha,
            "estado": estado
        }
        
        response = requests.post(f"{API_URL}/nuevo_ticket", json=data)
        return response.status_code == 200
    except Exception as e:
        print(f"Error al insertar ticket: {e}")
        return False

def actualizar_estado_ticket(ticket_id, estado):
    """Actualizar estado de ticket"""
    try:
        data = {"estado": estado}
        response = requests.patch(f"{API_URL}/actualizar_estado_ticket?ticket_id={ticket_id}", json=data)
        return response.status_code == 200
    except Exception as e:
        print(f"Error al actualizar estado de ticket: {e}")
        return False

def obtener_ticket_por_id(ticket_id):
    """Obtener ticket específico por ID"""
    try:
        response = requests.get(f"{API_URL}/obtener_ticket?ticket_id={ticket_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error al obtener ticket por ID: {e}")
        return None