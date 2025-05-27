"""
Diálogos específicos para el módulo de inventario
"""

import customtkinter as ctk
from tkinter import messagebox
from services.producto_service import obtener_productos_para_combobox
from services.materia_prima_service import obtener_materias_para_combobox
from services.proveedor_service import obtener_proveedores_para_combobox
from datetime import date

class BaseDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, size="400x300"):
        super().__init__(parent)
        
        self.resultado = None
        self.title(title)
        self.geometry(size)
        self.transient(parent)
        self.grab_set()
        
        # Centrar ventana
        self.centrar_ventana()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Esperar a que el diálogo se cierre
        self.wait_window()
    
    def centrar_ventana(self):
        """Centrar la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def crear_interfaz(self):
        """Método que debe ser implementado por las clases hijas"""
        raise NotImplementedError("Las clases hijas deben implementar crear_interfaz()")

class ProductoDialog(BaseDialog):
    def __init__(self, parent, modo="agregar", datos=None):
        self.modo = modo
        self.datos = datos
        
        title = f"{'Agregar' if modo == 'agregar' else 'Editar'} Producto"
        super().__init__(parent, title, "500x500")
    
    def crear_interfaz(self):
        """Crear interfaz del diálogo de producto"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text=f"{'Agregar Nuevo' if self.modo == 'agregar' else 'Editar'} Producto",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Formulario
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=30, pady=0)
        
        # Crear campos
        self.crear_campos(form_frame)
        
        # Botones
        self.crear_botones()
    
    def crear_campos(self, parent):
        """Crear campos del formulario"""
        # Nombre
        nombre_label = ctk.CTkLabel(parent, text="Nombre del Producto:")
        nombre_label.pack(anchor="w", pady=(0, 5))
        self.nombre_entry = ctk.CTkEntry(parent, placeholder_text="Nombre del producto", width=440)
        self.nombre_entry.pack(fill="x", pady=(0, 15))
        
        # Descripción
        descripcion_label = ctk.CTkLabel(parent, text="Descripción:")
        descripcion_label.pack(anchor="w", pady=(0, 5))
        self.descripcion_textbox = ctk.CTkTextbox(parent, height=80, width=440)
        self.descripcion_textbox.pack(fill="x", pady=(0, 15))
        
        # Precio unitario
        precio_label = ctk.CTkLabel(parent, text="Precio Unitario:")
        precio_label.pack(anchor="w", pady=(0, 5))
        self.precio_entry = ctk.CTkEntry(parent, placeholder_text="Precio unitario", width=440)
        self.precio_entry.pack(fill="x", pady=(0, 15))
        
        # Stock
        stock_label = ctk.CTkLabel(parent, text="Stock:")
        stock_label.pack(anchor="w", pady=(0, 5))
        self.stock_entry = ctk.CTkEntry(parent, placeholder_text="Cantidad en stock", width=440)
        self.stock_entry.pack(fill="x", pady=(0, 15))
        
        # Llenar campos si es edición
        if self.modo == "editar" and self.datos:
            self.nombre_entry.insert(0, self.datos[1])
            self.descripcion_textbox.insert("1.0", self.datos[2])
            # Limpiar formato de precio
            precio_limpio = self.datos[3].replace("$", "").replace(",", "")
            self.precio_entry.insert(0, precio_limpio)
            self.stock_entry.insert(0, str(self.datos[4]))
    
    def crear_botones(self):
        """Crear botones del diálogo"""
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=20)
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            command=self.cancelar
        )
        cancel_button.pack(side="left", padx=(0, 10))
        
        save_button = ctk.CTkButton(
            button_frame,
            text=f"{'Agregar' if self.modo == 'agregar' else 'Actualizar'} Producto",
            command=self.guardar
        )
        save_button.pack(side="right")
    
    def guardar(self):
        """Guardar datos del formulario"""
        # Validar campos
        if not all([self.nombre_entry.get(), self.descripcion_textbox.get("1.0", "end-1c"),
                   self.precio_entry.get(), self.stock_entry.get()]):
            messagebox.showwarning("Campos requeridos", "Todos los campos son obligatorios.")
            return
        
        try:
            precio_unitario = float(self.precio_entry.get())
            stock = int(self.stock_entry.get())
        except ValueError:
            messagebox.showwarning("Valores inválidos", "Precio y stock deben ser números válidos.")
            return
        
        # Guardar resultado
        self.resultado = {
            "nombre": self.nombre_entry.get(),
            "descripcion": self.descripcion_textbox.get("1.0", "end-1c"),
            "precio_unitario": precio_unitario,
            "stock": stock
        }
        
        self.destroy()
    
    def cancelar(self):
        """Cancelar diálogo"""
        self.resultado = None
        self.destroy()

