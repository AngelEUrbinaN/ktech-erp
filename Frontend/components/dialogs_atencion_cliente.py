"""
Diálogos específicos para el módulo de Atención al Cliente
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from components.dialogs import BaseDialog
from services.cliente_service import obtener_clientes_para_combobox
from services.venta_service import obtener_venta_por_id

class TicketDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent, "Nuevo Ticket de Soporte", "600x700")

    def crear_interfaz(self):
        """Crear interfaz del diálogo de ticket"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="Nuevo Ticket de Soporte",
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
        # Cliente
        cliente_label = ctk.CTkLabel(parent, text="Cliente:")
        cliente_label.pack(anchor="w", pady=(0, 5))
        
        clientes_opciones = obtener_clientes_para_combobox()
        self.cliente_combobox = ctk.CTkComboBox(
            parent,
            values=clientes_opciones,
            width=540,
            command=self.on_cliente_change
        )
        self.cliente_combobox.pack(fill="x", pady=(0, 15))
        
        # ID de Venta
        venta_label = ctk.CTkLabel(parent, text="ID de Venta:")
        venta_label.pack(anchor="w", pady=(0, 5))
        
        venta_frame = ctk.CTkFrame(parent, fg_color="transparent")
        venta_frame.pack(fill="x", pady=(0, 15))
        
        self.venta_entry = ctk.CTkEntry(
            venta_frame, 
            placeholder_text="Ingresa el ID de la venta",
            width=440
        )
        self.venta_entry.pack(side="left", fill="x", expand=True)
        
        self.validar_button = ctk.CTkButton(
            venta_frame,
            text="Validar",
            command=self.validar_venta,
            width=80,
            fg_color="#4169E1",
            hover_color="#1E90FF"
        )
        self.validar_button.pack(side="right", padx=(10, 0))
        
        # Información de la venta
        self.venta_info_frame = ctk.CTkFrame(parent, fg_color="#ffffff")
        self.venta_info_frame.pack(fill="x", pady=(0, 15))
        
        self.venta_info_label = ctk.CTkLabel(
            self.venta_info_frame,
            text="ℹ️ Ingresa un ID de venta y haz clic en 'Validar' para verificar la información.",
            font=ctk.CTkFont(size=12)
        )
        self.venta_info_label.pack(pady=10)
        
        # Descripción del problema
        descripcion_label = ctk.CTkLabel(parent, text="Descripción del Problema:")
        descripcion_label.pack(anchor="w", pady=(0, 5))
        
        self.descripcion_textbox = ctk.CTkTextbox(
            parent,
            height=120,
            width=540,
            wrap="word"
        )
        self.descripcion_textbox.pack(fill="x", pady=(0, 15))
        
        # Fecha (automática)
        fecha_label = ctk.CTkLabel(parent, text="Fecha:")
        fecha_label.pack(anchor="w", pady=(0, 5))
        self.fecha_entry = ctk.CTkEntry(parent, width=540)
        self.fecha_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.fecha_entry.configure(state="disabled")
        self.fecha_entry.pack(fill="x", pady=(0, 15))
        
        # Estado (automático)
        estado_label = ctk.CTkLabel(parent, text="Estado:")
        estado_label.pack(anchor="w", pady=(0, 5))
        self.estado_entry = ctk.CTkEntry(parent, width=540)
        self.estado_entry.insert(0, "Pendiente")
        self.estado_entry.configure(state="disabled")
        self.estado_entry.pack(fill="x", pady=(0, 15))

    def on_cliente_change(self, value):
        """Limpiar información de venta cuando cambia el cliente"""
        self.venta_entry.delete(0, "end")
        self.venta_info_label.configure(
            text="ℹ️ Ingresa un ID de venta y haz clic en 'Validar' para verificar la información."
        )
        self.venta_info_frame.configure(fg_color="#ffffff")

    def validar_venta(self):
        """Validar que la venta pertenezca al cliente seleccionado"""
        if not self.cliente_combobox.get():
            messagebox.showwarning("Cliente requerido", "Selecciona un cliente primero.")
            return
        
        if not self.venta_entry.get():
            messagebox.showwarning("ID requerido", "Ingresa el ID de la venta.")
            return
        
        try:
            venta_id = int(self.venta_entry.get())
        except ValueError:
            messagebox.showwarning("ID inválido", "El ID de venta debe ser un número.")
            return
        
        # Extraer ID del cliente seleccionado
        cliente_seleccionado = self.cliente_combobox.get()
        cliente_id = int(cliente_seleccionado.split(" - ")[0])
        
        # Obtener información de la venta
        venta = obtener_venta_por_id(venta_id)
        
        if not venta:
            self.venta_info_label.configure(text="❌ Venta no encontrada.")
            self.venta_info_frame.configure(fg_color="#8B0000")
            return
        
        # Verificar que la venta pertenezca al cliente
        if venta[1] != cliente_id:
            self.venta_info_label.configure(
                text="❌ Esta venta no pertenece al cliente seleccionado."
            )
            self.venta_info_frame.configure(fg_color="#8B0000")
            return
        
        # Mostrar información de la venta
        info_text = f"✅ Venta válida - Producto: {venta[3]} | Cantidad: {venta[4]} | Total: ${venta[2]} | Estado: {venta[6]}"
        self.venta_info_label.configure(text=info_text)
        self.venta_info_frame.configure(fg_color="#006400")

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
            text="Crear Ticket",
            command=self.guardar,
            fg_color="#4169E1",
            hover_color="#1E90FF"
        )
        create_button.pack(side="right")

    def guardar(self):
        """Guardar datos del formulario"""
        # Validar campos
        if not self.cliente_combobox.get():
            messagebox.showwarning("Campo requerido", "Selecciona un cliente.")
            return
        
        if not self.venta_entry.get():
            messagebox.showwarning("Campo requerido", "Ingresa el ID de la venta.")
            return
        
        descripcion = self.descripcion_textbox.get("1.0", "end-1c").strip()
        if not descripcion:
            messagebox.showwarning("Campo requerido", "Describe el problema.")
            return
        
        # Validar venta una vez más
        try:
            venta_id = int(self.venta_entry.get())
        except ValueError:
            messagebox.showwarning("ID inválido", "El ID de venta debe ser un número.")
            return
        
        cliente_seleccionado = self.cliente_combobox.get()
        cliente_id = int(cliente_seleccionado.split(" - ")[0])
        
        venta = obtener_venta_por_id(venta_id)
        if not venta or venta[1] != cliente_id:
            messagebox.showwarning("Venta inválida", "Valida la venta antes de continuar.")
            return
        
        # Guardar resultado
        self.resultado = {
            "cliente_id": cliente_id,
            "venta_id": venta_id,
            "descripcion": descripcion,
            "fecha": date.today().strftime("%Y-%m-%d"),
            "estado": "Pendiente"
        }
        
        self.destroy()

    def cancelar(self):
        """Cancelar diálogo"""
        self.resultado = None
        self.destroy()

