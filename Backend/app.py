from config.db import get_connection
from flask import Flask, request, jsonify
from datetime import datetime
app = Flask(__name__)

@app.route('/nuevo_empleado', methods=['POST'])
def registrar_empleado():
    data = request.get_json()
    print(data)
    nombre = data.get('nombre')
    correo = data.get('correo')
    RFC = data.get('RFC')
    puesto = data.get('puesto')
    departamento_id = data.get('departamento_id')
    salario = data.get('salario')
    fecha_contratacion = data.get('fecha_contratacion')
    if not nombre or not correo or not RFC or not puesto or not departamento_id or not salario or not fecha_contratacion:
        return jsonify({'error': 'Faltan parametros'}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO empleados (nombre, correo, RFC, puesto, departamento_id, salario, fecha_contratacion) VALUES (%s, %s, %s, %s, %s, %s, %s)", (nombre, correo, RFC, puesto, departamento_id, salario, fecha_contratacion))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Empleado registrado con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/obtener_empleados', methods=['GET'])
def obtener_empleados():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT e.empleado_id, e.nombre, e.correo, e.RFC, e.puesto, d.nombre AS departamento, e.salario, e.fecha_contratacion FROM empleados e JOIN departamentos d ON e.departamento_id = d.departamento_id")
        empleados = cursor.fetchall()
        conn.close()
        return jsonify(empleados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/actualizar_empleado', methods=['PUT'])
def actualizar_empleado():
    empleado_id = request.args.get('empleado_id', type=int)
    data = request.get_json()
    
    nombre = data.get('nombre')
    correo = data.get('correo')
    RFC = data.get('RFC')
    puesto = data.get('puesto')
    departamento_id = data.get('departamento_id')
    salario = data.get('salario')
    fecha_contratacion = data.get('fecha_contratacion')

    if not empleado_id or not nombre or not correo or not RFC or not puesto or not departamento_id or not salario or not fecha_contratacion:
        return jsonify({'error': 'Faltan parametros'}), 400

    from datetime import datetime
    try:
        fecha_contratacion = datetime.strptime(fecha_contratacion, "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE empleados 
            SET nombre = %s, correo = %s, RFC = %s, puesto = %s, 
                departamento_id = %s, salario = %s, fecha_contratacion = %s 
            WHERE empleado_id = %s
        """, (nombre, correo, RFC, puesto, departamento_id, salario, fecha_contratacion, empleado_id))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Empleado actualizado con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route('/eliminar_empleado', methods=['DELETE'])
def eliminar_empleado():
    try:
        empleado_id = request.args.get('empleado_id', type=int)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM empleados WHERE empleado_id = %s", (empleado_id,))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Empleado eliminado con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nuevo_usuario', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    correo = data.get('correo')
    contrasena = data.get('contrasena')
    empleado_id = data.get('empleado_id')

    try:
        empleado_id = int(empleado_id)
    except (TypeError, ValueError):
        return jsonify({'error': 'ID de empleado inválido'}), 400

    if not correo or not contrasena or not empleado_id:
        return jsonify({'error': 'Faltan parametros'}), 400

    print(data)
    print("empleado_id", empleado_id)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (correo, contrasena, empleado_id) VALUES (%s, %s, %s)",
            (correo, contrasena, empleado_id)
        )
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Usuario registrado con exito"}), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
@app.route('/obtener_usuarios', methods=['GET'])
def obtener_usuarios():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        conn.close()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500    
    
@app.route('/actualizar_contrasena_usuario', methods=['PATCH'])
def actualizar_usuario():
    usuario_id = request.args.get('usuario_id', type=int)
    data = request.get_json()
    contrasena = data.get('contrasena')
    if not usuario_id or not contrasena:
        return jsonify({'error': 'Faltan parametros'}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET contrasena = %s WHERE usuario_id = %s", (contrasena, usuario_id))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Contrasena actualizada con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/eliminar_usuario', methods=['DELETE'])
def eliminar_usuario():
    usuario_id = request.args.get('usuario_id', type=int)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE usuario_id = %s", (usuario_id,))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Usuario eliminado con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nuevo_departamento', methods=['POST'])
def registrar_departamento():
    data = request.get_json()
    nombre = data.get('nombre')
    presupuesto = data.get('presupuesto')
    descripcion = data.get('descripcion')
    if not nombre or not presupuesto or not descripcion:
        return jsonify({'error': 'Faltan parametros'}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO departamentos (nombre, presupuesto, descripcion) VALUES (%s, %s, %s)", (nombre, presupuesto, descripcion))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Departamento registrado con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/obtener_departamentos', methods=['GET'])
def obtener_departamentos():    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM departamentos")
        departamentos = cursor.fetchall()
        conn.close()
        return jsonify(departamentos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/actualizar_departamento', methods=['PUT'])
def actualizar_departamento():
    departamento_id = request.args.get("departamento_id", type=int)
    data = request.get_json()

    nombre = data.get("nombre")
    presupuesto = data.get("presupuesto")
    descripcion = data.get("descripcion")

    if not departamento_id or not nombre or presupuesto is None or not descripcion:
        return jsonify({"error": "Faltan parámetros"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE departamentos 
            SET nombre = %s, presupuesto = %s, descripcion = %s 
            WHERE departamento_id = %s
        """, (nombre, presupuesto, descripcion, departamento_id))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Departamento actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/eliminar_departamento', methods=['DELETE'])
def eliminar_departamento():
    departamento_id = request.args.get("departamento_id", type=int)

    if not departamento_id:
        return jsonify({"error": "Falta el ID del departamento"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM departamentos WHERE departamento_id = %s", (departamento_id,))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Departamento eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nuevo_cliente', methods=['POST'])
def registrar_cliente():
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')
    telefono = data.get('telefono')
    direccion = data.get('direccion')
    if not nombre or not correo or not telefono or not direccion:
        return jsonify({'error': 'Faltan parametros'}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes (nombre, correo, telefono, direccion) VALUES (%s, %s, %s, %s)", (nombre, correo, telefono, direccion))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Cliente registrado con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/obtener_clientes', methods=['GET'])
def obtener_clientes():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        conn.close()
        return jsonify(clientes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/nuevo_proveedor', methods=['POST'])
def registrar_proveedor():
    data = request.get_json()
    nombre = data.get('nombre')
    nombre_empresa = data.get('empresa')
    correo = data.get('correo')
    telefono = data.get('telefono')
    direccion = data.get('direccion')
    if not nombre or not correo or not telefono or not direccion:
        return jsonify({'error': 'Faltan parametros'}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO proveedores (nombre, nombre_empresa ,correo, telefono, direccion) VALUES (%s, %s, %s, %s, %s)", (nombre, nombre_empresa, correo, telefono, direccion))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Proveedor registrado con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/obtener_proveedores', methods=['GET'])
def obtener_proveedores():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proveedores")
        proveedores = cursor.fetchall()
        conn.close()
        return jsonify(proveedores), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/nueva_materia', methods=['POST'])
def registrar_materia():
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    proveedor_id = data.get('proveedor_id')
    stock = data.get('stock')
    if not nombre or not descripcion or not proveedor_id or not stock:
        return jsonify({'error': 'Faltan parametros'}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO materias (nombre, descripcion, proveedor_id, stock) VALUES (%s, %s, %s, %s)", (nombre, descripcion, proveedor_id, stock))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Materia registrada con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/obtener_materias', methods=['GET'])
def obtener_materias():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM materias")
        materias = cursor.fetchall()
        conn.close()
        return jsonify(materias), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/actualizar_materia', methods=['PUT'])
def actualizar_materia():
    data = request.get_json()
    materia_id = request.args.get('materia_id', type=int)
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    proveedor_id = data.get('proveedor_id')
    stock = data.get('stock')
    try:
        materia_id = int(materia_id)
        proveedor_id = int(proveedor_id)
    except (TypeError, ValueError):
        return jsonify({'error': 'ID de materia o proveedor inválido'}), 400

    if not materia_id or not nombre or not descripcion or not proveedor_id or not stock:
        return jsonify({'error': 'Faltan parametros'}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE materias SET nombre = %s, descripcion = %s, proveedor_id = %s, stock = %s WHERE materia_id = %s", (nombre, descripcion, proveedor_id, stock, materia_id))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Materia actualizada con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/actualizar_stock_materia', methods=['PATCH'])
def actualizar_stock_materia():
    data = request.get_json()
    materia_id = request.args.get('materia_id', type=int)
    stock = data.get('stock')
    if not materia_id or not stock:
        return jsonify({'error': 'Faltan parametros'}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE materias SET stock = %s WHERE materia_id = %s", (stock, materia_id))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Stock de la materia actualizado con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/eliminar_materia', methods=['DELETE'])
def eliminar_materia():
    materia_id = request.args.get('materia_id', type=int)
    if not materia_id:
        return jsonify({'error': 'Faltan parametros'}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM materias WHERE materia_id = %s", (materia_id,))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Materia eliminada con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nuevo_producto', methods=['POST'])
def registrar_producto():
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    precio_unitario = data.get('precio_unitario')
    stock = data.get('stock')
    if not nombre or not descripcion or not precio_unitario or not stock:
        return jsonify({'error': 'Faltan parametros'}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, descripcion, precio_unitario, stock) VALUES (%s, %s, %s, %s)", (nombre, descripcion, precio_unitario, stock))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Producto registrado con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/obtener_productos', methods=['GET'])
def obtener_productos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        conn.close()
        return jsonify(productos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/obtener_producto_por_id', methods=['GET'])
def obtener_producto_por_id():
    producto_id = request.args.get('producto_id', type=int)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE producto_id = %s", (producto_id,))
        producto = cursor.fetchone()
        conn.close()
        return jsonify(producto), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/actualizar_producto', methods=['PUT'])
def actualizar_producto():
    data = request.get_json()
    producto_id = request.args.get('producto_id', type=int)
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    precio_unitario = data.get('precio_unitario')
    stock = data.get('stock')
    if not producto_id or not nombre or not descripcion or not precio_unitario or not stock:
        return jsonify({'error': 'Faltan parametros'}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE productos SET nombre = %s, descripcion = %s, precio_unitario = %s, stock = %s WHERE producto_id = %s", (nombre, descripcion, precio_unitario, stock, producto_id))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Producto actualizado con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/actualizar_stock_producto', methods=['PATCH'])
def actualizar_stock_producto():
    data = request.get_json()
    producto_id = request.args.get('producto_id', type=int)
    stock = data.get('stock')
    if not producto_id or not stock:
        return jsonify({'error': 'Faltan parametros'}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE productos SET stock = %s WHERE producto_id = %s", (stock, producto_id))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Stock actualizado con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/eliminar_producto', methods=['DELETE'])
def eliminar_producto():
    producto_id = request.args.get('producto_id', type=int)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE producto_id = %s", (producto_id,))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Producto eliminado con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/agregar_materia_a_producto', methods=['POST'])
def agregar_materia_a_producto():
    data = request.get_json()
    producto_id = request.args.get('producto_id', type=int)
    materia_id = data.get('materia_id')
    cantidad = data.get('cantidad')
    try:
        producto_id = int(producto_id)
        materia_id = int(materia_id)
        cantidad = int(cantidad)
    except (TypeError, ValueError):
        return jsonify({'error': 'ID de materia, producto o cantidad inválidos'}), 400
    
    if not producto_id or not materia_id or not cantidad:
        return jsonify({'error': 'Faltan parametros'}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO lista_materias (producto_id, materia_id, cantidad) VALUES (%s, %s, %s)", (producto_id, materia_id, cantidad))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Materia agregada al producto con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/obtener_materias_de_producto', methods=['GET'])
def obtener_materias_de_producto():
    producto_id = request.args.get('producto_id', type=int)
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lista_materias WHERE producto_id = %s", (producto_id,))
        materias = cursor.fetchall()
        conn.close()
        return jsonify(materias), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nueva_venta', methods=['POST'])
def registrar_venta():
    data = request.get_json()
    cliente_id = data.get('cliente_id')
    producto_id = data.get('producto_id')
    cantidad = data.get('cantidad')
    total = data.get('total')
    estado = data.get('estado')
    if not cliente_id or not producto_id or not cantidad or not total or not estado:
        return jsonify({'error': 'Faltan parametros'}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ventas (cliente_id, producto_id, cantidad, total, estado) VALUES (%s, %s, %s, %s, %s)", (cliente_id, producto_id, cantidad, total, estado))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Venta registrada con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/obtener_ventas', methods=['GET'])
def obtener_ventas():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ventas")
        ventas = cursor.fetchall()
        conn.close()
        return jsonify(ventas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/actualizar_estado_venta', methods=['PATCH'])
def actualizar_estado_venta():
    data = request.get_json()
    venta_id = request.args.get('venta_id', type=int)
    estado = data.get('estado')
    cantidad_descontar = data.get('cantidad_descontar')
    
    if not venta_id or not estado:
        return jsonify({'error': 'Faltan parametros'}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("UPDATE ventas SET estado = %s WHERE venta_id = %s", (estado, venta_id))

        if estado == "Finalizado" and cantidad_descontar:

            cursor.execute("SELECT producto_id FROM ventas WHERE venta_id = %s", (venta_id,))
            result = cursor.fetchone()
            if result:
                producto_id = result[0]

                cursor.execute("UPDATE productos SET stock = stock - %s WHERE producto_id = %s", (cantidad_descontar, producto_id))
        
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Estado de la venta actualizado con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nueva_orden_produccion', methods=['POST'])
def registrar_orden_produccion():
    data = request.get_json()
    producto_id = data.get('producto_id')
    cantidad = data.get('cantidad')
    fecha_inicio = data.get('fecha_inicio')
    fecha_fin = data.get('fecha_fin')
    estado = data.get('estado')
    if not producto_id or not cantidad or not fecha_inicio or not fecha_fin or not estado:
        return jsonify({'error': 'Faltan parametros'}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ordenes_produccion (producto_id, cantidad, fecha_inicio, fecha_fin, estado) VALUES (%s, %s, %s, %s, %s)", (producto_id, cantidad, fecha_inicio, fecha_fin, estado))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Orden de produccion registrada con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nueva_orden_materia', methods=['POST'])
def registrar_orden_materia():
    data = request.get_json()
    materia_id = data.get('materia_id')
    cantidad = data.get('cantidad')
    fecha = data.get('fecha')
    estado = data.get('estado')
    if not materia_id or not cantidad or not fecha or not estado:
        return jsonify({'error': 'Faltan parametros'}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ordenes_materias (materia_id, cantidad, fecha, estado) VALUES (%s, %s, %s, %s)", (materia_id, cantidad, fecha, estado))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Orden de materia registrada con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/obtener_ordenes_materia', methods=['GET'])
def obtener_ordenes_materia():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ordenes_materias")
        ordenes_materia = cursor.fetchall()
        conn.close()
        return jsonify(ordenes_materia), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/obtener_ordenes_produccion', methods=['GET'])
def obtener_ordenes_produccion():
    estado = request.args.get('estado')
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if estado:
            cursor.execute("SELECT * FROM ordenes_produccion WHERE estado = %s", (estado,))
        else:
            cursor.execute("SELECT * FROM ordenes_produccion")
        ordenes_produccion = cursor.fetchall()
        conn.close()
        return jsonify(ordenes_produccion), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/actualizar_estado_orden_produccion', methods=['PATCH'])
def actualizar_estado_orden_produccion():
    data = request.get_json()
    orden_id = request.args.get('orden_id', type=int)
    estado = data.get('estado')

    print(orden_id)
    print(estado)

    if not orden_id or not estado:
        return jsonify({'error': 'Faltan parámetros'}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()

        if estado == "Finalizado":
            cursor.execute("SELECT producto_id, cantidad FROM ordenes_produccion WHERE orden_produccion_id = %s", (orden_id,))
            result = cursor.fetchone()
            if result:
                producto_id, cantidad = result
                cursor.execute("UPDATE productos SET stock = stock + %s WHERE producto_id = %s", (cantidad, producto_id))

        cursor.execute("UPDATE ordenes_produccion SET estado = %s WHERE orden_produccion_id = %s", (estado, orden_id))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Estado actualizado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/actualizar_estado_orden_materia', methods=['PATCH'])
def actualizar_estado_orden_materia():
    data = request.get_json()
    orden_id = request.args.get('orden_id', type=int)
    estado = data.get('estado')
    cantidad_descontar = data.get('cantidad_descontar')

    if not orden_id or not estado:
        return jsonify({'error': 'Faltan parámetros'}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE ordenes_materias SET estado = %s WHERE orden_materias_id = %s", (estado, orden_id))

        if estado == "Finalizado" and cantidad_descontar:
            cursor.execute("SELECT materia_id FROM ordenes_materias WHERE orden_materias_id = %s", (orden_id,))
            result = cursor.fetchone()
            if result:
                materia_id = result[0]
                cursor.execute("UPDATE materias SET stock = stock - %s WHERE materia_id = %s", (cantidad_descontar, materia_id))

        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Orden de material actualizada"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/nueva_orden_compra', methods=['POST'])
def registrar_orden_compra():
    data = request.get_json()
    materia_id = data.get('materia_id')
    proveedor_id = data.get('proveedor_id')
    cantidad = data.get('cantidad')
    precio_unitario = data.get('precio_unitario')
    total = data.get('total')
    fecha = data.get('fecha')
    estado = data.get('estado')
    
    if not materia_id or not proveedor_id or not cantidad or not precio_unitario or not total or not fecha or not estado:
        return jsonify({'error': 'Faltan parametros'}), 400
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ordenes_compra (materia_id, proveedor_id, cantidad, precio_unitario, total, fecha, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (materia_id, proveedor_id, cantidad, precio_unitario, total, fecha, estado)
        )
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Orden de compra registrada con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/actualizar_estado_orden_compra', methods=['PATCH'])
def actualizar_estado_orden_compra():
    orden_id = request.args.get("orden_id", type=int)
    data = request.get_json()
    estado = data.get("estado")

    if not orden_id or not estado:
        return jsonify({"error": "Faltan parámetros"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE ordenes_compra SET estado = %s WHERE orden_compra_id = %s", (estado, orden_id))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Estado actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/procesar_orden_compra', methods=['PATCH'])
def procesar_orden_compra():
    orden_id = request.args.get("orden_id", type=int)
    data = request.get_json()

    estado = data.get("estado")
    materia_id = data.get("materia_id")
    cantidad_sumar = data.get("cantidad_sumar")

    if not orden_id or not estado:
        return jsonify({"error": "Faltan parámetros"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE ordenes_compra SET estado = %s WHERE orden_compra_id = %s", (estado, orden_id))

        if estado == "Finalizado" and materia_id and cantidad_sumar:
            cursor.execute("UPDATE materias SET stock = stock + %s WHERE materia_id = %s", (cantidad_sumar, materia_id))

        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Orden de compra procesada"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/obtener_ordenes_compra', methods=['GET'])
def obtener_ordenes_compra():
    """Obtener órdenes de compra con filtro opcional por estado"""
    filtro_estado = request.args.get('estado')
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if filtro_estado:
            cursor.execute("SELECT * FROM ordenes_compra WHERE estado = %s", (filtro_estado,))
        else:
            cursor.execute("SELECT * FROM ordenes_compra")
            
        ordenes_compra = cursor.fetchall()
        conn.close()
        return jsonify(ordenes_compra), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/actualizar_proveedor', methods=['PUT'])
def actualizar_proveedor():
    proveedor_id = request.args.get("proveedor_id", type=int)
    data = request.get_json()
    
    nombre = data.get("nombre")
    nombre_empresa = data.get("empresa", "")
    correo = data.get("correo")
    telefono = data.get("telefono")
    direccion = data.get("direccion")

    if not proveedor_id or not nombre or not correo or not telefono or not direccion:
        return jsonify({"error": "Faltan parámetros"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE proveedores 
            SET nombre = %s, nombre_empresa = %s, correo = %s, telefono = %s, direccion = %s 
            WHERE proveedor_id = %s
        """, (nombre, nombre_empresa, correo, telefono, direccion, proveedor_id))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Proveedor actualizado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/eliminar_proveedor', methods=['DELETE'])
def eliminar_proveedor():
    proveedor_id = request.args.get("proveedor_id", type=int)

    if not proveedor_id:
        return jsonify({"error": "Falta el ID"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM proveedores WHERE proveedor_id = %s", (proveedor_id,))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Proveedor eliminado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/obtener_proveedor', methods=['GET'])
def obtener_proveedor():
    """Obtener proveedor específico por ID"""
    proveedor_id = request.args.get('proveedor_id', type=int)

    if not proveedor_id:
        return jsonify({'error': 'Falta el ID del proveedor'}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proveedores WHERE id = %s", (proveedor_id,))
        proveedor = cursor.fetchone()
        conn.close()
        
        if proveedor:
            return jsonify(proveedor), 200
        else:
            return jsonify({"error": "Proveedor no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/obtener_ingresos_finalizados', methods=['GET'])
def obtener_ingresos_finalizados():
    """Obtener ingresos (ventas finalizadas)"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.venta_id, p.nombre as producto, v.cantidad, v.total
            FROM ventas v
            JOIN productos p ON v.producto_id = p.producto_id
            WHERE v.estado = 'Finalizado'
            ORDER BY v.venta_id DESC
        """)
        ingresos = cursor.fetchall()
        conn.close()
        return jsonify(ingresos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/obtener_egresos_finalizados', methods=['GET'])
def obtener_egresos_finalizados():
    """Obtener egresos (compras finalizadas)"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT oc.orden_compra_id, m.nombre as materia, oc.cantidad, oc.total, oc.fecha
            FROM ordenes_compra oc
            JOIN materias m ON oc.materia_id = m.materia_id
            WHERE oc.estado = 'Finalizado'
            ORDER BY oc.fecha DESC
        """)
        egresos = cursor.fetchall()
        conn.close()
        return jsonify(egresos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/resumen_ingresos', methods=['GET'])
def resumen_ingresos():
    """Calcular resumen de ingresos"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as total_ventas, COALESCE(SUM(total), 0) as monto_total
            FROM ventas
            WHERE estado = 'Finalizado'
        """)
        result = cursor.fetchone()
        conn.close()
        
        return jsonify({
            'total_ventas': result[0],
            'monto_total': float(result[1])
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/resumen_egresos', methods=['GET'])
def resumen_egresos():
    """Calcular resumen de egresos"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as total_compras, COALESCE(SUM(total), 0) as monto_total
            FROM ordenes_compra
            WHERE estado = 'Finalizado'
        """)
        result = cursor.fetchone()
        conn.close()
        
        return jsonify({
            'total_compras': result[0],
            'monto_total': float(result[1])
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/obtener_tickets', methods=['GET'])
def obtener_tickets():
    """Obtener tickets con filtro opcional por estado"""
    filtro_estado = request.args.get('estado')
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if filtro_estado:
            cursor.execute("""
                SELECT t.ticket_id, c.nombre as cliente, t.venta_id, t.fecha, t.descripcion_problema, t.estado
                FROM tickets t
                JOIN clientes c ON t.cliente_id = c.cliente_id
                WHERE t.estado = %s
                ORDER BY t.ticket_id DESC
            """, (filtro_estado,))
        else:
            cursor.execute("""
                SELECT t.ticket_id, c.nombre as cliente, t.venta_id, t.fecha, t.descripcion_problema, t.estado
                FROM tickets t
                JOIN clientes c ON t.cliente_id = c.cliente_id
                ORDER BY t.ticket_id DESC
            """)
            
        tickets = cursor.fetchall()
        conn.close()
        return jsonify(tickets), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/nuevo_ticket', methods=['POST'])
def registrar_ticket():
    """Registrar nuevo ticket"""
    data = request.get_json()
    cliente_id = data.get('cliente_id')
    venta_id = data.get('venta_id')
    descripcion = data.get('descripcion')
    fecha = data.get('fecha')
    estado = data.get('estado')

    if not cliente_id or not venta_id or not descripcion or not fecha or not estado:
        return jsonify({'error': 'Faltan parametros'}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tickets (cliente_id, venta_id, descripcion_problema, fecha, estado) VALUES (%s, %s, %s, %s, %s)",
            (cliente_id, venta_id, descripcion, fecha, estado)
        )
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Ticket registrado con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/actualizar_estado_ticket', methods=['PATCH'])
def actualizar_estado_ticket():
    """Actualizar estado de ticket"""
    data = request.get_json()
    ticket_id = request.args.get('ticket_id', type=int)
    estado = data.get('estado')

    if not ticket_id or not estado:
        return jsonify({'error': 'Faltan parametros'}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tickets SET estado = %s WHERE ticket_id = %s", (estado, ticket_id))
        conn.commit()
        conn.close()
        return jsonify({"mensaje": "Estado del ticket actualizado con exito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/obtener_ticket', methods=['GET'])
def obtener_ticket():
    """Obtener ticket específico por ID"""
    ticket_id = request.args.get('ticket_id', type=int)

    if not ticket_id:
        return jsonify({'error': 'Falta el ID del ticket'}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.ticket_id, c.nombre as cliente, t.venta_id, t.fecha, t.descripcion_problema, t.estado
            FROM tickets t
            JOIN clientes c ON t.cliente_id = c.cliente_id
            WHERE t.ticket_id = %s
        """, (ticket_id,))
        ticket = cursor.fetchone()
        conn.close()
        
        if ticket:
            return jsonify(ticket), 200
        else:
            return jsonify({"error": "Ticket no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/obtener_venta_por_id', methods=['GET'])
def obtener_venta_por_id():
    """Obtener venta específica por ID"""
    venta_id = request.args.get('venta_id', type=int)

    if not venta_id:
        return jsonify({'error': 'Falta el ID de la venta'}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.venta_id, v.cliente_id, v.total, p.nombre as producto, v.cantidad, p.precio_unitario, v.estado
            FROM ventas v
            JOIN productos p ON v.producto_id = p.producto_id
            WHERE v.venta_id = %s
        """, (venta_id,))
        venta = cursor.fetchone()
        conn.close()
        
        if venta:
            return jsonify(venta), 200
        else:
            return jsonify({"error": "Venta no encontrada"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    data = request.get_json()
    correo = data.get("correo")
    contrasena = data.get("contrasena")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.usuario_id, d.departamento_id
        FROM usuarios u 
        JOIN empleados e ON u.empleado_id = e.empleado_id 
        JOIN departamentos d ON e.departamento_id = d.departamento_id 
        WHERE u.correo = %s AND u.contrasena = %s
    """, (correo, contrasena))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        usuario_id, departamento_id = resultado
        return jsonify({
            "success": True,
            "usuario_id": usuario_id,
            "departamento_id": departamento_id
        }), 200
    else:
        return jsonify({"success": False}), 401

if __name__ == '__main__':
    app.run(debug=True, threaded=True)