class MateriaPrimaDialog(BaseDialog):
    def __init__(self, parent, modo="agregar", datos=None):
        self.modo = modo
        self.datos = datos
        
        title = f"{'Agregar' if modo == 'agregar' else 'Editar'} Materia Prima"
        super().__init__(parent, title, "500x500")
    
    def crear_interfaz(self):
        """Crear interfaz del diálogo de materia prima"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text=f"{'Agregar Nueva' if self.modo == 'agregar' else 'Editar'} Materia Prima",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Formulario
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=30, pady=0)
        
        # Crear campos
        self.crear_campos(form_frame)
        
        # Botones
        self.crear_botones()
    
    def crear_campos(self, parent):
        """Crear campos del formulario"""
        # Nombre
        nombre_label = ctk.CTkLabel(parent, text="Nombre de la Materia Prima:")
        nombre_label.pack(anchor="w", pady=(0, 5))
        self.nombre_entry = ctk.CTkEntry(parent, placeholder_text="Nombre de la materia prima", width=440)
        self.nombre_entry.pack(fill="x", pady=(0, 15))
        
        # Descripción
        descripcion_label = ctk.CTkLabel(parent, text="Descripción:")
        descripcion_label.pack(anchor="w", pady=(0, 5))
        self.descripcion_textbox = ctk.CTkTextbox(parent, height=80, width=440)
        self.descripcion_textbox.pack(fill="x", pady=(0, 15))
        
        # Proveedor
        proveedor_label = ctk.CTkLabel(parent, text="Proveedor:")
        proveedor_label.pack(anchor="w", pady=(0, 5))
        
        proveedores_opciones = obtener_proveedores_para_combobox()
        self.proveedor_combobox = ctk.CTkComboBox(
            parent,
            values=proveedores_opciones,
            width=440
        )
        self.proveedor_combobox.pack(fill="x", pady=(0, 15))
        
        # Stock
        stock_label = ctk.CTkLabel(parent, text="Stock:")
        stock_label.pack(anchor="w", pady=(0, 5))
        self.stock_entry = ctk.CTkEntry(parent, placeholder_text="Cantidad en stock", width=440)
        self.stock_entry.pack(fill="x", pady=(0, 15))
        
        # Llenar campos si es edición
        if self.modo == "editar" and self.datos:
            self.nombre_entry.insert(0, self.datos[1])
            self.descripcion_textbox.insert("1.0", self.datos[2])
            
            # Buscar proveedor correspondiente
            proveedor_actual = self.datos[3]
            for opcion in proveedores_opciones:
                if proveedor_actual in opcion:
                    self.proveedor_combobox.set(opcion)
                    break
            
            self.stock_entry.insert(0, str(self.datos[4]))
    
    def crear_botones(self):
        """Crear botones del diálogo"""
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=20)
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            command=self.cancelar
        )
        cancel_button.pack(side="left", padx=(0, 10))
        
        save_button = ctk.CTkButton(
            button_frame,
            text=f"{'Agregar' if self.modo == 'agregar' else 'Actualizar'} Materia Prima",
            command=self.guardar
        )
        save_button.pack(side="right")
    
    def guardar(self):
        """Guardar datos del formulario"""
        # Validar campos
        if not all([self.nombre_entry.get(), self.descripcion_textbox.get("1.0", "end-1c"),
                   self.proveedor_combobox.get(), self.stock_entry.get()]):
            messagebox.showwarning("Campos requeridos", "Todos los campos son obligatorios.")
            return
        
        try:
            stock = int(self.stock_entry.get())
        except ValueError:
            messagebox.showwarning("Stock inválido", "El stock debe ser un número válido.")
            return
        
        # Extraer ID del proveedor
        proveedor_seleccionado = self.proveedor_combobox.get()
        proveedor_id = int(proveedor_seleccionado.split(" - ")[0])
        
        # Guardar resultado
        self.resultado = {
            "nombre": self.nombre_entry.get(),
            "descripcion": self.descripcion_textbox.get("1.0", "end-1c"),
            "proveedor_id": proveedor_id,
            "stock": stock
        }
        
        self.destroy()
    
    def cancelar(self):
        """Cancelar diálogo"""
        self.resultado = None
        self.destroy()

class AgregarMaterialDialog(BaseDialog):
    def __init__(self, parent, producto_datos):
        self.producto_datos = producto_datos
        super().__init__(parent, "Agregar Material al Producto", "500x400")
    
    def crear_interfaz(self):
        """Crear interfaz del diálogo de agregar material"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="Agregar Material al Producto",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Información del producto
        producto_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        producto_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        producto_title = ctk.CTkLabel(
            producto_frame,
            text="Información del Producto",
            font=ctk.CTkFont(weight="bold")
        )
        producto_title.pack(pady=(10, 5))
        
        producto_info = ctk.CTkLabel(
            producto_frame,
            text=f"ID: {self.producto_datos[0]} | Nombre: {self.producto_datos[1]}"
        )
        producto_info.pack(pady=(0, 10))
        
        # Formulario
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=30, pady=0)
        
        # Crear campos
        self.crear_campos(form_frame)
        
        # Botones
        self.crear_botones()
    
    def crear_campos(self, parent):
        """Crear campos del formulario"""
        # Materia prima
        materia_label = ctk.CTkLabel(parent, text="Materia Prima:")
        materia_label.pack(anchor="w", pady=(0, 5))
        
        materias_opciones = obtener_materias_para_combobox()
        self.materia_combobox = ctk.CTkComboBox(
            parent,
            values=materias_opciones,
            width=440
        )
        self.materia_combobox.pack(fill="x", pady=(0, 15))
        
        # Cantidad necesaria
        cantidad_label = ctk.CTkLabel(parent, text="Cantidad Necesaria:")
        cantidad_label.pack(anchor="w", pady=(0, 5))
        self.cantidad_entry = ctk.CTkEntry(parent, placeholder_text="Cantidad necesaria", width=440)
        self.cantidad_entry.pack(fill="x", pady=(0, 15))
    
    def crear_botones(self):
        """Crear botones del diálogo"""
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=20)
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            command=self.cancelar
        )
        cancel_button.pack(side="left", padx=(0, 10))
        
        add_button = ctk.CTkButton(
            button_frame,
            text="Agregar Material",
            command=self.guardar
        )
        add_button.pack(side="right")
    
    def guardar(self):
        """Guardar datos del formulario"""
        # Validar campos
        if not self.materia_combobox.get() or not self.cantidad_entry.get():
            messagebox.showwarning("Campos requeridos", "Todos los campos son obligatorios.")
            return
        
        try:
            cantidad = int(self.cantidad_entry.get())
        except ValueError:
            messagebox.showwarning("Cantidad inválida", "La cantidad debe ser un número válido.")
            return
        
        # Extraer ID de la materia prima
        materia_seleccionada = self.materia_combobox.get()
        materia_id = int(materia_seleccionada.split(" - ")[0])
        
        # Guardar resultado
        self.resultado = {
            "producto_id": self.producto_datos[0],
            "materia_id": materia_id,
            "cantidad": cantidad
        }
        
        self.destroy()
    
    def cancelar(self):
        """Cancelar diálogo"""
        self.resultado = None
        self.destroy()

class OrdenProduccionDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent, "Nueva Orden de Producción", "500x550")
    
    def crear_interfaz(self):
        """Crear interfaz del diálogo de orden de producción"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="Nueva Orden de Producción",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Formulario
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=30, pady=0)
        
        # Crear campos
        self.crear_campos(form_frame)
        
        # Botones
        self.crear_botones()
    
    def crear_campos(self, parent):
        """Crear campos del formulario"""
        # Producto
        producto_label = ctk.CTkLabel(parent, text="Producto:")
        producto_label.pack(anchor="w", pady=(0, 5))
        
        productos_opciones = obtener_productos_para_combobox()
        self.producto_combobox = ctk.CTkComboBox(
            parent,
            values=productos_opciones,
            width=440
        )
        self.producto_combobox.pack(fill="x", pady=(0, 15))
        
        # Cantidad
        cantidad_label = ctk.CTkLabel(parent, text="Cantidad:")
        cantidad_label.pack(anchor="w", pady=(0, 5))
        self.cantidad_entry = ctk.CTkEntry(parent, placeholder_text="Cantidad a producir", width=440)
        self.cantidad_entry.pack(fill="x", pady=(0, 15))
        
        # Fecha de inicio (automática)
        fecha_inicio_label = ctk.CTkLabel(parent, text="Fecha de Inicio:")
        fecha_inicio_label.pack(anchor="w", pady=(0, 5))
        self.fecha_inicio_entry = ctk.CTkEntry(parent, width=440)
        self.fecha_inicio_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.fecha_inicio_entry.configure(state="disabled")
        self.fecha_inicio_entry.pack(fill="x", pady=(0, 15))
        
        # Fecha fin estimada
        fecha_fin_label = ctk.CTkLabel(parent, text="Fecha Fin Estimada:")
        fecha_fin_label.pack(anchor="w", pady=(0, 5))
        self.fecha_fin_entry = ctk.CTkEntry(parent, placeholder_text="YYYY-MM-DD", width=440)
        self.fecha_fin_entry.pack(fill="x", pady=(0, 15))
        
        # Estado (automático)
        estado_label = ctk.CTkLabel(parent, text="Estado:")
        estado_label.pack(anchor="w", pady=(0, 5))
        self.estado_entry = ctk.CTkEntry(parent, width=440)
        self.estado_entry.insert(0, "En espera")
        self.estado_entry.configure(state="disabled")
        self.estado_entry.pack(fill="x", pady=(0, 15))
    
    def crear_botones(self):
        """Crear botones del diálogo"""
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=20)
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            command=self.cancelar
        )
        cancel_button.pack(side="left", padx=(0, 10))
        
        create_button = ctk.CTkButton(
            button_frame,
            text="Crear Orden",
            command=self.guardar
        )
        create_button.pack(side="right")
    
    def guardar(self):
        """Guardar datos del formulario"""
        # Validar campos
        if not self.producto_combobox.get() or not self.cantidad_entry.get() or not self.fecha_fin_entry.get():
            messagebox.showwarning("Campos requeridos", "Producto, cantidad y fecha fin son obligatorios.")
            return
        
        try:
            cantidad = int(self.cantidad_entry.get())
        except ValueError:
            messagebox.showwarning("Cantidad inválida", "La cantidad debe ser un número válido.")
            return
        
        # Extraer ID del producto
        producto_seleccionado = self.producto_combobox.get()
        producto_id = int(producto_seleccionado.split(" - ")[0])
        
        # Guardar resultado
        self.resultado = {
            "producto_id": producto_id,
            "cantidad": cantidad,
            "fecha_inicio": date.today().strftime("%Y-%m-%d"),
            "fecha_fin": self.fecha_fin_entry.get(),
            "estado": "En espera"
        }
        
        self.destroy()
    
    def cancelar(self):
        """Cancelar diálogo"""
        self.resultado = None
        self.destroy()

class EditarEstadoVentaDialog(BaseDialog):
    def __init__(self, parent, venta_datos):
        self.venta_datos = venta_datos
        super().__init__(parent, "Cambiar Estado de Venta", "500x450")
    
    def crear_interfaz(self):
        """Crear interfaz del diálogo de editar estado de venta"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="Cambiar Estado de Venta",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Información de la venta
        info_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        info_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        info_title = ctk.CTkLabel(
            info_frame,
            text="Información de la Venta",
            font=ctk.CTkFont(weight="bold")
        )
        info_title.pack(pady=(10, 5))
        
        info_text = f"ID: {self.venta_datos[0]} | Cliente: {self.venta_datos[1]}\n"
        info_text += f"Producto: {self.venta_datos[2]} | Cantidad: {self.venta_datos[3]}\n"
        info_text += f"Total: {self.venta_datos[4]} | Estado actual: {self.venta_datos[5]}"
        
        info_label = ctk.CTkLabel(info_frame, text=info_text)
        info_label.pack(pady=(0, 10))
        
        # Advertencia sobre stock
        warning_frame = ctk.CTkFrame(self, fg_color="#8B4513")
        warning_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        warning_label = ctk.CTkLabel(
            warning_frame,
            text="⚠️ IMPORTANTE: Al finalizar una venta se descontará del stock del producto",
            font=ctk.CTkFont(weight="bold"),
            text_color="white"
        )
        warning_label.pack(pady=10)
        
        # Formulario
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=30, pady=0)
        
        # Nuevo estado
        estado_label = ctk.CTkLabel(form_frame, text="Nuevo Estado:")
        estado_label.pack(anchor="w", pady=(0, 5))
        
        estados_opciones = ["Finalizado", "Rechazado"]
        
        self.estado_combobox = ctk.CTkComboBox(
            form_frame,
            values=estados_opciones,
            width=440
        )
        self.estado_combobox.pack(fill="x", pady=(0, 15))
        
        # Descripción de estados
        desc_frame = ctk.CTkFrame(form_frame, fg_color="#ffffff")
        desc_frame.pack(fill="x", pady=(0, 15))
        
        desc_title = ctk.CTkLabel(
            desc_frame,
            text="Descripción de Estados:",
            font=ctk.CTkFont(weight="bold")
        )
        desc_title.pack(pady=(10, 5))
        
        desc_text = "• Finalizado: Se aprueba la venta y se descuenta del stock\n"
        desc_text += "• Rechazado: Se rechaza la venta sin afectar el stock"
        
        desc_label = ctk.CTkLabel(desc_frame, text=desc_text, justify="left")
        desc_label.pack(pady=(0, 10), padx=10)
        
        # Botones
        self.crear_botones()
    
    def crear_botones(self):
        """Crear botones del diálogo"""
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=20)
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            command=self.cancelar
        )
        cancel_button.pack(side="left", padx=(0, 10))
        
        update_button = ctk.CTkButton(
            button_frame,
            text="Actualizar Estado",
            command=self.guardar
        )
        update_button.pack(side="right")
    
    def guardar(self):
        """Guardar datos del formulario"""
        if not self.estado_combobox.get():
            messagebox.showwarning("Campo requerido", "Selecciona un nuevo estado.")
            return
        
        # Confirmación adicional para estado "Finalizado"
        if self.estado_combobox.get() == "Finalizado":
            if not messagebox.askyesno(
                "Confirmar Finalización",
                f"¿Confirmas que quieres FINALIZAR esta venta?\n\n"
                f"Se descontarán {self.venta_datos[3]} unidades del producto '{self.venta_datos[2]}' del stock.\n\n"
                f"Esta acción no se puede deshacer."
            ):
                return
        
        self.resultado = {
            "estado": self.estado_combobox.get()
        }
        
        self.destroy()
    
    def cancelar(self):
        """Cancelar diálogo"""
        self.resultado = None
        self.destroy()

