"""
Vista del módulo de Compras
"""

import customtkinter as ctk
from tkinter import messagebox
from views.base_view import BaseView
from services.proveedor_service import obtener_proveedores, insertar_proveedor, actualizar_proveedor, eliminar_proveedor
from services.orden_compra_service import obtener_ordenes_compra, actualizar_estado_orden_compra_con_stock
from services.materia_prima_service import obtener_materias

class ComprasView(BaseView):
    def __init__(self, parent):
        self.proveedor_seleccionado = None
        self.compra_seleccionada = None
        super().__init__(parent)
    
    def crear_vista(self):
        """Crear la vista del módulo de compras"""
        # Header
        self.crear_header("Módulo de Compras")
        
        # Información del módulo
        info_frame = ctk.CTkFrame(self.parent, fg_color="#8B4513")
        info_frame.pack(fill="x", padx=20, pady=(10, 0))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="🛒 Centro de Gestión de Compras",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        info_label.pack(pady=10)
        
        info_desc = ctk.CTkLabel(
            info_frame,
            text="Administra proveedores y procesa las órdenes de compra para reposición de materiales.",
            font=ctk.CTkFont(size=12),
            text_color="lightgray"
        )
        info_desc.pack(pady=(0, 10))
        
        # Pestañas
        self.tabs = ctk.CTkTabview(self.parent)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear pestañas
        self.tab_proveedores = self.tabs.add("Proveedores")
        self.tab_compras = self.tabs.add("Órdenes de Compra")
        
        # Configurar pestañas
        self.configurar_tab_proveedores()
        self.configurar_tab_compras()
    
    def configurar_tab_proveedores(self):
        """Configurar pestaña de proveedores"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.tab_proveedores)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Información de la pestaña
        info_frame = ctk.CTkFrame(main_frame, fg_color="#ffffff")
        info_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="👥 Gestión de Proveedores",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        info_label.pack(pady=10)
        
        info_desc = ctk.CTkLabel(
            info_frame,
            text="Administra la información de contacto y datos de todos los proveedores de materias primas.",
            font=ctk.CTkFont(size=12)
        )
        info_desc.pack(pady=(0, 10))
        
        # Botones de acción
        botones_config = [
            {
                "name": "agregar",
                "text": "Agregar Proveedor",
                "command": self.agregar_proveedor,
                "fg_color": "#1f538d",
                "hover_color": "#14375e"
            },
            {
                "name": "editar",
                "text": "Editar Proveedor",
                "command": self.editar_proveedor,
                "state": "disabled"
            },
            {
                "name": "eliminar",
                "text": "Eliminar Proveedor",
                "command": self.eliminar_proveedor,
                "state": "disabled",
                "fg_color": "red",
                "hover_color": "darkred"
            },
            {
                "name": "refrescar",
                "text": "Refrescar",
                "command": self.cargar_proveedores,
                "fg_color": "gray",
                "hover_color": "darkgray"
            }
        ]
        
        self.botones_proveedores_frame, self.botones_proveedores = self.crear_botones_accion(main_frame, botones_config)
        
        # Tabla
        columnas = ("ID", "Nombre", "Empresa", "Correo", "Teléfono", "Dirección")
        self.proveedores_table_frame, self.proveedores_table = self.crear_tabla_frame(main_frame, columnas)
        
        # Configurar columnas específicas
        self.proveedores_table.column("ID", anchor="center", width=60)
        self.proveedores_table.column("Nombre", anchor="w", width=150)
        self.proveedores_table.column("Empresa", anchor="w", width=180)
        self.proveedores_table.column("Correo", anchor="w", width=200)
        self.proveedores_table.column("Teléfono", anchor="center", width=120)
        self.proveedores_table.column("Dirección", anchor="w", width=250)
        
        for col in columnas:
            self.proveedores_table.heading(col, text=col)
        
        # Evento de selección
        self.proveedores_table.bind("<<TreeviewSelect>>", self.on_proveedor_select)
        
        # Cargar datos
        self.cargar_proveedores()
    
    def configurar_tab_compras(self):
        """Configurar pestaña de órdenes de compra"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.tab_compras)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Información de la pestaña
        info_frame = ctk.CTkFrame(main_frame, fg_color="#ffffff")
        info_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="📦 Procesamiento de Órdenes de Compra",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        info_label.pack(pady=10)
        
        info_desc = ctk.CTkLabel(
            info_frame,
            text="Procesa las órdenes de compra pendientes. Al finalizar una orden, el stock se actualizará automáticamente.",
            font=ctk.CTkFont(size=12)
        )
        info_desc.pack(pady=(0, 10))
        
        # Frame para filtros y botones
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        # Filtro por estado
        filter_label = ctk.CTkLabel(controls_frame, text="Filtrar por estado:")
        filter_label.pack(side="left", padx=(10, 5), pady=10)
        
        self.filtro_estado_compras = ctk.CTkComboBox(
            controls_frame,
            values=["Todos", "En espera", "Finalizado", "Rechazado"],
            command=self.filtrar_compras,
            width=150
        )
        self.filtro_estado_compras.set("Todos")
        self.filtro_estado_compras.pack(side="left", padx=5, pady=10)
        
        # Botones de acción
        button_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=10, pady=5)
        
        self.btn_procesar_compra = ctk.CTkButton(
            button_frame,
            text="Procesar Orden",
            command=self.procesar_compra,
            state="disabled",
            fg_color="#8B4513",
            hover_color="#654321"
        )
        self.btn_procesar_compra.pack(side="left", padx=5)
        
        self.btn_refrescar_compras = ctk.CTkButton(
            button_frame,
            text="Refrescar",
            command=self.cargar_compras,
            fg_color="gray",
            hover_color="darkgray"
        )
        self.btn_refrescar_compras.pack(side="left", padx=5)
        
        # Tabla
        columnas = ("ID", "Materia Prima", "Proveedor", "Cantidad", "Precio Unit.", "Total", "Fecha", "Estado")
        self.compras_table_frame, self.compras_table = self.crear_tabla_frame(main_frame, columnas)
        
        # Configurar columnas específicas
        self.compras_table.column("ID", anchor="center", width=60)
        self.compras_table.column("Materia Prima", anchor="w", width=180)
        self.compras_table.column("Proveedor", anchor="w", width=150)
        self.compras_table.column("Cantidad", anchor="center", width=80)
        self.compras_table.column("Precio Unit.", anchor="e", width=100)
        self.compras_table.column("Total", anchor="e", width=100)
        self.compras_table.column("Fecha", anchor="center", width=100)
        self.compras_table.column("Estado", anchor="center", width=100)
        
        for col in columnas:
            self.compras_table.heading(col, text=col)
        
        # Evento de selección
        self.compras_table.bind("<<TreeviewSelect>>", self.on_compra_select)
        
        # Cargar datos
        self.cargar_compras()
    
    def cargar_proveedores(self):
        """Cargar proveedores en la tabla"""
        # Limpiar tabla
        for row in self.proveedores_table.get_children():
            self.proveedores_table.delete(row)
        
        # Obtener proveedores
        proveedores = obtener_proveedores()
        
        # Insertar en la tabla
        for proveedor in proveedores:
            self.proveedores_table.insert("", "end", values=proveedor)
    
    def cargar_compras(self, filtro_estado=None):
        """Cargar órdenes de compra en la tabla"""
        # Limpiar tabla
        for row in self.compras_table.get_children():
            self.compras_table.delete(row)
        
        # Obtener órdenes, materias y proveedores
        ordenes = obtener_ordenes_compra(filtro_estado)
        materias = {m[0]: m[1] for m in obtener_materias()}
        proveedores = {p[0]: p[1] for p in obtener_proveedores()}
        
        # Insertar en la tabla
        for orden in ordenes:
            # Estructura: (ID, materia_id, proveedor_id, cantidad, precio_unitario, total, fecha, estado)
            orden_formateada = [
                orden[0],  # ID
                materias.get(orden[1], "Materia desconocida"),  # Materia nombre
                proveedores.get(orden[2], "Proveedor desconocido"),  # Proveedor nombre
                orden[3],  # Cantidad
                f"${orden[4]}",  # Precio unitario formateado
                f"${orden[5]}",  # Total formateado
                orden[6],  # Fecha
                orden[7]   # Estado
            ]
            
            self.compras_table.insert("", "end", values=orden_formateada)
    
    def filtrar_compras(self, estado_seleccionado):
        """Filtrar órdenes de compra por estado"""
        filtro = None if estado_seleccionado == "Todos" else estado_seleccionado
        self.cargar_compras(filtro)
    
    def on_proveedor_select(self, event):
        """Manejar selección de proveedor"""
        selected = self.proveedores_table.selection()
        if selected:
            self.proveedor_seleccionado = self.proveedores_table.item(selected[0], "values")
            self.botones_proveedores["editar"].configure(state="normal")
            self.botones_proveedores["eliminar"].configure(state="normal")
        else:
            self.proveedor_seleccionado = None
            self.botones_proveedores["editar"].configure(state="disabled")
            self.botones_proveedores["eliminar"].configure(state="disabled")
    
    def on_compra_select(self, event):
        """Manejar selección de orden de compra"""
        selected = self.compras_table.selection()
        if selected:
            self.compra_seleccionada = self.compras_table.item(selected[0], "values")
            # Solo habilitar procesar si el estado es "En espera"
            if self.compra_seleccionada[7] == "En espera":
                self.btn_procesar_compra.configure(state="normal")
            else:
                self.btn_procesar_compra.configure(state="disabled")
        else:
            self.compra_seleccionada = None
            self.btn_procesar_compra.configure(state="disabled")
    
    # Métodos para proveedores
    def agregar_proveedor(self):
        """Abrir ventana para agregar proveedor"""
        from components.dialogs_compras import ProveedorDialog
        
        dialog = ProveedorDialog(self.parent, "agregar")
        if dialog.resultado:
            if insertar_proveedor(
                dialog.resultado["nombre"],
                dialog.resultado["empresa"],
                dialog.resultado["correo"],
                dialog.resultado["telefono"],
                dialog.resultado["direccion"]
            ):
                self.cargar_proveedores()
                messagebox.showinfo("Éxito", f"Proveedor '{dialog.resultado['nombre']}' agregado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo agregar el proveedor.")
    
    def editar_proveedor(self):
        """Abrir ventana para editar proveedor"""
        if not self.proveedor_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un proveedor primero.")
            return
        
        from components.dialogs_compras import ProveedorDialog
        
        dialog = ProveedorDialog(self.parent, "editar", self.proveedor_seleccionado)
        if dialog.resultado:
            if actualizar_proveedor(
                self.proveedor_seleccionado[0],  # ID del proveedor
                dialog.resultado["nombre"],
                dialog.resultado["empresa"],
                dialog.resultado["correo"],
                dialog.resultado["telefono"],
                dialog.resultado["direccion"]
            ):
                self.cargar_proveedores()
                messagebox.showinfo("Éxito", f"Proveedor '{dialog.resultado['nombre']}' actualizado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el proveedor.")
    
    def eliminar_proveedor(self):
        """Eliminar proveedor seleccionado"""
        if not self.proveedor_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un proveedor primero.")
            return
        
        if messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar el proveedor '{self.proveedor_seleccionado[1]}'?\n\n"
            f"Empresa: {self.proveedor_seleccionado[2]}\n"
            f"Esta acción no se puede deshacer."
        ):
            if eliminar_proveedor(self.proveedor_seleccionado[0]):
                self.cargar_proveedores()
                messagebox.showinfo("Éxito", f"Proveedor '{self.proveedor_seleccionado[1]}' eliminado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el proveedor.")
    
    # Métodos para órdenes de compra
    def procesar_compra(self):
        """Procesar orden de compra"""
        if not self.compra_seleccionada:
            messagebox.showwarning("Advertencia", "Selecciona una orden de compra primero.")
            return
        
        if self.compra_seleccionada[7] != "En espera":
            messagebox.showwarning("No procesable", "Solo se pueden procesar órdenes en estado 'En espera'.")
            return
        
        from components.dialogs_compras import ProcesarCompraDialog
        
        dialog = ProcesarCompraDialog(self.parent, self.compra_seleccionada)
        if dialog.resultado:
            # Obtener datos originales de la orden para el stock
            ordenes_originales = obtener_ordenes_compra()
            orden_original = None
            for orden in ordenes_originales:
                if str(orden[0]) == str(self.compra_seleccionada[0]):
                    orden_original = orden
                    break
            
            if not orden_original:
                messagebox.showerror("Error", "No se pudo encontrar la orden original.")
                return
            
            # Actualizar estado y stock si es necesario
            if actualizar_estado_orden_compra_con_stock(
                self.compra_seleccionada[0],  # ID de la orden
                dialog.resultado["estado"],
                orden_original[1],  # materia_id
                orden_original[3] if dialog.resultado["estado"] == "Finalizado" else None  # cantidad para sumar
            ):
                self.cargar_compras()
                if dialog.resultado["estado"] == "Finalizado":
                    messagebox.showinfo(
                        "Éxito", 
                        f"Orden procesada correctamente.\n\n"
                        f"Estado: {dialog.resultado['estado']}\n"
                        f"Stock actualizado: +{orden_original[3]} unidades"
                    )
                else:
                    messagebox.showinfo("Éxito", f"Orden {dialog.resultado['estado'].lower()} correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo procesar la orden de compra.")