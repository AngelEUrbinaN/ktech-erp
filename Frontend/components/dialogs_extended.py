"""
Diálogos adicionales para empleados, usuarios, clientes y ventas
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from components.dialogs import BaseDialog
from services.departamento_service import obtener_departamentos_para_combobox
from services.producto_service import obtener_producto_por_nombre

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

class EmpleadoDialog(BaseDialog):
    def __init__(self, parent, modo="agregar", datos=None):
        self.modo = modo
        self.datos = datos
        
        title = f"{'Agregar' if modo == 'agregar' else 'Editar'} Empleado"
        super().__init__(parent, title, "500x750")
    
    def crear_interfaz(self):
        """Crear interfaz del diálogo de empleado"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text=f"{'Agregar Nuevo' if self.modo == 'agregar' else 'Editar'} Empleado",
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
        nombre_label = ctk.CTkLabel(parent, text="Nombre Completo:")
        nombre_label.pack(anchor="w", pady=(0, 5))
        self.nombre_entry = ctk.CTkEntry(parent, placeholder_text="Nombre completo", width=440)
        self.nombre_entry.pack(fill="x", pady=(0, 15))
        
        # Correo
        correo_label = ctk.CTkLabel(parent, text="Correo:")
        correo_label.pack(anchor="w", pady=(0, 5))
        self.correo_entry = ctk.CTkEntry(parent, placeholder_text="correo@ktech.com", width=440)
        self.correo_entry.pack(fill="x", pady=(0, 15))
        
        # RFC
        rfc_label = ctk.CTkLabel(parent, text="RFC:")
        rfc_label.pack(anchor="w", pady=(0, 5))
        self.rfc_entry = ctk.CTkEntry(parent, placeholder_text="RFC del empleado", width=440)
        self.rfc_entry.pack(fill="x", pady=(0, 15))
        
        # Puesto
        puesto_label = ctk.CTkLabel(parent, text="Puesto:")
        puesto_label.pack(anchor="w", pady=(0, 5))
        self.puesto_entry = ctk.CTkEntry(parent, placeholder_text="Puesto de trabajo", width=440)
        self.puesto_entry.pack(fill="x", pady=(0, 15))
        
        # Departamento
        departamento_label = ctk.CTkLabel(parent, text="Departamento:")
        departamento_label.pack(anchor="w", pady=(0, 5))
        
        departamentos_opciones = obtener_departamentos_para_combobox()
        self.departamento_combobox = ctk.CTkComboBox(
            parent,
            values=departamentos_opciones,
            width=440
        )
        self.departamento_combobox.pack(fill="x", pady=(0, 15))
        
        # Salario
        salario_label = ctk.CTkLabel(parent, text="Salario:")
        salario_label.pack(anchor="w", pady=(0, 5))
        self.salario_entry = ctk.CTkEntry(parent, placeholder_text="Salario mensual", width=440)
        self.salario_entry.pack(fill="x", pady=(0, 15))
        
        # Fecha de contratación
        fecha_label = ctk.CTkLabel(parent, text="Fecha de Contratación:")
        fecha_label.pack(anchor="w", pady=(0, 5))
        self.fecha_entry = ctk.CTkEntry(parent, placeholder_text="YYYY-MM-DD", width=440)
        self.fecha_entry.pack(fill="x", pady=(0, 15))
        
        # Llenar campos si es edición
        if self.modo == "editar" and self.datos:
            self.nombre_entry.insert(0, self.datos[1])
            self.correo_entry.insert(0, self.datos[2])
            self.rfc_entry.insert(0, self.datos[3])
            self.puesto_entry.insert(0, self.datos[4])
            
            # Buscar departamento correspondiente
            departamento_actual = self.datos[5]
            for opcion in departamentos_opciones:
                if departamento_actual in opcion:
                    self.departamento_combobox.set(opcion)
                    break
            
            # Limpiar formato de salario
            salario_limpio = self.datos[6].replace("$", "").replace(",", "")
            self.salario_entry.insert(0, salario_limpio)
            self.fecha_entry.insert(0, self.datos[7])
        else:
            # Fecha por defecto
            self.fecha_entry.insert(0, date.today().strftime("%Y-%m-%d"))
    
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
            text=f"{'Agregar' if self.modo == 'agregar' else 'Actualizar'} Empleado",
            command=self.guardar
        )
        save_button.pack(side="right")
    
    def guardar(self):
        """Guardar datos del formulario"""
        # Validar campos
        if not all([self.nombre_entry.get(), self.correo_entry.get(), self.rfc_entry.get(),
                   self.puesto_entry.get(), self.departamento_combobox.get(), 
                   self.salario_entry.get(), self.fecha_entry.get()]):
            messagebox.showwarning("Campos requeridos", "Todos los campos son obligatorios.")
            return
        
        try:
            salario = float(self.salario_entry.get())
        except ValueError:
            messagebox.showwarning("Salario inválido", "El salario debe ser un número válido.")
            return
        
        # Extraer ID del departamento
        departamento_seleccionado = self.departamento_combobox.get()
        departamento_id = int(departamento_seleccionado.split(" - ")[0])
        
        # Guardar resultado
        self.resultado = {
            "nombre": self.nombre_entry.get(),
            "correo": self.correo_entry.get(),
            "rfc": self.rfc_entry.get(),
            "puesto": self.puesto_entry.get(),
            "departamento_id": departamento_id,
            "salario": salario,
            "fecha_contratacion": self.fecha_entry.get()
        }
        
        self.destroy()
    
    def cancelar(self):
        """Cancelar diálogo"""
        self.resultado = None
        self.destroy()