class EditarEstadoOrdenDialog(BaseDialog):
    def __init__(self, parent, tipo_orden, orden_datos):
        self.tipo_orden = tipo_orden  # "produccion" o "materiales"
        self.orden_datos = orden_datos
        
        title = f"Editar Estado - Orden de {'Producción' if tipo_orden == 'produccion' else 'Materiales'}"
        super().__init__(parent, title, "450x400")
    
    def crear_interfaz(self):
        """Crear interfaz del diálogo de editar estado"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text=f"Editar Estado de Orden",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Información de la orden
        info_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        info_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        info_title = ctk.CTkLabel(
            info_frame,
            text="Información de la Orden",
            font=ctk.CTkFont(weight="bold")
        )
        info_title.pack(pady=(10, 5))
        
        if self.tipo_orden == "produccion":
            info_text = f"ID: {self.orden_datos[0]} | Producto: {self.orden_datos[1]}\nCantidad: {self.orden_datos[2]} | Estado actual: {self.orden_datos[4]}"
        else:
            info_text = f"ID: {self.orden_datos[0]} | Materia: {self.orden_datos[1]}\nCantidad: {self.orden_datos[2]} | Estado actual: {self.orden_datos[4]}"
        
        info_label = ctk.CTkLabel(info_frame, text=info_text)
        info_label.pack(pady=(0, 10))
        
        # Formulario
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=30, pady=0)
        
        # Nuevo estado
        estado_label = ctk.CTkLabel(form_frame, text="Nuevo Estado:")
        estado_label.pack(anchor="w", pady=(0, 5))
        
        if self.tipo_orden == "produccion":
            estados_opciones = ["Cancelado"]
        else:  # materiales
            estados_opciones = ["Finalizado", "Rechazado"]
        
        self.estado_combobox = ctk.CTkComboBox(
            form_frame,
            values=estados_opciones,
            width=390
        )
        self.estado_combobox.pack(fill="x", pady=(0, 15))
        
        # Botones
        self.crear_botones()
    
    def crear_botones(self):
        """Crear botones del diálogo"""
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=20)
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            command=self.cancelar
        )
        cancel_button.pack(side="left", padx=(0, 10))
        
        update_button = ctk.CTkButton(
            button_frame,
            text="Actualizar Estado",
            command=self.guardar
        )
        update_button.pack(side="right")
    
    def guardar(self):
        """Guardar datos del formulario"""
        if not self.estado_combobox.get():
            messagebox.showwarning("Campo requerido", "Selecciona un nuevo estado.")
            return
        
        self.resultado = {
            "estado": self.estado_combobox.get()
        }
        
        self.destroy()
    
    def cancelar(self):
        """Cancelar diálogo"""
        self.resultado = None
        self.destroy()

class OrdenCompraDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent, "Nueva Orden de Compra", "500x650")
    
    def crear_interfaz(self):
        """Crear interfaz del diálogo de orden de compra"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="Nueva Orden de Compra",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Formulario
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=30, pady=0)
        
        # Crear campos
        self.crear_campos(form_frame)
        
        # Botones
        self.crear_botones()
    
    def crear_campos(self, parent):
        """Crear campos del formulario"""
        # Materia Prima
        materia_label = ctk.CTkLabel(parent, text="Materia Prima:")
        materia_label.pack(anchor="w", pady=(0, 5))
        
        from services.materia_prima_service import obtener_materias_para_combobox
        materias_opciones = obtener_materias_para_combobox()
        self.materia_combobox = ctk.CTkComboBox(
            parent,
            values=materias_opciones,
            width=440
        )
        self.materia_combobox.pack(fill="x", pady=(0, 15))
        
        # Proveedor
        proveedor_label = ctk.CTkLabel(parent, text="Proveedor:")
        proveedor_label.pack(anchor="w", pady=(0, 5))
        
        from services.proveedor_service import obtener_proveedores_para_combobox
        proveedores_opciones = obtener_proveedores_para_combobox()
        self.proveedor_combobox = ctk.CTkComboBox(
            parent,
            values=proveedores_opciones,
            width=440
        )
        self.proveedor_combobox.pack(fill="x", pady=(0, 15))
        
        # Cantidad
        cantidad_label = ctk.CTkLabel(parent, text="Cantidad:")
        cantidad_label.pack(anchor="w", pady=(0, 5))
        self.cantidad_entry = ctk.CTkEntry(parent, placeholder_text="Cantidad a solicitar", width=440)
        self.cantidad_entry.pack(fill="x", pady=(0, 15))
        
        # Precio unitario
        precio_label = ctk.CTkLabel(parent, text="Precio Unitario:")
        precio_label.pack(anchor="w", pady=(0, 5))
        self.precio_entry = ctk.CTkEntry(parent, placeholder_text="Precio por unidad", width=440)
        self.precio_entry.pack(fill="x", pady=(0, 15))
        
        # Fecha (automática)
        fecha_label = ctk.CTkLabel(parent, text="Fecha:")
        fecha_label.pack(anchor="w", pady=(0, 5))
        self.fecha_entry = ctk.CTkEntry(parent, width=440)
        self.fecha_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.fecha_entry.configure(state="disabled")
        self.fecha_entry.pack(fill="x", pady=(0, 15))
        
        # Estado (automático)
        estado_label = ctk.CTkLabel(parent, text="Estado:")
        estado_label.pack(anchor="w", pady=(0, 5))
        self.estado_entry = ctk.CTkEntry(parent, width=440)
        self.estado_entry.insert(0, "En espera")
        self.estado_entry.configure(state="disabled")
        self.estado_entry.pack(fill="x", pady=(0, 15))
    
    def crear_botones(self):
        """Crear botones del diálogo"""
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=20)
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            command=self.cancelar
        )
        cancel_button.pack(side="left", padx=(0, 10))
        
        create_button = ctk.CTkButton(
            button_frame,
            text="Crear Orden",
            command=self.guardar
        )
        create_button.pack(side="right")
    
    def guardar(self):
        """Guardar datos del formulario"""
        # Validar campos
        if not self.materia_combobox.get() or not self.proveedor_combobox.get() or not self.cantidad_entry.get() or not self.precio_entry.get():
            messagebox.showwarning("Campos requeridos", "Todos los campos son obligatorios.")
            return
        
        try:
            cantidad = int(self.cantidad_entry.get())
            precio_unitario = float(self.precio_entry.get())
            total = cantidad * precio_unitario
        except ValueError:
            messagebox.showwarning("Valores inválidos", "La cantidad debe ser un número entero y el precio un número válido.")
            return
        
        # Extraer IDs
        materia_seleccionada = self.materia_combobox.get()
        materia_id = int(materia_seleccionada.split(" - ")[0])
        
        proveedor_seleccionado = self.proveedor_combobox.get()
        proveedor_id = int(proveedor_seleccionado.split(" - ")[0])
        
        # Guardar resultado
        self.resultado = {
            "materia_id": materia_id,
            "proveedor_id": proveedor_id,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "total": total,
            "fecha": date.today().strftime("%Y-%m-%d"),
            "estado": "En espera"
        }
        
        self.destroy()
    
    def cancelar(self):
        """Cancelar diálogo"""
        self.resultado = None
        self.destroy()

