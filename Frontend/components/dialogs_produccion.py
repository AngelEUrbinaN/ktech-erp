"""
Diálogos específicos para el módulo de Producción
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import date, datetime, timedelta
from components.dialogs import BaseDialog

class EditarEstadoProduccionDialog(BaseDialog):
    def __init__(self, parent, orden_datos):
        self.orden_datos = orden_datos
        super().__init__(parent, "Actualizar Estado - Orden de Producción", "500x450")

    def crear_interfaz(self):
        """Crear interfaz del diálogo de editar estado de orden de producción"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="Actualizar Estado de Producción",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Información de la orden
        info_frame = ctk.CTkFrame(self, fg_color="#1a472a")
        info_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        info_title = ctk.CTkLabel(
            info_frame,
            text="Información de la Orden",
            font=ctk.CTkFont(weight="bold"),
            text_color="white"
        )
        info_title.pack(pady=(10, 5))
        
        info_text = f"ID: {self.orden_datos[0]} | Producto: {self.orden_datos[1]}\n"
        info_text += f"Cantidad: {self.orden_datos[2]} | Fecha Inicio: {self.orden_datos[3]}\n"
        info_text += f"Fecha Fin Est.: {self.orden_datos[4]} | Estado actual: {self.orden_datos[5]}"
        
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
        estado_label = ctk.CTkLabel(form_frame, text="Nuevo Estado:")
        estado_label.pack(anchor="w", pady=(0, 5))
        
        estados_opciones = ["Finalizado", "Rechazado"]
        
        self.estado_combobox = ctk.CTkComboBox(
            form_frame,
            values=estados_opciones,
            width=440
        )
        self.estado_combobox.pack(fill="x", pady=(0, 15))
        
        # Nota informativa
        nota_frame = ctk.CTkFrame(form_frame, fg_color="#ffffff")
        nota_frame.pack(fill="x", pady=(0, 15))
        
        nota_label = ctk.CTkLabel(
            nota_frame,
            text="ℹ️ Finalizado: La orden se completó exitosamente\n"
                 "🚫 Rechazado: La orden fue rechazada y no se completará",
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

class OrdenMateriaDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent, "Nueva Solicitud de Material", "500x550")

    def crear_interfaz(self):
        """Crear interfaz del diálogo de orden de material"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="Nueva Solicitud de Material",
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
        
        # Cantidad
        cantidad_label = ctk.CTkLabel(parent, text="Cantidad Solicitada:")
        cantidad_label.pack(anchor="w", pady=(0, 5))
        self.cantidad_entry = ctk.CTkEntry(parent, placeholder_text="Cantidad necesaria", width=440)
        self.cantidad_entry.pack(fill="x", pady=(0, 15))
        
        # Fecha (automática)
        fecha_label = ctk.CTkLabel(parent, text="Fecha de Solicitud:")
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
        
        # Nota informativa
        nota_frame = ctk.CTkFrame(parent, fg_color="#ffffff")
        nota_frame.pack(fill="x", pady=(0, 15))
        
        nota_label = ctk.CTkLabel(
            nota_frame,
            text="📋 Esta solicitud será enviada al departamento de inventario para su procesamiento.",
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
        
        create_button = ctk.CTkButton(
            button_frame,
            text="Crear Solicitud",
            command=self.guardar,
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        create_button.pack(side="right")

    def guardar(self):
        """Guardar datos del formulario"""
        # Validar campos
        if not self.materia_combobox.get() or not self.cantidad_entry.get():
            messagebox.showwarning("Campos requeridos", "Todos los campos son obligatorios.")
            return
        
        try:
            cantidad = int(self.cantidad_entry.get())
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")
        except ValueError:
            messagebox.showwarning("Valor inválido", "La cantidad debe ser un número entero mayor a 0.")
            return
        
        # Extraer ID de la materia prima
        materia_seleccionada = self.materia_combobox.get()
        materia_id = int(materia_seleccionada.split(" - ")[0])
        
        # Guardar resultado
        self.resultado = {
            "materia_id": materia_id,
            "cantidad": cantidad,
            "fecha": date.today().strftime("%Y-%m-%d"),
            "estado": "En espera"
        }
        
        self.destroy()

    def cancelar(self):
        """Cancelar diálogo"""
        self.resultado = None
        self.destroy()