class UsuarioDialog(BaseDialog):
    def __init__(self, parent, empleado_datos):
        self.empleado_datos = empleado_datos
        super().__init__(parent, "Nuevo Usuario", "450x450")
    
    def crear_interfaz(self):
        """Crear interfaz del diálogo de usuario"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="Crear Nuevo Usuario",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Información del empleado
        empleado_frame = ctk.CTkFrame(self, fg_color="#2b2b2b")
        empleado_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        empleado_title = ctk.CTkLabel(
            empleado_frame,
            text="Información del Empleado",
            font=ctk.CTkFont(weight="bold")
        )
        empleado_title.pack(pady=(10, 5))
        
        empleado_info = ctk.CTkLabel(
            empleado_frame,
            text=f"ID: {self.empleado_datos[0]} | Nombre: {self.empleado_datos[1]}\nCorreo: {self.empleado_datos[2]}"
        )
        empleado_info.pack(pady=(0, 10))
        
        # Formulario
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=30, pady=0)
        
        # Campos
        correo_label = ctk.CTkLabel(form_frame, text="Correo:")
        correo_label.pack(anchor="w", pady=(0, 5))
        self.correo_entry = ctk.CTkEntry(form_frame, width=390)
        self.correo_entry.insert(0, self.empleado_datos[2])
        self.correo_entry.configure(state="disabled")
        self.correo_entry.pack(fill="x", pady=(0, 15))
        
        password_label = ctk.CTkLabel(form_frame, text="Contraseña:")
        password_label.pack(anchor="w", pady=(0, 5))
        self.password_entry = ctk.CTkEntry(form_frame, placeholder_text="Contraseña del usuario", show="*", width=390)
        self.password_entry.pack(fill="x", pady=(0, 15))
        
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
        
        create_button = ctk.CTkButton(
            button_frame,
            text="Crear Usuario",
            command=self.guardar
        )
        create_button.pack(side="right")
    
    def guardar(self):
        """Guardar datos del formulario"""
        if not self.password_entry.get():
            messagebox.showwarning("Campo requerido", "La contraseña es obligatoria.")
            return
        
        self.resultado = {
            "correo": self.empleado_datos[2],
            "password": self.password_entry.get(),
            "empleado_id": self.empleado_datos[0]
        }
        
        self.destroy()
    
    def cancelar(self):
        """Cancelar diálogo"""
        self.resultado = None
        self.destroy()

class PasswordDialog(BaseDialog):
    def __init__(self, parent, usuario_datos):
        self.usuario_datos = usuario_datos
        super().__init__(parent, "Editar Contraseña", "400x350")
    
    def crear_interfaz(self):
        """Crear interfaz del diálogo de contraseña"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="Editar Contraseña",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Información del usuario
        usuario_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        usuario_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        usuario_title = ctk.CTkLabel(
            usuario_frame,
            text="Información del Usuario",
            font=ctk.CTkFont(weight="bold")
        )
        usuario_title.pack(pady=(10, 5))
        
        usuario_info = ctk.CTkLabel(
            usuario_frame,
            text=f"ID: {self.usuario_datos[0]} | Correo: {self.usuario_datos[1]}"
        )
        usuario_info.pack(pady=(0, 10))
        
        # Formulario
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=30, pady=0)
        
        password_label = ctk.CTkLabel(form_frame, text="Nueva Contraseña:")
        password_label.pack(anchor="w", pady=(0, 5))
        self.password_entry = ctk.CTkEntry(form_frame, placeholder_text="Nueva contraseña", show="*", width=340)
        self.password_entry.pack(fill="x", pady=(0, 15))
        
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
            text="Actualizar Contraseña",
            command=self.guardar
        )
        update_button.pack(side="right")
    
    def guardar(self):
        """Guardar datos del formulario"""
        if not self.password_entry.get():
            messagebox.showwarning("Campo requerido", "La nueva contraseña es obligatoria.")
            return
        
        self.resultado = {
            "password": self.password_entry.get()
        }
        
        self.destroy()
    
    def cancelar(self):
        """Cancelar diálogo"""
        self.resultado = None
        self.destroy()

class ClienteDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent, "Agregar Cliente", "500x450")
    
    def crear_interfaz(self):
        """Crear interfaz del diálogo de cliente"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="Agregar Nuevo Cliente",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Formulario
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=30, pady=0)
        
        # Campos
        nombre_label = ctk.CTkLabel(form_frame, text="Nombre:")
        nombre_label.pack(anchor="w", pady=(0, 5))
        self.nombre_entry = ctk.CTkEntry(form_frame, placeholder_text="Nombre completo", width=340)
        self.nombre_entry.pack(fill="x", pady=(0, 15))
        
        email_label = ctk.CTkLabel(form_frame, text="Email:")
        email_label.pack(anchor="w", pady=(0, 5))
        self.email_entry = ctk.CTkEntry(form_frame, placeholder_text="correo@ejemplo.com", width=340)
        self.email_entry.pack(fill="x", pady=(0, 15))
        
        telefono_label = ctk.CTkLabel(form_frame, text="Teléfono:")
        telefono_label.pack(anchor="w", pady=(0, 5))
        self.telefono_entry = ctk.CTkEntry(form_frame, placeholder_text="Número de teléfono", width=340)
        self.telefono_entry.pack(fill="x", pady=(0, 15))
        
        direccion_label = ctk.CTkLabel(form_frame, text="Dirección:")
        direccion_label.pack(anchor="w", pady=(0, 5))
        self.direccion_entry = ctk.CTkEntry(form_frame, placeholder_text="Dirección completa", width=340)
        self.direccion_entry.pack(fill="x", pady=(0, 15))
        
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
        
        register_button = ctk.CTkButton(
            button_frame,
            text="Registrar Cliente",
            command=self.guardar
        )
        register_button.pack(side="right")
    
    def guardar(self):
        """Guardar datos del formulario"""
        if not self.nombre_entry.get() or not self.email_entry.get():
            messagebox.showwarning("Campos requeridos", "Nombre y email son obligatorios.")
            return
        
        self.resultado = {
            "nombre": self.nombre_entry.get(),
            "email": self.email_entry.get(),
            "telefono": self.telefono_entry.get(),
            "direccion": self.direccion_entry.get()
        }
        
        self.destroy()
    
    def cancelar(self):
        """Cancelar diálogo"""
        self.resultado = None
        self.destroy()

class BuscarClienteDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent, "Buscar Cliente", "400x250")
    
    def crear_interfaz(self):
        """Crear interfaz del diálogo de búsqueda"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="Buscar Cliente por Email",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Formulario
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=30, pady=0)
        
        email_label = ctk.CTkLabel(form_frame, text="Email del cliente:")
        email_label.pack(anchor="w", pady=(0, 5))
        
        search_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 15))
        
        self.email_entry = ctk.CTkEntry(search_frame, placeholder_text="correo@ejemplo.com", width=280)
        self.email_entry.pack(side="left")
        
        search_button = ctk.CTkButton(
            search_frame,
            text="Buscar",
            width=60,
            command=self.buscar
        )
        search_button.pack(side="right", padx=(10, 0))
        
        # Botón de cerrar
        close_button = ctk.CTkButton(
            self,
            text="Cerrar",
            command=self.cancelar
        )
        close_button.pack(pady=20)
    
    def buscar(self):
        """Buscar cliente"""
        email = self.email_entry.get().strip()
        if not email:
            messagebox.showwarning("Campo vacío", "Por favor ingresa un correo.")
            return
        
        self.resultado = {"email": email}
        self.destroy()
    
    def cancelar(self):
        """Cancelar diálogo"""
        self.resultado = None
        self.destroy()

