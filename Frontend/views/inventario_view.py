"""
Vista del módulo de Inventario - CORREGIDA
"""

import customtkinter as ctk
from tkinter import messagebox
from views.base_view import BaseView
from services.producto_service import (
    obtener_productos, insertar_producto, actualizar_producto, eliminar_producto,
    agregar_materia_a_producto, obtener_materias_de_producto, obtener_producto_por_id
)
from services.materia_prima_service import (
    obtener_materias, insertar_materia, actualizar_materia, eliminar_materia
)
from services.orden_produccion_service import obtener_ordenes_produccion, insertar_orden_produccion, actualizar_estado_orden_produccion
from services.orden_materia_service import obtener_ordenes_materia, actualizar_estado_orden_materia
from services.orden_compra_service import obtener_ordenes_compra, insertar_orden_compra, actualizar_estado_orden_compra
from services.proveedor_service import obtener_proveedores
from services.venta_service import obtener_ventas, actualizar_estado_venta

class InventarioView(BaseView):
    def __init__(self, parent):
        # CORREGIDO: Eliminé la definición duplicada de __init__
        self.producto_seleccionado = None
        self.materia_seleccionada = None
        self.orden_produccion_seleccionada = None
        self.orden_materia_seleccionada = None
        self.orden_compra_seleccionada = None
        self.venta_seleccionada = None
        super().__init__(parent)
    
    def crear_vista(self):
        """Crear la vista del módulo de inventario"""
        # Header
        self.crear_header("Módulo de Inventario")
        
        # Información del módulo
        info_frame = ctk.CTkFrame(self.parent, fg_color="#E5E5E5")
        info_frame.pack(fill="x", padx=20, pady=(10, 0))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="ℹ️ Módulo de Inventario",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="black"
        )
        info_label.pack(pady=10)
        
        info_desc = ctk.CTkLabel(
            info_frame,
            text="Visualiza el estado del stock de productos y materias primas. Controla órdenes de producción y abastecimiento de materiales.",
            font=ctk.CTkFont(size=12),
            text_color="black"
        )
        info_desc.pack(pady=(0, 10))
        
        # Pestañas
        self.tabs = ctk.CTkTabview(self.parent)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear pestañas
        self.tab_productos = self.tabs.add("Productos")
        self.tab_materias = self.tabs.add("Materia Prima")
        self.tab_ordenes_produccion = self.tabs.add("Órdenes de Producción")
        self.tab_ordenes_materiales = self.tabs.add("Órdenes de Materiales")
        self.tab_ordenes_compra = self.tabs.add("Órdenes de Compra")
        self.tab_ventas = self.tabs.add("Ventas")
        
        # Configurar pestañas
        self.configurar_tab_productos()
        self.configurar_tab_materias()
        self.configurar_tab_ordenes_produccion()
        self.configurar_tab_ordenes_materiales()
        self.configurar_tab_ordenes_compra()
        self.configurar_tab_ventas()
    
    def configurar_tab_productos(self):
        """Configurar pestaña de productos"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.tab_productos)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botones de acción
        botones_config = [
            {
                "name": "agregar",
                "text": "Agregar Producto",
                "command": self.agregar_producto
            },
            {
                "name": "editar",
                "text": "Editar Producto",
                "command": self.editar_producto,
                "state": "disabled"
            },
            {
                "name": "eliminar",
                "text": "Eliminar Producto",
                "command": self.eliminar_producto,
                "state": "disabled",
                "fg_color": "red",
                "hover_color": "darkred"
            },
            {
                "name": "agregar_materiales",
                "text": "Añadir Materiales Necesarios",
                "command": self.agregar_materiales_producto,
                "state": "disabled"
            }
        ]
        
        self.botones_productos_frame, self.botones_productos = self.crear_botones_accion(main_frame, botones_config)
        
        # Tabla
        columnas = ("ID", "Nombre", "Descripción", "Precio Unitario", "Stock", "Lista de Materiales")
        self.productos_table_frame, self.productos_table = self.crear_tabla_frame(main_frame, columnas)
        
        # Configurar columnas específicas
        self.productos_table.column("ID", anchor="center", width=60)
        self.productos_table.column("Nombre", anchor="w", width=150)
        self.productos_table.column("Descripción", anchor="w", width=200)
        self.productos_table.column("Precio Unitario", anchor="e", width=120)
        self.productos_table.column("Stock", anchor="center", width=80)
        self.productos_table.column("Lista de Materiales", anchor="w", width=250)
        
        for col in columnas:
            self.productos_table.heading(col, text=col)
        
        # Evento de selección
        self.productos_table.bind("<<TreeviewSelect>>", self.on_producto_select)
        
        # Cargar datos
        self.cargar_productos()
    
    def configurar_tab_materias(self):
        """Configurar pestaña de materias primas"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.tab_materias)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botones de acción
        botones_config = [
            {
                "name": "agregar",
                "text": "Agregar Materia Prima",
                "command": self.agregar_materia
            },
            {
                "name": "editar",
                "text": "Editar Materia Prima",
                "command": self.editar_materia,
                "state": "disabled"
            },
            {
                "name": "eliminar",
                "text": "Eliminar Materia Prima",
                "command": self.eliminar_materia,
                "state": "disabled",
                "fg_color": "red",
                "hover_color": "darkred"
            }
        ]
        
        self.botones_materias_frame, self.botones_materias = self.crear_botones_accion(main_frame, botones_config)
        
        # Tabla
        columnas = ("ID", "Nombre", "Descripción", "Proveedor", "Stock")
        self.materias_table_frame, self.materias_table = self.crear_tabla_frame(main_frame, columnas)
        
        # Configurar columnas específicas
        self.materias_table.column("ID", anchor="center", width=60)
        self.materias_table.column("Nombre", anchor="w", width=150)
        self.materias_table.column("Descripción", anchor="w", width=250)
        self.materias_table.column("Proveedor", anchor="w", width=150)
        self.materias_table.column("Stock", anchor="center", width=100)
        
        for col in columnas:
            self.materias_table.heading(col, text=col)
        
        # Evento de selección
        self.materias_table.bind("<<TreeviewSelect>>", self.on_materia_select)
        
        # Cargar datos
        self.cargar_materias()
    
    def configurar_tab_ordenes_produccion(self):
        """Configurar pestaña de órdenes de producción"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.tab_ordenes_produccion)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame para filtros y botones
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        # Filtro por estado
        filter_label = ctk.CTkLabel(controls_frame, text="Filtrar por estado:")
        filter_label.pack(side="left", padx=(10, 5), pady=10)
        
        self.filtro_estado_produccion = ctk.CTkComboBox(
            controls_frame,
            values=["Todos", "En espera", "En proceso", "Finalizado", "Cancelado"],
            command=self.filtrar_ordenes_produccion,
            width=150
        )
        self.filtro_estado_produccion.set("Todos")
        self.filtro_estado_produccion.pack(side="left", padx=5, pady=10)
        
        # Botones de acción
        botones_config = [
            {
                "name": "agregar",
                "text": "Nueva Orden de Producción",
                "command": self.agregar_orden_produccion
            },
            {
                "name": "editar",
                "text": "Editar Estado",
                "command": self.editar_orden_produccion,
                "state": "disabled"
            }
        ]
        
        # Crear botones en el frame de controles
        button_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=10, pady=5)
        
        self.botones_ordenes_prod = {}
        for config in botones_config:
            button = ctk.CTkButton(
                button_frame,
                text=config["text"],
                command=config["command"],
                state=config.get("state", "normal"),
                fg_color=config.get("fg_color", None),
                hover_color=config.get("hover_color", None)
            )
            button.pack(side="left", padx=5)
            self.botones_ordenes_prod[config["name"]] = button
        
        # Tabla
        columnas = ("ID", "Nombre del Producto", "Cantidad", "Fecha de Inicio", "Fecha de Fin Estimada", "Estado")
        self.ordenes_prod_table_frame, self.ordenes_prod_table = self.crear_tabla_frame(main_frame, columnas)
        
        # Configurar columnas específicas
        self.ordenes_prod_table.column("ID", anchor="center", width=60)
        self.ordenes_prod_table.column("Nombre del Producto", anchor="w", width=200)
        self.ordenes_prod_table.column("Cantidad", anchor="center", width=100)
        self.ordenes_prod_table.column("Fecha de Inicio", anchor="center", width=120)
        self.ordenes_prod_table.column("Fecha de Fin Estimada", anchor="center", width=120)
        self.ordenes_prod_table.column("Estado", anchor="center", width=120)
        
        for col in columnas:
            self.ordenes_prod_table.heading(col, text=col)
        
        # Evento de selección
        self.ordenes_prod_table.bind("<<TreeviewSelect>>", self.on_orden_produccion_select)
        
        # Cargar datos
        self.cargar_ordenes_produccion()
    
    def configurar_tab_ordenes_materiales(self):
        """Configurar pestaña de órdenes de materiales"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.tab_ordenes_materiales)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botones de acción (solo editar)
        botones_config = [
            {
                "name": "editar",
                "text": "Editar Estado",
                "command": self.editar_orden_materia,
                "state": "disabled"
            }
        ]
        
        self.botones_ordenes_mat_frame, self.botones_ordenes_mat = self.crear_botones_accion(main_frame, botones_config)
        
        # Tabla
        columnas = ("ID", "Materia", "Cantidad", "Fecha", "Estado")
        self.ordenes_mat_table_frame, self.ordenes_mat_table = self.crear_tabla_frame(main_frame, columnas)
        
        # Configurar columnas específicas
        self.ordenes_mat_table.column("ID", anchor="center", width=80)
        self.ordenes_mat_table.column("Materia", anchor="w", width=200)
        self.ordenes_mat_table.column("Cantidad", anchor="center", width=120)
        self.ordenes_mat_table.column("Fecha", anchor="center", width=150)
        self.ordenes_mat_table.column("Estado", anchor="center", width=150)
        
        for col in columnas:
            self.ordenes_mat_table.heading(col, text=col)
        
        # Evento de selección
        self.ordenes_mat_table.bind("<<TreeviewSelect>>", self.on_orden_materia_select)
        
        # Cargar datos
        self.cargar_ordenes_materiales()
    
    def configurar_tab_ordenes_compra(self):
        """Configurar pestaña de órdenes de compra"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.tab_ordenes_compra)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Información de la pestaña
        info_frame = ctk.CTkFrame(main_frame, fg_color="#ffffff")
        info_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="🛒 Órdenes de Compra - Reposición de Materias Primas",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        info_label.pack(pady=10)
        
        info_desc = ctk.CTkLabel(
            info_frame,
            text="Gestiona las órdenes de compra para reponer el stock de materias primas.",
            font=ctk.CTkFont(size=12)
        )
        info_desc.pack(pady=(0, 10))
        
        # Botones de acción
        botones_config = [
            {
                "name": "agregar",
                "text": "Nueva Orden de Compra",
                "command": self.agregar_orden_compra
            },
            {
                "name": "editar",
                "text": "Editar Estado",
                "command": self.editar_orden_compra,
                "state": "disabled"
            },
            {
                "name": "refrescar",
                "text": "Refrescar",
                "command": self.cargar_ordenes_compra
            }
        ]
        
        self.botones_ordenes_compra_frame, self.botones_ordenes_compra = self.crear_botones_accion(main_frame, botones_config)
        
        # Tabla
        columnas = ("ID", "Materia", "Proveedor", "Cantidad", "Fecha", "Estado")
        self.ordenes_compra_table_frame, self.ordenes_compra_table = self.crear_tabla_frame(main_frame, columnas)
        
        # Configurar columnas específicas
        self.ordenes_compra_table.column("ID", anchor="center", width=60)
        self.ordenes_compra_table.column("Materia", anchor="w", width=200)
        self.ordenes_compra_table.column("Proveedor", anchor="w", width=180)
        self.ordenes_compra_table.column("Cantidad", anchor="center", width=100)
        self.ordenes_compra_table.column("Fecha", anchor="center", width=120)
        self.ordenes_compra_table.column("Estado", anchor="center", width=120)
        
        for col in columnas:
            self.ordenes_compra_table.heading(col, text=col)
        
        # Evento de selección
        self.ordenes_compra_table.bind("<<TreeviewSelect>>", self.on_orden_compra_select)
        
        # Cargar datos
        self.cargar_ordenes_compra()
    
    def configurar_tab_ventas(self):
        """Configurar pestaña de ventas"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.tab_ventas)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Información de la pestaña
        info_frame = ctk.CTkFrame(main_frame, fg_color="#ffffff")
        info_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="📦 Control de Ventas - Gestión de Stock",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        info_label.pack(pady=10)
        
        info_desc = ctk.CTkLabel(
            info_frame,
            text="Aquí puedes ver las ventas pendientes y aprobar/rechazar para gestionar el stock de productos.",
            font=ctk.CTkFont(size=12)
        )
        info_desc.pack(pady=(0, 10))
        
        # Botones de acción (solo editar estado)
        botones_config = [
            {
                "name": "editar",
                "text": "Cambiar Estado",
                "command": self.editar_estado_venta,
                "state": "disabled"
            },
            {
                "name": "refrescar",
                "text": "Refrescar",
                "command": self.cargar_ventas
            }
        ]
        
        self.botones_ventas_frame, self.botones_ventas = self.crear_botones_accion(main_frame, botones_config)
        
        # Tabla
        columnas = ("ID", "Cliente", "Producto", "Cantidad", "Total", "Estado")
        self.ventas_table_frame, self.ventas_table = self.crear_tabla_frame(main_frame, columnas)
        
        # Configurar columnas específicas
        self.ventas_table.column("ID", anchor="center", width=60)
        self.ventas_table.column("Cliente", anchor="w", width=150)
        self.ventas_table.column("Producto", anchor="w", width=200)
        self.ventas_table.column("Cantidad", anchor="center", width=100)
        self.ventas_table.column("Total", anchor="e", width=120)
        self.ventas_table.column("Estado", anchor="center", width=120)
        
        for col in columnas:
            self.ventas_table.heading(col, text=col)
        
        # Evento de selección
        self.ventas_table.bind("<<TreeviewSelect>>", self.on_venta_select)
        
        # Cargar datos
        self.cargar_ventas()
    
    def cargar_productos(self):
        """Cargar productos en la tabla"""
        # Limpiar tabla
        for row in self.productos_table.get_children():
            self.productos_table.delete(row)
        
        # Obtener productos
        productos = obtener_productos()
        
        # Insertar en la tabla
        for producto in productos:
            # Obtener lista de materiales
            materias_producto = obtener_materias_de_producto(producto[0])
            lista_materiales = f"{len(materias_producto)} materiales" if materias_producto else "Sin materiales"
            
            # Formatear precio
            producto_formateado = list(producto)
            producto_formateado[3] = f"${producto[3]}"
            producto_formateado.append(lista_materiales)
            
            self.productos_table.insert("", "end", values=producto_formateado)
    
    def cargar_materias(self):
        """Cargar materias primas en la tabla"""
        # Limpiar tabla
        for row in self.materias_table.get_children():
            self.materias_table.delete(row)
        
        # Obtener materias y proveedores
        materias = obtener_materias()
        proveedores = {p[0]: p[1] for p in obtener_proveedores()}
        
        # Insertar en la tabla
        for materia in materias:
            materia_formateada = list(materia)
            # Reemplazar ID del proveedor por nombre
            proveedor_nombre = proveedores.get(materia[3], "Proveedor desconocido")
            materia_formateada[3] = proveedor_nombre
            
            self.materias_table.insert("", "end", values=materia_formateada)
    
    def cargar_ordenes_produccion(self, filtro_estado=None):
        """Cargar órdenes de producción en la tabla"""
        # Limpiar tabla
        for row in self.ordenes_prod_table.get_children():
            self.ordenes_prod_table.delete(row)
        
        # Obtener órdenes y productos
        ordenes = obtener_ordenes_produccion(filtro_estado)
        productos = {p[0]: p[1] for p in obtener_productos()}
        
        # Insertar en la tabla
        for orden in ordenes:
            orden_formateada = list(orden)
            # Reemplazar ID del producto por nombre
            producto_nombre = productos.get(orden[1], "Producto desconocido")
            orden_formateada[1] = producto_nombre
            
            self.ordenes_prod_table.insert("", "end", values=orden_formateada)
    
    def cargar_ordenes_materiales(self):
        """Cargar órdenes de materiales en la tabla"""
        # Limpiar tabla
        for row in self.ordenes_mat_table.get_children():
            self.ordenes_mat_table.delete(row)
        
        # Obtener órdenes y materias
        ordenes = obtener_ordenes_materia()
        materias = {m[0]: m[1] for m in obtener_materias()}
        
        # Insertar en la tabla
        for orden in ordenes:
            orden_formateada = list(orden)
            # Reemplazar ID de la materia por nombre
            materia_nombre = materias.get(orden[1], "Materia desconocida")
            orden_formateada[1] = materia_nombre
            
            self.ordenes_mat_table.insert("", "end", values=orden_formateada)
    
    def cargar_ordenes_compra(self):
        """Cargar órdenes de compra en la tabla"""
        # Limpiar tabla
        for row in self.ordenes_compra_table.get_children():
            self.ordenes_compra_table.delete(row)
        
        # Obtener órdenes, materias y proveedores
        ordenes = obtener_ordenes_compra()
        materias = {m[0]: m[1] for m in obtener_materias()}
        proveedores = {p[0]: p[1] for p in obtener_proveedores()}
        
        # Insertar en la tabla
        for orden in ordenes:
            # Estructura esperada: (ID, materia_id, proveedor_id, cantidad, precio_unitario, total, fecha, estado)
            # Mostrar: (ID, Materia, Proveedor, Cantidad, Fecha, Estado)
            orden_formateada = [
                orden[0],  # ID
                materias.get(orden[1], "Materia desconocida"),  # Materia nombre
                proveedores.get(orden[2], "Proveedor desconocido"),  # Proveedor nombre
                orden[3],  # Cantidad
                orden[6],  # Fecha (saltamos precio_unitario y total)
                orden[7]   # Estado
            ]
            
            self.ordenes_compra_table.insert("", "end", values=orden_formateada)
    
    def cargar_ventas(self):
        """Cargar ventas en la tabla"""
        # Limpiar tabla
        for row in self.ventas_table.get_children():
            self.ventas_table.delete(row)
        
        # Obtener ventas
        ventas = obtener_ventas()
        
        # Insertar en la tabla
        for venta in ventas:
            # Formato de venta: (ID Venta, Cliente, Total, Producto, Cantidad, Precio Unitario, Estado)
            # Reorganizar para la tabla: (ID, Cliente, Producto, Cantidad, Total, Estado)
            venta_formateada = [
                venta[0],  # ID
                venta[1],  # Cliente
                venta[3],  # Producto
                venta[4],  # Cantidad
                f"${venta[2]}",  # Total formateado
                venta[6]   # Estado
            ]
            
            self.ventas_table.insert("", "end", values=venta_formateada)
    
    def filtrar_ordenes_produccion(self, estado_seleccionado):
        """Filtrar órdenes de producción por estado"""
        filtro = None if estado_seleccionado == "Todos" else estado_seleccionado
        self.cargar_ordenes_produccion(filtro)
    
    def on_producto_select(self, event):
        """Manejar selección de producto"""
        selected = self.productos_table.selection()
        if selected:
            self.producto_seleccionado = self.productos_table.item(selected[0], "values")
            self.botones_productos["editar"].configure(state="normal")
            self.botones_productos["eliminar"].configure(state="normal")
            self.botones_productos["agregar_materiales"].configure(state="normal")
        else:
            self.producto_seleccionado = None
            self.botones_productos["editar"].configure(state="disabled")
            self.botones_productos["eliminar"].configure(state="disabled")
            self.botones_productos["agregar_materiales"].configure(state="disabled")
    
    def on_materia_select(self, event):
        """Manejar selección de materia prima"""
        selected = self.materias_table.selection()
        if selected:
            self.materia_seleccionada = self.materias_table.item(selected[0], "values")
            self.botones_materias["editar"].configure(state="normal")
            self.botones_materias["eliminar"].configure(state="normal")
        else:
            self.materia_seleccionada = None
            self.botones_materias["editar"].configure(state="disabled")
            self.botones_materias["eliminar"].configure(state="disabled")
    
    def on_orden_produccion_select(self, event):
        """Manejar selección de orden de producción"""
        selected = self.ordenes_prod_table.selection()
        if selected:
            self.orden_produccion_seleccionada = self.ordenes_prod_table.item(selected[0], "values")
            # Solo habilitar editar si el estado es "En espera"
            if self.orden_produccion_seleccionada[5] == "En espera":
                self.botones_ordenes_prod["editar"].configure(state="normal")
            else:
                self.botones_ordenes_prod["editar"].configure(state="disabled")
        else:
            self.orden_produccion_seleccionada = None
            self.botones_ordenes_prod["editar"].configure(state="disabled")
    
    def on_orden_materia_select(self, event):
        """Manejar selección de orden de materiales"""
        selected = self.ordenes_mat_table.selection()
        if selected:
            self.orden_materia_seleccionada = self.ordenes_mat_table.item(selected[0], "values")
            # Solo habilitar editar si el estado es "En espera"
            if self.orden_materia_seleccionada[4] == "En espera":
                self.botones_ordenes_mat["editar"].configure(state="normal")
            else:
                self.botones_ordenes_mat["editar"].configure(state="disabled")
        else:
            self.orden_materia_seleccionada = None
            self.botones_ordenes_mat["editar"].configure(state="disabled")
    
    def on_orden_compra_select(self, event):
        """Manejar selección de orden de compra"""
        selected = self.ordenes_compra_table.selection()
        if selected:
            self.orden_compra_seleccionada = self.ordenes_compra_table.item(selected[0], "values")
            # Solo habilitar editar si el estado es "En espera"
            if self.orden_compra_seleccionada[5] == "En espera":
                self.botones_ordenes_compra["editar"].configure(state="normal")
            else:
                self.botones_ordenes_compra["editar"].configure(state="disabled")
        else:
            self.orden_compra_seleccionada = None
            self.botones_ordenes_compra["editar"].configure(state="disabled")
    
    def on_venta_select(self, event):
        """Manejar selección de venta"""
        selected = self.ventas_table.selection()
        if selected:
            self.venta_seleccionada = self.ventas_table.item(selected[0], "values")
            # Solo habilitar editar si el estado es "En espera"
            if self.venta_seleccionada[5] == "En espera":
                self.botones_ventas["editar"].configure(state="normal")
            else:
                self.botones_ventas["editar"].configure(state="disabled")
        else:
            self.venta_seleccionada = None
            self.botones_ventas["editar"].configure(state="disabled")
    
    # Métodos para productos
    def agregar_producto(self):
        """Abrir ventana para agregar producto"""
        from components.dialogs_inventario import ProductoDialog
        
        dialog = ProductoDialog(self.parent, "agregar")
        if dialog.resultado:
            if insertar_producto(
                dialog.resultado["nombre"],
                dialog.resultado["descripcion"],
                dialog.resultado["precio_unitario"],
                dialog.resultado["stock"]
            ):
                self.cargar_productos()
                messagebox.showinfo("Éxito", f"{dialog.resultado['nombre']} ha sido agregado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo agregar el producto.")
    
    def editar_producto(self):
        """Abrir ventana para editar producto"""
        if not self.producto_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un producto primero.")
            return
        
        from components.dialogs_inventario import ProductoDialog
        
        dialog = ProductoDialog(self.parent, "editar", self.producto_seleccionado)
        if dialog.resultado:
            if actualizar_producto(
                self.producto_seleccionado[0],  # ID del producto
                dialog.resultado["nombre"],
                dialog.resultado["descripcion"],
                dialog.resultado["precio_unitario"],
                dialog.resultado["stock"]
            ):
                self.cargar_productos()
                messagebox.showinfo("Éxito", f"{dialog.resultado['nombre']} ha sido actualizado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el producto.")
    
    def eliminar_producto(self):
        """Eliminar producto seleccionado"""
        if not self.producto_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un producto primero.")
            return
        
        if messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar el producto '{self.producto_seleccionado[1]}'?\n\nEsta acción no se puede deshacer."
        ):
            if eliminar_producto(self.producto_seleccionado[0]):
                self.cargar_productos()
                messagebox.showinfo("Éxito", f"{self.producto_seleccionado[1]} ha sido eliminado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto.")
    
    def agregar_materiales_producto(self):
        """Abrir ventana para agregar materiales al producto"""
        if not self.producto_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un producto primero.")
            return
        
        from components.dialogs_inventario import AgregarMaterialDialog
        
        dialog = AgregarMaterialDialog(self.parent, self.producto_seleccionado)
        if dialog.resultado:
            if agregar_materia_a_producto(
                dialog.resultado["producto_id"],
                dialog.resultado["materia_id"],
                dialog.resultado["cantidad"]
            ):
                self.cargar_productos()  # Recargar para actualizar lista de materiales
                messagebox.showinfo("Éxito", "Material agregado al producto correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo agregar el material al producto.")
    
    # Métodos para materias primas
    def agregar_materia(self):
        """Abrir ventana para agregar materia prima"""
        from components.dialogs_inventario import MateriaPrimaDialog
        
        dialog = MateriaPrimaDialog(self.parent, "agregar")
        if dialog.resultado:
            if insertar_materia(
                dialog.resultado["nombre"],
                dialog.resultado["descripcion"],
                dialog.resultado["proveedor_id"],
                dialog.resultado["stock"]
            ):
                self.cargar_materias()
                messagebox.showinfo("Éxito", f"{dialog.resultado['nombre']} ha sido agregado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo agregar la materia prima.")
    
    def editar_materia(self):
        """Abrir ventana para editar materia prima"""
        if not self.materia_seleccionada:
            messagebox.showwarning("Advertencia", "Selecciona una materia prima primero.")
            return

        from components.dialogs_inventario import MateriaPrimaDialog

        dialog = MateriaPrimaDialog(self.parent, "editar", self.materia_seleccionada)
        if dialog.resultado:
            if actualizar_materia(
                self.materia_seleccionada[0],
                dialog.resultado["nombre"],
                dialog.resultado["descripcion"],
                dialog.resultado["proveedor_id"],
                dialog.resultado["stock"]
            ):
                self.cargar_materias()
                messagebox.showinfo("Éxito", "Materia prima actualizada correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar la materia prima.")

    
    def eliminar_materia(self):
        """Eliminar materia prima seleccionada"""
        if not self.materia_seleccionada:
            messagebox.showwarning("Advertencia", "Selecciona una materia prima primero.")
            return
        
        if messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar la materia prima '{self.materia_seleccionada[1]}'?\n\nEsta acción no se puede deshacer."
        ):
            if eliminar_materia(self.materia_seleccionada[0]):
                self.cargar_materias()
                messagebox.showinfo("Éxito", f"{self.materia_seleccionada[1]} ha sido eliminado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo eliminar la materia prima.")
    
    # Métodos para órdenes de producción
    def agregar_orden_produccion(self):
        """Abrir ventana para agregar orden de producción"""
        from components.dialogs_inventario import OrdenProduccionDialog
        
        dialog = OrdenProduccionDialog(self.parent)
        if dialog.resultado:
            if insertar_orden_produccion(
                dialog.resultado["producto_id"],
                dialog.resultado["cantidad"],
                dialog.resultado["fecha_inicio"],
                dialog.resultado["fecha_fin"],
                dialog.resultado["estado"]
            ):
                self.cargar_ordenes_produccion()
                messagebox.showinfo("Éxito", "Orden de producción creada correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo crear la orden de producción.")
    
    def editar_orden_produccion(self):
        """Editar estado de orden de producción"""
        if not self.orden_produccion_seleccionada:
            messagebox.showwarning("Advertencia", "Selecciona una orden de producción primero.")
            return
        
        if self.orden_produccion_seleccionada[5] != "En espera":
            messagebox.showwarning("No editable", "Solo se pueden editar órdenes en estado 'En espera'.")
            return
        
        from components.dialogs_inventario import EditarEstadoOrdenDialog
        
        dialog = EditarEstadoOrdenDialog(
            self.parent, 
            "produccion", 
            self.orden_produccion_seleccionada
        )
        if dialog.resultado:
            if actualizar_estado_orden_produccion(
                self.orden_produccion_seleccionada[0],
                dialog.resultado["estado"]
            ):
                self.cargar_ordenes_produccion()
                messagebox.showinfo("Éxito", "Estado de la orden actualizado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el estado de la orden.")
    
    # Métodos para órdenes de materiales
    def editar_orden_materia(self):
        """Editar estado de orden de materiales"""
        if not self.orden_materia_seleccionada:
            messagebox.showwarning("Advertencia", "Selecciona una orden de materiales primero.")
            return
        
        if self.orden_materia_seleccionada[4] != "En espera":
            messagebox.showwarning("No editable", "Solo se pueden editar órdenes en estado 'En espera'.")
            return
        
        from components.dialogs_inventario import EditarEstadoOrdenDialog
        
        dialog = EditarEstadoOrdenDialog(
            self.parent, 
            "materiales", 
            self.orden_materia_seleccionada
        )
        if dialog.resultado:
            if actualizar_estado_orden_materia(
                self.orden_materia_seleccionada[0],
                dialog.resultado["estado"],
                self.orden_materia_seleccionada[2] if dialog.resultado["estado"] == "Finalizado" else None  # cantidad para descontar
            ):
                self.cargar_ordenes_materiales()
                messagebox.showinfo("Éxito", "Estado de la orden actualizado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el estado de la orden.")
    
    # Métodos para órdenes de compra
    def agregar_orden_compra(self):
        """Abrir ventana para agregar orden de compra"""
        from components.dialogs_inventario import OrdenCompraDialog
        
        dialog = OrdenCompraDialog(self.parent)
        if dialog.resultado:
            if insertar_orden_compra(
                dialog.resultado["materia_id"],
                dialog.resultado["proveedor_id"],
                dialog.resultado["cantidad"],
                dialog.resultado["precio_unitario"],
                dialog.resultado["total"],
                dialog.resultado["fecha"],
                dialog.resultado["estado"]
            ):
                self.cargar_ordenes_compra()
                messagebox.showinfo("Éxito", "Orden de compra creada correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo crear la orden de compra.")
    
    def editar_orden_compra(self):
        """Editar estado de orden de compra"""
        if not self.orden_compra_seleccionada:
            messagebox.showwarning("Advertencia", "Selecciona una orden de compra primero.")
            return
        
        if self.orden_compra_seleccionada[5] != "En espera":
            messagebox.showwarning("No editable", "Solo se pueden editar órdenes en estado 'En espera'.")
            return
        
        from components.dialogs_inventario import EditarEstadoOrdenCompraDialog
        
        dialog = EditarEstadoOrdenCompraDialog(self.parent, self.orden_compra_seleccionada)
        if dialog.resultado:
            if actualizar_estado_orden_compra(
                self.orden_compra_seleccionada[0],
                dialog.resultado["estado"]
            ):
                self.cargar_ordenes_compra()
                messagebox.showinfo("Éxito", "Estado de la orden actualizado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el estado de la orden.")
    
    # Métodos para ventas
    def editar_estado_venta(self):
        """Editar estado de venta"""
        if not self.venta_seleccionada:
            messagebox.showwarning("Advertencia", "Selecciona una venta primero.")
            return
        
        if self.venta_seleccionada[5] != "En espera":
            messagebox.showwarning("No editable", "Solo se pueden editar ventas en estado 'En espera'.")
            return
        
        from components.dialogs_inventario import EditarEstadoVentaDialog
        
        dialog = EditarEstadoVentaDialog(self.parent, self.venta_seleccionada)
        if dialog.resultado:
            # Verificar stock si el estado es "Finalizado"
            if dialog.resultado["estado"] == "Finalizado":
                # Obtener información del producto para verificar stock
                producto_nombre = self.venta_seleccionada[2]
                cantidad_solicitada = int(self.venta_seleccionada[3])
                
                # Buscar el producto por nombre para obtener su ID y stock actual
                productos = obtener_productos()
                producto_encontrado = None
                for producto in productos:
                    if producto[1] == producto_nombre:
                        producto_encontrado = producto
                        break
                
                if not producto_encontrado:
                    messagebox.showerror("Error", "No se pudo encontrar el producto.")
                    return
                
                stock_actual = int(producto_encontrado[4])
                
                # Verificar si hay suficiente stock
                if stock_actual < cantidad_solicitada:
                    messagebox.showwarning(
                        "Stock insuficiente",
                        f"No hay suficiente stock para completar la venta.\n\n"
                        f"Stock actual: {stock_actual}\n"
                        f"Cantidad solicitada: {cantidad_solicitada}\n"
                        f"Faltante: {cantidad_solicitada - stock_actual}"
                    )
                    return
            
            # Actualizar estado de la venta
            if actualizar_estado_venta(
                self.venta_seleccionada[0],  # ID de la venta
                dialog.resultado["estado"],
                self.venta_seleccionada[3] if dialog.resultado["estado"] == "Finalizado" else None  # cantidad para descontar
            ):
                self.cargar_ventas()
                self.cargar_productos()  # Recargar productos para actualizar stock
                messagebox.showinfo("Éxito", "Estado de la venta actualizado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el estado de la venta.")