"""
Diálogos reutilizables para el sistema
"""

import customtkinter as ctk
from tkinter import messagebox

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

class DepartamentoDialog(BaseDialog):
    def __init__(self, parent, modo="agregar", datos=None):
        self.modo = modo
        self.datos = datos
        
        title = f"{'Agregar' if modo == 'agregar' else 'Editar'} Departamento"
        super().__init__(parent, title, "500x500")
    
    def crear_interfaz(self):
        """Crear interfaz del diálogo de departamento"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text=f"{'Agregar Nuevo' if self.modo == 'agregar' else 'Editar'} Departamento",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Formulario
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=30, pady=0)
        
        # Campos
        self.crear_campos(form_frame)
        
        # Botones
        self.crear_botones()
    
    def crear_campos(self, parent):
        """Crear campos del formulario"""
        # Nombre
        nombre_label = ctk.CTkLabel(parent, text="Nombre del Departamento:")
        nombre_label.pack(anchor="w", pady=(0, 5))
        self.nombre_entry = ctk.CTkEntry(parent, placeholder_text="Nombre del departamento", width=440)
        self.nombre_entry.pack(fill="x", pady=(0, 15))
        
        # Presupuesto
        presupuesto_label = ctk.CTkLabel(parent, text="Presupuesto:")
        presupuesto_label.pack(anchor="w", pady=(0, 5))
        self.presupuesto_entry = ctk.CTkEntry(parent, placeholder_text="Presupuesto asignado", width=440)
        self.presupuesto_entry.pack(fill="x", pady=(0, 15))
        
        # Descripción
        descripcion_label = ctk.CTkLabel(parent, text="Descripción:")
        descripcion_label.pack(anchor="w", pady=(0, 5))
        self.descripcion_textbox = ctk.CTkTextbox(parent, height=100, width=440)
        self.descripcion_textbox.pack(fill="x", pady=(0, 15))
        
        # Llenar campos si es edición
        if self.modo == "editar" and self.datos:
            self.nombre_entry.insert(0, self.datos[1])
            presupuesto_limpio = self.datos[2].replace("$", "").replace(",", "")
            self.presupuesto_entry.insert(0, presupuesto_limpio)
            self.descripcion_textbox.insert("1.0", self.datos[3])
    
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
            text=f"{'Agregar' if self.modo == 'agregar' else 'Actualizar'} Departamento",
            command=self.guardar
        )
        save_button.pack(side="right")
    
    def guardar(self):
        """Guardar datos del formulario"""
        # Validar campos
        if not all([self.nombre_entry.get(), self.presupuesto_entry.get(), 
                   self.descripcion_textbox.get("1.0", "end-1c")]):
            messagebox.showwarning("Campos requeridos", "Todos los campos son obligatorios.")
            return
        
        try:
            presupuesto = float(self.presupuesto_entry.get())
        except ValueError:
            messagebox.showwarning("Presupuesto inválido", "El presupuesto debe ser un número válido.")
            return
        
        # Guardar resultado
        self.resultado = {
            "nombre": self.nombre_entry.get(),
            "presupuesto": presupuesto,
            "descripcion": self.descripcion_textbox.get("1.0", "end-1c")
        }
        
        self.destroy()
    
    def cancelar(self):
        """Cancelar diálogo"""
        self.resultado = None
        self.destroy()

# Importar diálogos adicionales
from components.dialogs_extended import (
    EmpleadoDialog, 
    UsuarioDialog, 
    PasswordDialog, 
    ClienteDialog, 
    BuscarClienteDialog, 
    VentaDialog
)