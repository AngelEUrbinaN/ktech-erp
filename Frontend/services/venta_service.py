"""
Servicio para manejo de ventas - ACTUALIZADO
"""

import requests
from config.api_config import API_URL
from services.cliente_service import obtener_clientes
from services.producto_service import obtener_productos

def obtener_ventas():
    """Obtener todas las ventas con información relacionada"""
    try:
        response = requests.get(f"{API_URL}/obtener_ventas")
        if response.status_code != 200:
            return []
        
        ventas = response.json()
        clientes = {c[0]: c[1] for c in obtener_clientes()}
        productos = {p[0]: (p[1], float(p[3])) for p in obtener_productos()}
        
        datos = []
        for v in ventas:
            cliente_nombre = clientes.get(v[1], "Desconocido")
            producto_nombre, precio_unitario = productos.get(v[2], ("Producto desconocido", 0))
            estado = v[5]
            # Formato: (ID Venta, Cliente, Total, Producto, Cantidad, Precio Unitario, Estado)
            datos.append((v[0], cliente_nombre, v[4], producto_nombre, v[3], precio_unitario, estado))
        return datos
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener ventas: {e}")
        return []

def registrar_venta(cliente_id, producto_id, cantidad, precio_unitario):
    """Registrar una nueva venta"""
    try:
        total = float(precio_unitario) * int(cantidad)
        data = {
            "cliente_id": int(cliente_id),
            "producto_id": int(producto_id),
            "cantidad": int(cantidad),
            "total": total,
            "estado": "En espera"
        }
        response = requests.post(f"{API_URL}/nueva_venta", json=data)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al registrar venta: {e}")
        return False

def actualizar_estado_venta(venta_id, nuevo_estado, cantidad_descontar=None):
    """Actualizar estado de una venta"""
    try:
        data = {"estado": nuevo_estado}
        if cantidad_descontar and nuevo_estado == "Finalizado":
            data["cantidad_descontar"] = cantidad_descontar
        
        response = requests.patch(f"{API_URL}/actualizar_estado_venta", params={"venta_id": venta_id}, json=data)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al actualizar estado de venta: {e}")
        return False

def calcular_resumen_ventas():
    """Calcular resumen de ventas (total de ventas y monto total)"""
    ventas = obtener_ventas()
    total_ventas = len(ventas)
    monto_total = sum(float(venta[2]) for venta in ventas) if ventas else 0
    return total_ventas, monto_total

def obtener_ventas_por_cliente(cliente_id):
    """Obtener ventas de un cliente específico"""
    ventas = obtener_ventas()
    return [venta for venta in ventas if venta[2] == cliente_id]

def obtener_ventas_por_producto(producto_id):
    """Obtener ventas de un producto específico"""
    try:
        response = requests.get(f"{API_URL}/obtener_ventas")
        if response.status_code != 200:
            return []
        
        ventas = response.json()
        return [venta for venta in ventas if venta[2] == producto_id]
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener ventas por producto: {e}")
        return []
    
def obtener_venta_por_id(venta_id):
    """Obtener venta específica por ID"""
    try:
        response = requests.get(f"{API_URL}/obtener_venta_por_id?venta_id={venta_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error al obtener venta por ID: {e}")
        return None
    
