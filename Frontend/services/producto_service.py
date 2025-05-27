"""
Servicio para manejo de productos
"""

import requests
from config.api_config import API_URL

def obtener_productos():
    """Obtener todos los productos"""
    try:
        response = requests.get(f"{API_URL}/obtener_productos")
        return response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener productos: {e}")
        return []

def obtener_producto_por_id(producto_id):
    """Obtener producto por ID"""
    try:
        response = requests.get(f"{API_URL}/obtener_producto_por_id", params={"producto_id": producto_id})
        if response.status_code == 200:
            p = response.json()
            return {
                "id_producto": p[0],
                "nombre": p[1],
                "descripcion": p[2],
                "precio_unitario": float(p[3]),
                "stock_actual": int(p[4])
            }
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener producto por ID: {e}")
        return None

def obtener_producto_por_nombre(nombre):
    """Buscar producto por nombre"""
    productos = obtener_productos()
    for p in productos:
        if p[1].lower() == nombre.lower():
            return {
                "id_producto": p[0],
                "nombre": p[1],
                "descripcion": p[2],
                "precio_unitario": float(p[3]),
                "stock_actual": int(p[4])
            }
    return None

def insertar_producto(nombre, descripcion, precio_unitario, stock):
    """Insertar un nuevo producto"""
    try:
        data = {
            "nombre": nombre,
            "descripcion": descripcion,
            "precio_unitario": precio_unitario,
            "stock": stock
        }
        response = requests.post(f"{API_URL}/nuevo_producto", json=data)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al insertar producto: {e}")
        return False

def actualizar_producto(producto_id, nombre, descripcion, precio_unitario, stock):
    """Actualizar un producto"""
    try:
        data = {
            "nombre": nombre,
            "descripcion": descripcion,
            "precio_unitario": precio_unitario,
            "stock": stock
        }
        response = requests.put(f"{API_URL}/actualizar_producto", params={"producto_id": producto_id}, json=data)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al actualizar producto: {e}")
        return False

def eliminar_producto(producto_id):
    """Eliminar un producto"""
    try:
        response = requests.delete(f"{API_URL}/eliminar_producto", params={"producto_id": producto_id})
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al eliminar producto: {e}")
        return False

def actualizar_stock_producto(producto_id, nuevo_stock):
    """Actualizar stock de un producto"""
    try:
        data = {"stock": nuevo_stock}
        response = requests.patch(f"{API_URL}/actualizar_stock_producto", params={"producto_id": producto_id}, json=data)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al actualizar stock: {e}")
        return False

def descontar_stock_producto(producto_id, cantidad):
    """Descontar stock de un producto"""
    try:
        producto = obtener_producto_por_id(producto_id)
        if producto:
            nuevo_stock = producto["stock_actual"] - cantidad
            return actualizar_stock_producto(producto_id, nuevo_stock)
        return False
    except Exception as e:
        print(f"Error al descontar stock: {e}")
        return False

def agregar_materia_a_producto(producto_id, materia_id, cantidad):
    """Agregar materia prima a un producto"""
    try:
        data = {
            "materia_id": materia_id,
            "cantidad": cantidad
        }
        response = requests.post(f"{API_URL}/agregar_materia_a_producto", params={"producto_id": producto_id}, json=data)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error al agregar materia a producto: {e}")
        return False

def obtener_materias_de_producto(producto_id):
    """Obtener materias primas de un producto"""
    try:
        response = requests.get(f"{API_URL}/obtener_materias_de_producto", params={"producto_id": producto_id})
        return response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener materias del producto: {e}")
        return []

def obtener_productos_para_combobox():
    """Obtener productos formateados para combobox (ID - Nombre)"""
    try:
        productos = obtener_productos()
        return [f"{producto[0]} - {producto[1]}" for producto in productos]
    except Exception as e:
        print(f"Error al obtener productos para combobox: {e}")
        return []