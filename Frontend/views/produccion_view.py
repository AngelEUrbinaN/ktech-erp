"""
Vista del módulo de Producción
"""

import customtkinter as ctk
from tkinter import messagebox
from views.base_view import BaseView
from services.orden_produccion_service import obtener_ordenes_produccion, actualizar_estado_orden_produccion
from services.orden_materia_service import obtener_ordenes_materia, insertar_orden_materia, actualizar_estado_orden_materia
from services.producto_service import obtener_productos
from services.materia_prima_service import obtener_materias

class ProduccionView(BaseView):
    def __init__(self, parent):
        self.orden_produccion_seleccionada = None
        self.orden_materia_seleccionada = None
        super().__init__(parent)
    
    def crear_vista(self):
        """Crear la vista del módulo de producción"""
        # Header
        self.crear_header("Módulo de Producción")
        
        # Información del módulo
        info_frame = ctk.CTkFrame(self.parent, fg_color="#1a472a")
        info_frame.pack(fill="x", padx=20, pady=(10, 0))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="🏭 Centro de Control de Producción",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        info_label.pack(pady=10)
        
        info_desc = ctk.CTkLabel(
            info_frame,
            text="Gestiona las órdenes de producción y solicita materiales necesarios para la fabricación.",
            font=ctk.CTkFont(size=12),
            text_color="lightgray"
        )
        info_desc.pack(pady=(0, 10))
        
        # Pestañas
        self.tabs = ctk.CTkTabview(self.parent)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear pestañas
        self.tab_ordenes_produccion = self.tabs.add("Órdenes de Producción")
        self.tab_ordenes_materiales = self.tabs.add("Órdenes de Materiales")
        
        # Configurar pestañas
        self.configurar_tab_ordenes_produccion()
        self.configurar_tab_ordenes_materiales()
    
    def configurar_tab_ordenes_produccion(self):
        """Configurar pestaña de órdenes de producción"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.tab_ordenes_produccion)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Información de la pestaña
        info_frame = ctk.CTkFrame(main_frame, fg_color="#ffffff")
        info_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="📋 Control de Órdenes de Producción",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        info_label.pack(pady=10)
        
        info_desc = ctk.CTkLabel(
            info_frame,
            text="Supervisa y actualiza el estado de las órdenes de producción. Solo puedes finalizar o rechazar órdenes en espera.",
            font=ctk.CTkFont(size=12)
        )
        info_desc.pack(pady=(0, 10))
        
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
        button_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=10, pady=5)
        
        self.btn_editar_produccion = ctk.CTkButton(
            button_frame,
            text="Actualizar Estado",
            command=self.editar_orden_produccion,
            state="disabled"
        )
        self.btn_editar_produccion.pack(side="left", padx=5)
        
        self.btn_refrescar_produccion = ctk.CTkButton(
            button_frame,
            text="Refrescar",
            command=self.cargar_ordenes_produccion,
            fg_color="gray",
            hover_color="darkgray"
        )
        self.btn_refrescar_produccion.pack(side="left", padx=5)
        
        # Tabla
        columnas = ("ID", "Producto", "Cantidad", "Fecha Inicio", "Fecha Fin Est.", "Estado")
        self.ordenes_prod_table_frame, self.ordenes_prod_table = self.crear_tabla_frame(main_frame, columnas)
        
        # Configurar columnas específicas
        self.ordenes_prod_table.column("ID", anchor="center", width=60)
        self.ordenes_prod_table.column("Producto", anchor="w", width=200)
        self.ordenes_prod_table.column("Cantidad", anchor="center", width=100)
        self.ordenes_prod_table.column("Fecha Inicio", anchor="center", width=120)
        self.ordenes_prod_table.column("Fecha Fin Est.", anchor="center", width=120)
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
        
        # Información de la pestaña
        info_frame = ctk.CTkFrame(main_frame, fg_color="#ffffff")
        info_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="📦 Solicitudes de Materiales",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        info_label.pack(pady=10)
        
        info_desc = ctk.CTkLabel(
            info_frame,
            text="Crea nuevas solicitudes de materiales y cancela órdenes en espera si es necesario.",
            font=ctk.CTkFont(size=12)
        )
        info_desc.pack(pady=(0, 10))
        
        # Botones de acción
        botones_config = [
            {
                "name": "agregar",
                "text": "Nueva Solicitud de Material",
                "command": self.agregar_orden_materia,
                "fg_color": "#1f538d",
                "hover_color": "#14375e"
            },
            {
                "name": "editar",
                "text": "Cancelar Orden",
                "command": self.editar_orden_materia,
                "state": "disabled",
                "fg_color": "red",
                "hover_color": "darkred"
            },
            {
                "name": "refrescar",
                "text": "Refrescar",
                "command": self.cargar_ordenes_materiales,
                "fg_color": "gray",
                "hover_color": "darkgray"
            }
        ]
        
        self.botones_ordenes_mat_frame, self.botones_ordenes_mat = self.crear_botones_accion(main_frame, botones_config)
        
        # Tabla
        columnas = ("ID", "Materia Prima", "Cantidad", "Fecha Solicitud", "Estado")
        self.ordenes_mat_table_frame, self.ordenes_mat_table = self.crear_tabla_frame(main_frame, columnas)
        
        # Configurar columnas específicas
        self.ordenes_mat_table.column("ID", anchor="center", width=80)
        self.ordenes_mat_table.column("Materia Prima", anchor="w", width=250)
        self.ordenes_mat_table.column("Cantidad", anchor="center", width=120)
        self.ordenes_mat_table.column("Fecha Solicitud", anchor="center", width=150)
        self.ordenes_mat_table.column("Estado", anchor="center", width=150)
        
        for col in columnas:
            self.ordenes_mat_table.heading(col, text=col)
        
        # Evento de selección
        self.ordenes_mat_table.bind("<<TreeviewSelect>>", self.on_orden_materia_select)
        
        # Cargar datos
        self.cargar_ordenes_materiales()
    
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
    
    def filtrar_ordenes_produccion(self, estado_seleccionado):
        """Filtrar órdenes de producción por estado"""
        filtro = None if estado_seleccionado == "Todos" else estado_seleccionado
        self.cargar_ordenes_produccion(filtro)
    
    def on_orden_produccion_select(self, event):
        """Manejar selección de orden de producción"""
        selected = self.ordenes_prod_table.selection()
        if selected:
            self.orden_produccion_seleccionada = self.ordenes_prod_table.item(selected[0], "values")
            # Solo habilitar editar si el estado es "En espera"
            if self.orden_produccion_seleccionada[5] == "En espera":
                self.btn_editar_produccion.configure(state="normal")
            else:
                self.btn_editar_produccion.configure(state="disabled")
        else:
            self.orden_produccion_seleccionada = None
            self.btn_editar_produccion.configure(state="disabled")
    
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
    
    def editar_orden_produccion(self):
        """Editar estado de orden de producción"""
        if not self.orden_produccion_seleccionada:
            messagebox.showwarning("Advertencia", "Selecciona una orden de producción primero.")
            return
        
        if self.orden_produccion_seleccionada[5] != "En espera":
            messagebox.showwarning("No editable", "Solo se pueden editar órdenes en estado 'En espera'.")
            return
        
        from components.dialogs_produccion import EditarEstadoProduccionDialog
        
        dialog = EditarEstadoProduccionDialog(self.parent, self.orden_produccion_seleccionada)
        if dialog.resultado:
            if actualizar_estado_orden_produccion(
                self.orden_produccion_seleccionada[0],
                dialog.resultado["estado"]
            ):
                self.cargar_ordenes_produccion()
                messagebox.showinfo("Éxito", "Estado de la orden actualizado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el estado de la orden.")
    
    def agregar_orden_materia(self):
        """Abrir ventana para agregar orden de materiales"""
        from components.dialogs_produccion import OrdenMateriaDialog
        
        dialog = OrdenMateriaDialog(self.parent)
        if dialog.resultado:
            if insertar_orden_materia(
                dialog.resultado["materia_id"],
                dialog.resultado["cantidad"],
                dialog.resultado["fecha"],
                dialog.resultado["estado"]
            ):
                self.cargar_ordenes_materiales()
                messagebox.showinfo("Éxito", "Solicitud de material creada correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo crear la solicitud de material.")
    
    def editar_orden_materia(self):
        """Cancelar orden de materiales"""
        if not self.orden_materia_seleccionada:
            messagebox.showwarning("Advertencia", "Selecciona una orden de materiales primero.")
            return
        
        if self.orden_materia_seleccionada[4] != "En espera":
            messagebox.showwarning("No editable", "Solo se pueden cancelar órdenes en estado 'En espera'.")
            return
        
        # Confirmar cancelación
        if messagebox.askyesno(
            "Confirmar cancelación",
            f"¿Cancelar la solicitud de material '{self.orden_materia_seleccionada[1]}'?\n\n"
            f"Cantidad: {self.orden_materia_seleccionada[2]}\n"
            f"Fecha: {self.orden_materia_seleccionada[3]}\n\n"
            "Esta acción no se puede deshacer."
        ):
            if actualizar_estado_orden_materia(
                self.orden_materia_seleccionada[0],
                "Cancelado",
                None  # No descontar cantidad al cancelar
            ):
                self.cargar_ordenes_materiales()
                messagebox.showinfo("Éxito", "Orden de material cancelada correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo cancelar la orden de material.")