class EditarEstadoOrdenCompraDialog(BaseDialog):
    def __init__(self, parent, orden_datos):
        self.orden_datos = orden_datos
        super().__init__(parent, "Editar Estado - Orden de Compra", "450x350")
    
    def crear_interfaz(self):
        """Crear interfaz del diálogo de editar estado de orden de compra"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="Editar Estado de Orden de Compra",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Información de la orden
        info_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        info_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        info_title = ctk.CTkLabel(
            info_frame,
            text="Información de la Orden",
            font=ctk.CTkFont(weight="bold")
        )
        info_title.pack(pady=(10, 5))
        
        info_text = f"ID: {self.orden_datos[0]} | Materia: {self.orden_datos[1]}\n"
        info_text += f"Proveedor: {self.orden_datos[2]} | Cantidad: {self.orden_datos[3]}\n"
        info_text += f"Fecha: {self.orden_datos[4]} | Estado actual: {self.orden_datos[5]}"
        
        info_label = ctk.CTkLabel(info_frame, text=info_text)
        info_label.pack(pady=(0, 10))
        
        # Formulario
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=30, pady=0)
        
        # Nuevo estado
        estado_label = ctk.CTkLabel(form_frame, text="Nuevo Estado:")
        estado_label.pack(anchor="w", pady=(0, 5))
        
        estados_opciones = ["Cancelado"]
        
        self.estado_combobox = ctk.CTkComboBox(
            form_frame,
            values=estados_opciones,
            width=390
        )
        self.estado_combobox.pack(fill="x", pady=(0, 15))
        
        # Nota informativa
        nota_frame = ctk.CTkFrame(form_frame, fg_color="#ffffff")
        nota_frame.pack(fill="x", pady=(0, 15))
        
        nota_label = ctk.CTkLabel(
            nota_frame,
            text="ℹ️ Solo se puede cambiar el estado a 'Cancelado'",
            font=ctk.CTkFont(size=12)
        )
        nota_label.pack(pady=10)
        
        # Botones
        self.crear_botones()
    
    def crear_botones(self):
        """Crear botones del diálogo"""
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=20)
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90"),
            command=self.cancelar
        )
        cancel_button.pack(side="left", padx=(0, 10))
        
        update_button = ctk.CTkButton(
            button_frame,
            text="Actualizar Estado",
            command=self.guardar
        )
        update_button.pack(side="right")
    
    def guardar(self):
        """Guardar datos del formulario"""
        if not self.estado_combobox.get():
            messagebox.showwarning("Campo requerido", "Selecciona un nuevo estado.")
            return
        
        self.resultado = {
            "estado": self.estado_combobox.get()
        }
        
        self.destroy()
    
    def cancelar(self):
        """Cancelar diálogo"""
        self.resultado = None
        self.destroy()