"""
Diálogos específicos para el módulo de Compras
"""

import customtkinter as ctk
from tkinter import messagebox
import re
from components.dialogs import BaseDialog

class ProveedorDialog(BaseDialog):
    def __init__(self, parent, modo, datos_proveedor=None):
        self.modo = modo
        self.datos_proveedor = datos_proveedor
        titulo = "Agregar Proveedor" if modo == "agregar" else "Editar Proveedor"
        super().__init__(parent, titulo, "600x600")

    def crear_interfaz(self):
        """Crear interfaz del diálogo de proveedor"""
        # Título
        titulo_texto = "Nuevo Proveedor" if self.modo == "agregar" else "Editar Proveedor"
        title_label = ctk.CTkLabel(
            self,
            text=titulo_texto,
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
        # Nombre del proveedor
        nombre_label = ctk.CTkLabel(parent, text="Nombre del Proveedor:")
        nombre_label.pack(anchor="w", pady=(0, 5))
        self.nombre_entry = ctk.CTkEntry(parent, placeholder_text="Nombre completo del contacto", width=540)
        if self.datos_proveedor:
            self.nombre_entry.insert(0, self.datos_proveedor[1])
        self.nombre_entry.pack(fill="x", pady=(0, 15))
        
        # Nombre de la empresa
        empresa_label = ctk.CTkLabel(parent, text="Nombre de la Empresa:")
        empresa_label.pack(anchor="w", pady=(0, 5))
        self.empresa_entry = ctk.CTkEntry(parent, placeholder_text="Razón social o nombre comercial", width=540)
        if self.datos_proveedor:
            self.empresa_entry.insert(0, self.datos_proveedor[2])
        self.empresa_entry.pack(fill="x", pady=(0, 15))
        
        # Correo electrónico
        correo_label = ctk.CTkLabel(parent, text="Correo Electrónico:")
        correo_label.pack(anchor="w", pady=(0, 5))
        self.correo_entry = ctk.CTkEntry(parent, placeholder_text="ejemplo@empresa.com", width=540)
        if self.datos_proveedor:
            self.correo_entry.insert(0, self.datos_proveedor[3])
        self.correo_entry.pack(fill="x", pady=(0, 15))
        
        # Teléfono
        telefono_label = ctk.CTkLabel(parent, text="Teléfono:")
        telefono_label.pack(anchor="w", pady=(0, 5))
        self.telefono_entry = ctk.CTkEntry(parent, placeholder_text="+1234567890", width=540)
        if self.datos_proveedor:
            self.telefono_entry.insert(0, self.datos_proveedor[4])
        self.telefono_entry.pack(fill="x", pady=(0, 15))
        
        # Dirección
        direccion_label = ctk.CTkLabel(parent, text="Dirección:")
        direccion_label.pack(anchor="w", pady=(0, 5))
        self.direccion_entry = ctk.CTkEntry(parent, placeholder_text="Dirección completa de la empresa", width=540)
        if self.datos_proveedor:
            self.direccion_entry.insert(0, self.datos_proveedor[5])
        self.direccion_entry.pack(fill="x", pady=(0, 15))
        
        # Nota informativa
        nota_frame = ctk.CTkFrame(parent, fg_color="#ffffff")
        nota_frame.pack(fill="x", pady=(0, 15))
        
        nota_label = ctk.CTkLabel(
            nota_frame,
            text="📋 Asegúrate de que toda la información de contacto sea correcta para facilitar las comunicaciones.",
            font=ctk.CTkFont(size=12)
        )
        nota_label.pack(pady=10)

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
        
        texto_boton = "Agregar Proveedor" if self.modo == "agregar" else "Actualizar Proveedor"
        save_button = ctk.CTkButton(
            button_frame,
            text=texto_boton,
            command=self.guardar,
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        save_button.pack(side="right")

    def validar_correo(self, correo):
        """Validar formato de correo electrónico"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, correo) is not None

    def guardar(self):
        """Guardar datos del formulario"""
        # Validar campos obligatorios
        if not all([
            self.nombre_entry.get().strip(),
            self.empresa_entry.get().strip(),
            self.correo_entry.get().strip(),
            self.telefono_entry.get().strip(),
            self.direccion_entry.get().strip()
        ]):
            messagebox.showwarning("Campos requeridos", "Todos los campos son obligatorios.")
            return
        
        # Validar formato de correo
        if not self.validar_correo(self.correo_entry.get().strip()):
            messagebox.showwarning("Correo inválido", "Por favor ingresa un correo electrónico válido.")
            return
        
        # Guardar resultado
        self.resultado = {
            "nombre": self.nombre_entry.get().strip(),
            "empresa": self.empresa_entry.get().strip(),
            "correo": self.correo_entry.get().strip(),
            "telefono": self.telefono_entry.get().strip(),
            "direccion": self.direccion_entry.get().strip()
        }
        
        self.destroy()

    def cancelar(self):
        """Cancelar diálogo"""
        self.resultado = None
        self.destroy()

class ProcesarCompraDialog(BaseDialog):
    def __init__(self, parent, compra_datos):
        self.compra_datos = compra_datos
        super().__init__(parent, "Procesar Orden de Compra", "550x500")

    def crear_interfaz(self):
        """Crear interfaz del diálogo de procesar compra"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="Procesar Orden de Compra",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Información de la orden
        info_frame = ctk.CTkFrame(self, fg_color="#8B4513")
        info_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        info_title = ctk.CTkLabel(
            info_frame,
            text="Información de la Orden",
            font=ctk.CTkFont(weight="bold"),
            text_color="white"
        )
        info_title.pack(pady=(10, 5))
        
        info_text = f"ID: {self.compra_datos[0]} | Materia: {self.compra_datos[1]}\n"
        info_text += f"Proveedor: {self.compra_datos[2]} | Cantidad: {self.compra_datos[3]}\n"
        info_text += f"Precio Unit.: {self.compra_datos[4]} | Total: {self.compra_datos[5]}\n"
        info_text += f"Fecha: {self.compra_datos[6]} | Estado actual: {self.compra_datos[7]}"
        
        info_label = ctk.CTkLabel(
            info_frame, 
            text=info_text,
            text_color="lightgray"
        )
        info_label.pack(pady=(0, 10))
        
        # Formulario
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill="x", padx=30, pady=0)
        
        # Nuevo estado
        estado_label = ctk.CTkLabel(form_frame, text="Resultado del Procesamiento:")
        estado_label.pack(anchor="w", pady=(0, 5))
        
        estados_opciones = ["Finalizado", "Rechazado"]
        
        self.estado_combobox = ctk.CTkComboBox(
            form_frame,
            values=estados_opciones,
            width=490
        )
        self.estado_combobox.pack(fill="x", pady=(0, 15))
        
        # Nota informativa
        nota_frame = ctk.CTkFrame(form_frame, fg_color="#ffffff")
        nota_frame.pack(fill="x", pady=(0, 15))
        
        nota_label = ctk.CTkLabel(
            nota_frame,
            text="✅ Finalizado: La compra se completó y el stock se actualizará automáticamente\n"
                 "❌ Rechazado: La compra fue rechazada y no se actualizará el stock",
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
        
        process_button = ctk.CTkButton(
            button_frame,
            text="Procesar Orden",
            command=self.guardar,
            fg_color="#8B4513",
            hover_color="#654321"
        )
        process_button.pack(side="right")

    def guardar(self):
        """Guardar datos del formulario"""
        if not self.estado_combobox.get():
            messagebox.showwarning("Campo requerido", "Selecciona el resultado del procesamiento.")
            return
        
        self.resultado = {
            "estado": self.estado_combobox.get()
        }
        
        self.destroy()

    def cancelar(self):
        """Cancelar diálogo"""
        self.resultado = None
        self.destroy()