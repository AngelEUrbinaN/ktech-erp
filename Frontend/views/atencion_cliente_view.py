"""
Vista del módulo de Atención al Cliente
"""

import customtkinter as ctk
from tkinter import messagebox
from views.base_view import BaseView
from services.ticket_service import obtener_tickets, insertar_ticket, actualizar_estado_ticket
from services.cliente_service import obtener_clientes

class AtencionClienteView(BaseView):
    def __init__(self, parent):
        self.ticket_seleccionado = None
        super().__init__(parent)
    
    def crear_vista(self):
        """Crear la vista del módulo de atención al cliente"""
        # Header
        self.crear_header("Módulo de Atención al Cliente")
        
        # Información del módulo
        info_frame = ctk.CTkFrame(self.parent, fg_color="#4169E1")
        info_frame.pack(fill="x", padx=20, pady=(10, 0))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="🎧 Centro de Atención al Cliente",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        info_label.pack(pady=10)
        
        info_desc = ctk.CTkLabel(
            info_frame,
            text="Gestiona tickets de soporte, problemas de clientes y seguimiento de casos relacionados con ventas.",
            font=ctk.CTkFont(size=12),
            text_color="lightgray"
        )
        info_desc.pack(pady=(0, 10))
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Información de la sección
        section_info_frame = ctk.CTkFrame(main_frame, fg_color="#ffffff")
        section_info_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        section_info_label = ctk.CTkLabel(
            section_info_frame,
            text="🎫 Gestión de Tickets de Soporte",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        section_info_label.pack(pady=10)
        
        section_info_desc = ctk.CTkLabel(
            section_info_frame,
            text="Crea y gestiona tickets de soporte para resolver problemas de clientes relacionados con sus compras.",
            font=ctk.CTkFont(size=12)
        )
        section_info_desc.pack(pady=(0, 10))
        
        # Frame para filtros y botones
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        # Filtro por estado
        filter_label = ctk.CTkLabel(controls_frame, text="Filtrar por estado:")
        filter_label.pack(side="left", padx=(10, 5), pady=10)
        
        self.filtro_estado = ctk.CTkComboBox(
            controls_frame,
            values=["Todos", "Pendiente", "Abierto", "Cerrado"],
            command=self.filtrar_tickets,
            width=150
        )
        self.filtro_estado.set("Todos")
        self.filtro_estado.pack(side="left", padx=5, pady=10)
        
        # Botones de acción
        button_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=10, pady=5)
        
        self.btn_nuevo_ticket = ctk.CTkButton(
            button_frame,
            text="🎫 Nuevo Ticket",
            command=self.agregar_ticket,
            fg_color="#4169E1",
            hover_color="#1E90FF"
        )
        self.btn_nuevo_ticket.pack(side="left", padx=5)
        
        self.btn_actualizar_estado = ctk.CTkButton(
            button_frame,
            text="📝 Actualizar Estado",
            command=self.actualizar_estado_ticket,
            state="disabled",
            fg_color="#093809",
            hover_color="#042404"
        )
        self.btn_actualizar_estado.pack(side="left", padx=5)
        
        self.btn_refrescar = ctk.CTkButton(
            button_frame,
            text="🔄 Refrescar",
            command=self.cargar_tickets,
            fg_color="gray",
            hover_color="darkgray"
        )
        self.btn_refrescar.pack(side="left", padx=5)
        
        # Tabla de tickets
        columnas = ("ID", "Cliente", "Venta ID", "Fecha", "Descripción", "Estado")
        self.tickets_table_frame, self.tickets_table = self.crear_tabla_frame(main_frame, columnas)
        
        # Configurar columnas específicas
        self.tickets_table.column("ID", anchor="center", width=60)
        self.tickets_table.column("Cliente", anchor="w", width=180)
        self.tickets_table.column("Venta ID", anchor="center", width=80)
        self.tickets_table.column("Fecha", anchor="center", width=100)
        self.tickets_table.column("Descripción", anchor="w", width=300)
        self.tickets_table.column("Estado", anchor="center", width=100)
        
        for col in columnas:
            self.tickets_table.heading(col, text=col)
        
        # Evento de selección
        self.tickets_table.bind("<<TreeviewSelect>>", self.on_ticket_select)
        
        # Frame para estadísticas
        self.stats_frame = ctk.CTkFrame(main_frame, fg_color="#191970")
        self.stats_frame.pack(fill="x", padx=10, pady=(10, 10))
        
        stats_title = ctk.CTkLabel(
            self.stats_frame,
            text="📊 Estadísticas de Tickets",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        )
        stats_title.pack(pady=(10, 5))
        
        # Contenedor para las estadísticas
        stats_container = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
        stats_container.pack(fill="x", padx=20, pady=(0, 10))
        
        # Etiquetas de estadísticas
        self.total_tickets_label = ctk.CTkLabel(
            stats_container,
            text="Total: 0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="lightblue"
        )
        self.total_tickets_label.pack(side="left", padx=10)
        
        self.pendientes_label = ctk.CTkLabel(
            stats_container,
            text="Pendientes: 0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="orange"
        )
        self.pendientes_label.pack(side="left", padx=10)
        
        self.abiertos_label = ctk.CTkLabel(
            stats_container,
            text="Abiertos: 0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="yellow"
        )
        self.abiertos_label.pack(side="left", padx=10)
        
        self.cerrados_label = ctk.CTkLabel(
            stats_container,
            text="Cerrados: 0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="lightgreen"
        )
        self.cerrados_label.pack(side="right", padx=10)
        
        # Cargar datos
        self.cargar_tickets()
    
    def cargar_tickets(self, filtro_estado=None):
        """Cargar tickets en la tabla"""
        # Limpiar tabla
        for row in self.tickets_table.get_children():
            self.tickets_table.delete(row)
        
        # Obtener tickets
        tickets = obtener_tickets(filtro_estado)
        
        # Insertar en la tabla
        for ticket in tickets:
            self.tickets_table.insert("", "end", values=ticket)
        
        # Actualizar estadísticas
        self.actualizar_estadisticas()
    
    def actualizar_estadisticas(self):
        """Actualizar estadísticas de tickets"""
        todos_tickets = obtener_tickets()
        
        total = len(todos_tickets)
        pendientes = len([t for t in todos_tickets if t[5] == "Pendiente"])
        abiertos = len([t for t in todos_tickets if t[5] == "Abierto"])
        cerrados = len([t for t in todos_tickets if t[5] == "Cerrado"])
        
        self.total_tickets_label.configure(text=f"Total: {total}")
        self.pendientes_label.configure(text=f"Pendientes: {pendientes}")
        self.abiertos_label.configure(text=f"Abiertos: {abiertos}")
        self.cerrados_label.configure(text=f"Cerrados: {cerrados}")
    
    def filtrar_tickets(self, estado_seleccionado):
        """Filtrar tickets por estado"""
        filtro = None if estado_seleccionado == "Todos" else estado_seleccionado
        self.cargar_tickets(filtro)
    
    def on_ticket_select(self, event):
        """Manejar selección de ticket"""
        selected = self.tickets_table.selection()
        if selected:
            self.ticket_seleccionado = self.tickets_table.item(selected[0], "values")
            # Solo habilitar actualizar estado si no está cerrado
            if self.ticket_seleccionado[5] != "Cerrado":
                self.btn_actualizar_estado.configure(state="normal")
            else:
                self.btn_actualizar_estado.configure(state="disabled")
        else:
            self.ticket_seleccionado = None
            self.btn_actualizar_estado.configure(state="disabled")
    
    def agregar_ticket(self):
        """Abrir ventana para agregar ticket"""
        from components.dialogs_atencion_cliente import TicketDialog
        
        dialog = TicketDialog(self.parent)
        if dialog.resultado:
            if insertar_ticket(
                dialog.resultado["cliente_id"],
                dialog.resultado["venta_id"],
                dialog.resultado["descripcion"],
                dialog.resultado["fecha"],
                dialog.resultado["estado"]
            ):
                self.cargar_tickets()
                messagebox.showinfo("Éxito", "Ticket creado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo crear el ticket.")
    
    def actualizar_estado_ticket(self):
        """Actualizar estado del ticket seleccionado"""
        if not self.ticket_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un ticket primero.")
            return
        
        estado_actual = self.ticket_seleccionado[5]
        
        if estado_actual == "Cerrado":
            messagebox.showwarning("No editable", "Los tickets cerrados no se pueden modificar.")
            return
        
        from components.dialogs_atencion_cliente import ActualizarEstadoTicketDialog
        
        dialog = ActualizarEstadoTicketDialog(self.parent, self.ticket_seleccionado)
        if dialog.resultado:
            if actualizar_estado_ticket(
                self.ticket_seleccionado[0],  # ticket_id
                dialog.resultado["estado"]
            ):
                self.cargar_tickets()
                messagebox.showinfo("Éxito", f"Estado actualizado a '{dialog.resultado['estado']}'.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el estado del ticket.")