class ActualizarEstadoTicketDialog(BaseDialog):
    def __init__(self, parent, ticket_datos):
        self.ticket_datos = ticket_datos
        super().__init__(parent, "Actualizar Estado del Ticket", "500x350")

    def crear_interfaz(self):
        """Crear interfaz del diálogo de actualizar estado"""
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="Actualizar Estado del Ticket",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Información del ticket
        info_frame = ctk.CTkFrame(self, fg_color="#4169E1")
        info_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        info_title = ctk.CTkLabel(
            info_frame,
            text="Información del Ticket",
            font=ctk.CTkFont(weight="bold"),
            text_color="white"
        )
        info_title.pack(pady=(10, 5))
        
        info_text = f"ID: {self.ticket_datos[0]} | Cliente: {self.ticket_datos[1]}\n"
        info_text += f"Venta ID: {self.ticket_datos[2]} | Fecha: {self.ticket_datos[3]}\n"
        info_text += f"Estado actual: {self.ticket_datos[5]}"
        
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
        
        # Determinar siguiente estado
        estado_actual = self.ticket_datos[5]
        if estado_actual == "Pendiente":
            siguiente_estado = "Abierto"
        elif estado_actual == "Abierto":
            siguiente_estado = "Cerrado"
        else:
            siguiente_estado = None
        
        if siguiente_estado:
            self.estado_combobox = ctk.CTkComboBox(
                form_frame,
                values=[siguiente_estado],
                width=440
            )
            self.estado_combobox.set(siguiente_estado)
        else:
            self.estado_combobox = ctk.CTkComboBox(
                form_frame,
                values=["No disponible"],
                width=440,
                state="disabled"
            )
        
        self.estado_combobox.pack(fill="x", pady=(0, 15))
        
        # Tarjeta
        nota_frame = ctk.CTkFrame(form_frame, fg_color="#ffffff")
        nota_frame.pack(fill="x", pady=(0, 15))
        
        if siguiente_estado:
            nota_text = f"📋 El ticket pasará de '{estado_actual}' a '{siguiente_estado}'"
        else:
            nota_text = "🔒 Este ticket ya está cerrado y no se puede modificar"
        
        nota_label = ctk.CTkLabel(
            nota_frame,
            text=nota_text,
            font=ctk.CTkFont(size=12)
        )
        nota_label.pack(pady=10)
        
        # Botones
        self.crear_botones(siguiente_estado is not None)

    def crear_botones(self, puede_actualizar):
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
        
        if puede_actualizar:
            update_button = ctk.CTkButton(
                button_frame,
                text="Actualizar Estado",
                command=self.guardar,
                fg_color="#32CD32",
                hover_color="#228B22"
            )
            update_button.pack(side="right")

    def guardar(self):
        """Guardar datos del formulario"""
        if not self.estado_combobox.get() or self.estado_combobox.get() == "No disponible":
            messagebox.showwarning("Estado no válido", "No se puede actualizar el estado.")
            return
        
        self.resultado = {
            "estado": self.estado_combobox.get()
        }
        
        self.destroy()

    def cancelar(self):
        """Cancelar diálogo"""
        self.resultado = None
        self.destroy()