"""
Servicio para órdenes de compra - ACTUALIZADO
"""

import requests
from config.api_config import API_URL

def obtener_ordenes_compra(filtro_estado=None):
    """Obtener todas las órdenes de compra con filtro opcional"""
    try:
        url = f"{API_URL}/obtener_ordenes_compra"
        if filtro_estado:
            url += f"?estado={filtro_estado}"
        
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error al obtener órdenes de compra: {e}")
        return []

def insertar_orden_compra(materia_id, proveedor_id, cantidad, precio_unitario, total, fecha, estado):
    """Insertar nueva orden de compra"""
    try:
        data = {
            "materia_id": materia_id,
            "proveedor_id": proveedor_id,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "total": total,
            "fecha": fecha,
            "estado": estado
        }
        
        response = requests.post(f"{API_URL}/nueva_orden_compra", json=data)
        return response.status_code == 200
    except Exception as e:
        print(f"Error al insertar orden de compra: {e}")
        return False

def actualizar_estado_orden_compra(orden_id, estado):
    """Actualizar estado de orden de compra (versión simple)"""
    try:
        data = {"estado": estado}
        response = requests.patch(f"{API_URL}/actualizar_estado_orden_compra?orden_id={orden_id}", json=data)
        return response.status_code == 200
    except Exception as e:
        print(f"Error al actualizar estado de orden de compra: {e}")
        return False

def actualizar_estado_orden_compra_con_stock(orden_id, estado, materia_id, cantidad_sumar):
    """Actualizar estado de orden de compra y stock si es necesario"""
    try:
        data = {
            "estado": estado,
            "materia_id": materia_id,
            "cantidad_sumar": cantidad_sumar
        }
        response = requests.patch(f"{API_URL}/procesar_orden_compra?orden_id={orden_id}", json=data)
        return response.status_code == 200
    except Exception as e:
        print(f"Error al procesar orden de compra: {e}")
        return False