"""
Vista del módulo de Recursos Humanos
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from views.base_view import BaseView
from services.empleado_service import obtener_empleados, insertar_empleado, actualizar_empleado, eliminar_empleado
from services.usuario_service import obtener_usuarios, insertar_usuario, eliminar_usuario, actualizar_password_usuario, verificar_usuario_existente
from services.departamento_service import obtener_departamentos_para_combobox

class RecursosHumanosView(BaseView):
    def __init__(self, parent):
        self.empleado_seleccionado = None
        self.usuario_seleccionado = None
        super().__init__(parent)
    
    def crear_vista(self):
        """Crear la vista del módulo de recursos humanos"""
        # Header
        self.crear_header("Módulo de Recursos Humanos")

        # Información del módulo
        info_frame = ctk.CTkFrame(self.parent, fg_color="#edc1ff")
        info_frame.pack(fill="x", padx=20, pady=(10, 0))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="ℹ️ Módulo de Recursos Humanos",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="black"
        )
        info_label.pack(pady=10)
        
        info_desc = ctk.CTkLabel(
            info_frame,
            text="Administra empleados y usuarios del sistema ERP. Aquí puedes agregar, editar o eliminar registros de personal y gestionar sus cuentas de acceso.",
            font=ctk.CTkFont(size=12),
            text_color="black"
        )
        info_desc.pack(pady=(0, 10))
        
        # Pestañas
        self.tabs = ctk.CTkTabview(self.parent)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear pestañas
        self.tab_empleados = self.tabs.add("Empleados")
        self.tab_usuarios = self.tabs.add("Usuarios")
        
        # Configurar pestañas
        self.configurar_tab_empleados()
        self.configurar_tab_usuarios()
    
    def configurar_tab_empleados(self):
        """Configurar pestaña de empleados"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.tab_empleados)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botones de acción
        botones_config = [
            {
                "name": "agregar",
                "text": "Agregar Empleado",
                "command": self.agregar_empleado
            },
            {
                "name": "editar",
                "text": "Editar Empleado",
                "command": self.editar_empleado,
                "state": "disabled"
            },
            {
                "name": "eliminar",
                "text": "Eliminar Empleado",
                "command": self.eliminar_empleado,
                "state": "disabled",
                "fg_color": "red",
                "hover_color": "darkred"
            },
            {
                "name": "nuevo_usuario",
                "text": "Nuevo Usuario",
                "command": self.nuevo_usuario,
                "state": "disabled"
            }
        ]
        
        self.botones_empleados_frame, self.botones_empleados = self.crear_botones_accion(main_frame, botones_config)
        
        # Tabla
        columnas = ("ID", "Nombre", "Correo", "RFC", "Puesto", "Departamento", "Salario", "Fecha Contratación")
        self.empleados_table_frame, self.empleados_table = self.crear_tabla_frame(main_frame, columnas)
        
        # Configurar columnas específicas
        self.empleados_table.column("ID", anchor="center", width=50)
        self.empleados_table.column("Nombre", anchor="w", width=180)
        self.empleados_table.column("Correo", anchor="w", width=200)
        self.empleados_table.column("RFC", anchor="center", width=120)
        self.empleados_table.column("Puesto", anchor="center", width=120)
        self.empleados_table.column("Departamento", anchor="center", width=100)
        self.empleados_table.column("Salario", anchor="e", width=100)
        self.empleados_table.column("Fecha Contratación", anchor="center", width=120)
        
        for col in columnas:
            self.empleados_table.heading(col, text=col)
        
        # Evento de selección
        self.empleados_table.bind("<<TreeviewSelect>>", self.on_empleado_select)
        
        # Cargar datos
        self.cargar_empleados()
    
    def configurar_tab_usuarios(self):
        """Configurar pestaña de usuarios"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.tab_usuarios)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botones de acción
        botones_config = [
            {
                "name": "eliminar",
                "text": "Eliminar Usuario",
                "command": self.eliminar_usuario,
                "state": "disabled",
                "fg_color": "red",
                "hover_color": "darkred"
            },
            {
                "name": "editar_password",
                "text": "Editar Contraseña",
                "command": self.editar_password,
                "state": "disabled"
            }
        ]
        
        self.botones_usuarios_frame, self.botones_usuarios = self.crear_botones_accion(main_frame, botones_config)
        
        # Tabla
        columnas = ("ID Usuario", "Correo", "Contraseña", "ID Empleado")
        self.usuarios_table_frame, self.usuarios_table = self.crear_tabla_frame(main_frame, columnas)
        
        # Configurar columnas específicas
        self.usuarios_table.column("ID Usuario", anchor="center", width=100)
        self.usuarios_table.column("Correo", anchor="w", width=250)
        self.usuarios_table.column("Contraseña", anchor="center", width=150)
        self.usuarios_table.column("ID Empleado", anchor="center", width=120)
        
        for col in columnas:
            self.usuarios_table.heading(col, text=col)
        
        # Evento de selección
        self.usuarios_table.bind("<<TreeviewSelect>>", self.on_usuario_select)
        
        # Cargar datos
        self.cargar_usuarios()
    
    def cargar_empleados(self):
        """Cargar empleados en la tabla"""
        # Limpiar tabla
        for row in self.empleados_table.get_children():
            self.empleados_table.delete(row)
        
        # Obtener empleados
        empleados = obtener_empleados()
        
        # Insertar en la tabla
        for empleado in empleados:
            # Formatear salario
            empleado_formateado = list(empleado)
            empleado_formateado[6] = f"${empleado[6]}"
            self.empleados_table.insert("", "end", values=empleado_formateado)
    
    def cargar_usuarios(self):
        """Cargar usuarios en la tabla"""
        # Limpiar tabla
        for row in self.usuarios_table.get_children():
            self.usuarios_table.delete(row)
        
        # Obtener usuarios
        usuarios = obtener_usuarios()
        
        # Insertar en la tabla
        for usuario in usuarios:
            # Ocultar contraseña
            usuario_formateado = list(usuario)
            if len(usuario_formateado) > 2:
                usuario_formateado[2] = "********"
            self.usuarios_table.insert("", "end", values=usuario_formateado)
    
    def on_empleado_select(self, event):
        """Manejar selección de empleado"""
        selected = self.empleados_table.selection()
        if selected:
            self.empleado_seleccionado = self.empleados_table.item(selected[0], "values")
            self.botones_empleados["editar"].configure(state="normal")
            self.botones_empleados["eliminar"].configure(state="normal")
            self.botones_empleados["nuevo_usuario"].configure(state="normal")
        else:
            self.empleado_seleccionado = None
            self.botones_empleados["editar"].configure(state="disabled")
            self.botones_empleados["eliminar"].configure(state="disabled")
            self.botones_empleados["nuevo_usuario"].configure(state="disabled")
    
    def on_usuario_select(self, event):
        """Manejar selección de usuario"""
        selected = self.usuarios_table.selection()
        if selected:
            self.usuario_seleccionado = self.usuarios_table.item(selected[0], "values")
            self.botones_usuarios["eliminar"].configure(state="normal")
            self.botones_usuarios["editar_password"].configure(state="normal")
        else:
            self.usuario_seleccionado = None
            self.botones_usuarios["eliminar"].configure(state="disabled")
            self.botones_usuarios["editar_password"].configure(state="disabled")
    
    def agregar_empleado(self):
        """Abrir ventana para agregar empleado"""
        from components.dialogs import EmpleadoDialog
        
        dialog = EmpleadoDialog(self.parent, "agregar")
        if dialog.resultado:
            if insertar_empleado(
                dialog.resultado["nombre"],
                dialog.resultado["correo"],
                dialog.resultado["rfc"],
                dialog.resultado["puesto"],
                dialog.resultado["departamento_id"],
                dialog.resultado["salario"],
                dialog.resultado["fecha_contratacion"]
            ):
                self.cargar_empleados()
                messagebox.showinfo("Éxito", f"{dialog.resultado['nombre']} ha sido agregado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo agregar el empleado.")
    
    def editar_empleado(self):
        """Abrir ventana para editar empleado"""
        if not self.empleado_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un empleado primero.")
            return
        
        from components.dialogs import EmpleadoDialog
        
        dialog = EmpleadoDialog(self.parent, "editar", self.empleado_seleccionado)
        if dialog.resultado:
            if actualizar_empleado(
                self.empleado_seleccionado[0],  # ID del empleado
                dialog.resultado["nombre"],
                dialog.resultado["correo"],
                dialog.resultado["rfc"],
                dialog.resultado["puesto"],
                dialog.resultado["departamento_id"],
                dialog.resultado["salario"],
                dialog.resultado["fecha_contratacion"]
            ):
                self.cargar_empleados()
                messagebox.showinfo("Éxito", f"{dialog.resultado['nombre']} ha sido actualizado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el empleado.")
    
    def eliminar_empleado(self):
        """Eliminar empleado seleccionado"""
        if not self.empleado_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un empleado primero.")
            return
        
        if messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar al empleado {self.empleado_seleccionado[1]}?\n\nEsta acción no se puede deshacer."
        ):
            if eliminar_empleado(self.empleado_seleccionado[0]):
                self.cargar_empleados()
                self.cargar_usuarios()  # Recargar usuarios también
                messagebox.showinfo("Éxito", f"{self.empleado_seleccionado[1]} ha sido eliminado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el empleado.")
    
    def nuevo_usuario(self):
        """Crear nuevo usuario para empleado seleccionado"""
        if not self.empleado_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un empleado primero.")
            return
        
        # Verificar si el empleado ya tiene usuario
        empleado_id = self.empleado_seleccionado[0]
        if verificar_usuario_existente(empleado_id):
            messagebox.showwarning("Usuario existente", "Este empleado ya tiene un usuario asignado.")
            return
        
        from components.dialogs import UsuarioDialog
        
        dialog = UsuarioDialog(self.parent, self.empleado_seleccionado)
        if dialog.resultado:
            if insertar_usuario(
                dialog.resultado["correo"],
                dialog.resultado["password"],
                dialog.resultado["empleado_id"]
            ):
                self.cargar_usuarios()
                messagebox.showinfo("Éxito", f"Usuario para {self.empleado_seleccionado[1]} creado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo crear el usuario.")
    
    def eliminar_usuario(self):
        """Eliminar usuario seleccionado"""
        if not self.usuario_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un usuario primero.")
            return
        
        if messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar el usuario {self.usuario_seleccionado[1]}?\n\nEsta acción no se puede deshacer."
        ):
            if eliminar_usuario(self.usuario_seleccionado[0]):
                self.cargar_usuarios()
                messagebox.showinfo("Éxito", f"Usuario {self.usuario_seleccionado[1]} eliminado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario.")
    
    def editar_password(self):
        """Editar contraseña de usuario seleccionado"""
        if not self.usuario_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un usuario primero.")
            return
        
        from components.dialogs import PasswordDialog
        
        dialog = PasswordDialog(self.parent, self.usuario_seleccionado)
        if dialog.resultado:
            if actualizar_password_usuario(
                self.usuario_seleccionado[0],
                dialog.resultado["password"]
            ):
                messagebox.showinfo("Éxito", f"Contraseña de {self.usuario_seleccionado[1]} actualizada correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar la contraseña.")