class VentaDialog(BaseDialog):
    def __init__(self, parent, cliente_datos):
        self.cliente_datos = cliente_datos
        super().__init__(parent, "Nueva Venta", "500x700")
    
    def crear_interfaz(self):
        """Crear interfaz del diálogo de venta"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="Registrar Nueva Venta",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Información del cliente
        cliente_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        cliente_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        cliente_title = ctk.CTkLabel(
            cliente_frame,
            text="Información del Cliente",
            font=ctk.CTkFont(weight="bold")
        )
        cliente_title.pack(pady=(10, 5))
        
        cliente_info = ctk.CTkLabel(
            cliente_frame,
            text=f"ID: {self.cliente_datos[0]} | Nombre: {self.cliente_datos[1]}\nEmail: {self.cliente_datos[2]}"
        )
        cliente_info.pack(pady=(0, 10))
        
        # Formulario
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=30, pady=0)
        
        # Crear campos
        self.crear_campos(form_frame)
        
        # Botones
        self.crear_botones()
    
    def crear_campos(self, parent):
        """Crear campos del formulario"""
        # Fecha
        fecha_label = ctk.CTkLabel(parent, text="Fecha:")
        fecha_label.pack(anchor="w", pady=(0, 5))
        self.fecha_entry = ctk.CTkEntry(parent, width=440)
        self.fecha_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.fecha_entry.configure(state="disabled")
        self.fecha_entry.pack(fill="x", pady=(0, 15))
        
        # Producto
        producto_label = ctk.CTkLabel(parent, text="Producto:")
        producto_label.pack(anchor="w", pady=(0, 5))
        
        producto_frame = ctk.CTkFrame(parent, fg_color="transparent")
        producto_frame.pack(fill="x", pady=(0, 15))
        
        self.producto_entry = ctk.CTkEntry(producto_frame, placeholder_text="Nombre del producto", width=370)
        self.producto_entry.pack(side="left")
        
        # Variables para producto
        self.producto_id = None
        self.precio_unitario = None
        
        search_button = ctk.CTkButton(
            producto_frame,
            text="Buscar",
            width=60,
            command=self.buscar_producto
        )
        search_button.pack(side="right", padx=(10, 0))
        
        # Información del producto
        self.producto_info_frame = ctk.CTkFrame(parent, fg_color="#2b2b2b")
        self.producto_info_label = ctk.CTkLabel(self.producto_info_frame, text="")
        self.producto_info_label.pack(pady=10)
        
        # Cantidad
        cantidad_label = ctk.CTkLabel(parent, text="Cantidad:")
        cantidad_label.pack(anchor="w", pady=(0, 5))
        self.cantidad_entry = ctk.CTkEntry(parent, placeholder_text="Cantidad", width=440)
        self.cantidad_entry.pack(fill="x", pady=(0, 15))
        
        # Precio unitario
        precio_label = ctk.CTkLabel(parent, text="Precio Unitario:")
        precio_label.pack(anchor="w", pady=(0, 5))
        self.precio_entry = ctk.CTkEntry(parent, placeholder_text="Precio unitario", width=440)
        self.precio_entry.pack(fill="x", pady=(0, 15))
        
        # Total
        total_label = ctk.CTkLabel(parent, text="Total:")
        total_label.pack(anchor="w", pady=(0, 5))
        self.total_entry = ctk.CTkEntry(parent, placeholder_text="Total", width=440)
        self.total_entry.pack(fill="x", pady=(0, 15))
        
        # Eventos para calcular total
        self.cantidad_entry.bind("<KeyRelease>", self.calcular_total)
        self.precio_entry.bind("<KeyRelease>", self.calcular_total)
    
    def buscar_producto(self):
        """Buscar producto por nombre"""
        nombre = self.producto_entry.get().strip()
        if not nombre:
            messagebox.showwarning("Advertencia", "Ingresa el nombre del producto.")
            return
        
        producto = obtener_producto_por_nombre(nombre)
        if not producto:
            messagebox.showinfo("Producto no encontrado", "No existe un producto con ese nombre.")
            self.producto_info_frame.pack_forget()
        else:
            self.producto_id = producto["id_producto"]
            self.precio_unitario = producto["precio_unitario"]
            
            # Actualizar campo de precio
            self.precio_entry.delete(0, "end")
            self.precio_entry.insert(0, str(self.precio_unitario))
            
            # Mostrar información del producto
            self.producto_info_frame.pack(fill="x", pady=(0, 15))
            self.producto_info_label.configure(
                text=f"ID: {producto['id_producto']} | Stock: {producto['stock_actual']} unidades"
            )
            
            # Calcular total si hay cantidad
            self.calcular_total()
    
    def calcular_total(self, event=None):
        """Calcular total de la venta"""
        try:
            cantidad = int(self.cantidad_entry.get()) if self.cantidad_entry.get() else 0
            precio = float(self.precio_entry.get()) if self.precio_entry.get() else 0
            total = cantidad * precio
            
            self.total_entry.delete(0, "end")
            total = cantidad * precio
            
            self.total_entry.delete(0, "end")
            self.total_entry.insert(0, f"{total}")
        except ValueError:
            pass
    
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
        
        register_button = ctk.CTkButton(
            button_frame,
            text="Registrar Venta",
            command=self.guardar
        )
        register_button.pack(side="right")
    
    def guardar(self):
        """Guardar datos del formulario"""
        # Validar campos
        if not self.producto_id or not self.cantidad_entry.get() or not self.precio_entry.get():
            messagebox.showwarning("Campos requeridos", "Producto, cantidad y precio son obligatorios.")
            return
        
        try:
            cantidad = int(self.cantidad_entry.get())
            precio_unitario = float(self.precio_entry.get())
        except ValueError:
            messagebox.showwarning("Valores inválidos", "Cantidad y precio deben ser números válidos.")
            return
        
        self.resultado = {
            "cliente_id": self.cliente_datos[0],
            "producto_id": self.producto_id,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario
        }
        
        self.destroy()
    
    def cancelar(self):
        """Cancelar diálogo"""
        self.resultado = None
        self.destroy()
