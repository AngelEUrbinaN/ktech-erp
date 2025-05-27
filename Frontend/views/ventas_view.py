"""
Vista del módulo de Ventas
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from views.base_view import BaseView
from services.cliente_service import obtener_clientes, insertar_cliente, buscar_cliente_por_email
from services.venta_service import obtener_ventas, registrar_venta, calcular_resumen_ventas
from services.producto_service import obtener_producto_por_nombre, obtener_producto_por_id, descontar_stock_producto

class VentasView(BaseView):
    def __init__(self, parent):
        self.cliente_seleccionado = None
        super().__init__(parent)
    
    def crear_vista(self):
        """Crear la vista del módulo de ventas"""
        # Header con botones de acción
        header_frame = self.crear_header("Módulo de Ventas")

        # Información del módulo
        info_frame = ctk.CTkFrame(self.parent, fg_color="#E5E5E5")
        info_frame.pack(fill="x", padx=20, pady=(10, 0))

        info_label = ctk.CTkLabel(
            info_frame,
            text="ℹ️ Módulo de Ventas",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="black"
        )
        info_label.pack(pady=10)
        
        info_desc = ctk.CTkLabel(
            info_frame,
            text="Administra la información de clientes y registra nuevas ventas. Supervisa las transacciones y el historial de ventas de la empresa.",
            font=ctk.CTkFont(size=12),
            text_color="black"
        )
        info_desc.pack(pady=(0, 10))
        
        # Botones de acción en la cabecera
        action_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        action_frame.pack(side="right", padx=10)
        
        self.search_button = ctk.CTkButton(
            action_frame,
            text="Buscar Cliente",
            command=self.buscar_cliente
        )
        self.search_button.pack(side="left", padx=5)
        
        self.add_client_button = ctk.CTkButton(
            action_frame,
            text="Agregar Cliente",
            command=self.agregar_cliente
        )
        self.add_client_button.pack(side="left", padx=5)
        
        self.new_sale_button = ctk.CTkButton(
            action_frame,
            text="Nueva Venta",
            state="disabled",
            command=self.nueva_venta
        )
        self.new_sale_button.pack(side="left", padx=5)
        
        # Pestañas
        self.tabs = ctk.CTkTabview(self.parent)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear pestañas
        self.tab_clientes = self.tabs.add("Clientes")
        self.tab_ventas = self.tabs.add("Ventas")
        
        # Configurar pestañas
        self.configurar_tab_clientes()
        self.configurar_tab_ventas()
        
        # Cargar datos iniciales
        self.cargar_clientes()
        self.cargar_ventas()
    
    def configurar_tab_clientes(self):
        """Configurar pestaña de clientes"""
        # Frame para la tabla de clientes
        self.clientes_table_frame, self.clientes_table = self.crear_tabla_frame(
            self.tab_clientes, 
            ("ID", "Nombre", "Email", "Teléfono", "Dirección")
        )
        
        # Configurar columnas específicas
        self.clientes_table.column("ID", anchor="center", width=80)
        self.clientes_table.column("Nombre", anchor="w", width=180)
        self.clientes_table.column("Email", anchor="w", width=200)
        self.clientes_table.column("Teléfono", anchor="center", width=120)
        self.clientes_table.column("Dirección", anchor="w", width=250)
        
        for col in ["ID", "Nombre", "Email", "Teléfono", "Dirección"]:
            self.clientes_table.heading(col, text=col)
        
        # Evento de selección
        self.clientes_table.bind("<<TreeviewSelect>>", self.on_cliente_select)
    
    def configurar_tab_ventas(self):
        """Configurar pestaña de ventas"""
        # Frame principal para ventas
        main_ventas_frame = ctk.CTkFrame(self.tab_ventas)
        main_ventas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tabla de ventas
        self.ventas_table_frame, self.ventas_table = self.crear_tabla_frame(
            main_ventas_frame,
            ("ID Venta", "Cliente", "Total", "Producto", "Cantidad", "Precio Unitario", "Estado"),
            height=10
        )
        
        # Configurar columnas específicas
        self.ventas_table.column("ID Venta", anchor="center", width=80)
        self.ventas_table.column("Cliente", anchor="w", width=150)
        self.ventas_table.column("Total", anchor="e", width=100)
        self.ventas_table.column("Producto", anchor="w", width=150)
        self.ventas_table.column("Cantidad", anchor="center", width=80)
        self.ventas_table.column("Precio Unitario", anchor="e", width=120)
        self.ventas_table.column("Estado", anchor="center", width=100)
        
        for col in ["ID Venta", "Cliente", "Total", "Producto", "Cantidad", "Precio Unitario", "Estado"]:
            self.ventas_table.heading(col, text=col)
        
        # Frame para el resumen
        self.resumen_frame = ctk.CTkFrame(main_ventas_frame)
        self.resumen_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Etiquetas de resumen
        self.total_ventas_label = ctk.CTkLabel(
            self.resumen_frame,
            text="Total de ventas: 0",
            font=ctk.CTkFont(weight="bold")
        )
        self.total_ventas_label.pack(side="left", padx=20, pady=10)
        
        self.monto_total_label = ctk.CTkLabel(
            self.resumen_frame,
            text="Monto total: $0.00",
            font=ctk.CTkFont(weight="bold")
        )
        self.monto_total_label.pack(side="right", padx=20, pady=10)
    
    def cargar_clientes(self):
        """Cargar clientes en la tabla"""
        # Limpiar tabla
        for row in self.clientes_table.get_children():
            self.clientes_table.delete(row)
        
        # Obtener clientes
        clientes = obtener_clientes()
        
        # Insertar en la tabla
        for cliente in clientes:
            self.clientes_table.insert("", "end", values=cliente)
    
    def cargar_ventas(self):
        """Cargar ventas en la tabla"""
        # Limpiar tabla
        for row in self.ventas_table.get_children():
            self.ventas_table.delete(row)
        
        # Obtener ventas
        ventas = obtener_ventas()
        
        # Insertar en la tabla
        for venta in ventas:
            # Formatear valores monetarios
            venta_formateada = list(venta)
            venta_formateada[2] = f"${venta[2]}"  # Total
            venta_formateada[5] = f"${venta[5]}"  # Precio unitario
            self.ventas_table.insert("", "end", values=venta_formateada)
        
        # Actualizar resumen
        total_ventas, monto_total = calcular_resumen_ventas()
        self.total_ventas_label.configure(text=f"Total de ventas: {total_ventas}")
        self.monto_total_label.configure(text=f"Monto total: ${monto_total}")
    
    def on_cliente_select(self, event):
        """Manejar selección de cliente"""
        selected = self.clientes_table.selection()
        if selected:
            self.cliente_seleccionado = self.clientes_table.item(selected[0], "values")
            self.new_sale_button.configure(state="normal")
        else:
            self.cliente_seleccionado = None
            self.new_sale_button.configure(state="disabled")
    
    def agregar_cliente(self):
        """Abrir ventana para agregar cliente"""
        from components.dialogs import ClienteDialog
        
        dialog = ClienteDialog(self.parent)
        if dialog.resultado:
            if insertar_cliente(
                dialog.resultado["nombre"],
                dialog.resultado["email"],
                dialog.resultado["telefono"],
                dialog.resultado["direccion"]
            ):
                self.cargar_clientes()
                messagebox.showinfo("Éxito", f"{dialog.resultado['nombre']} ha sido agregado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo agregar el cliente.")
    
    def buscar_cliente(self):
        """Buscar cliente por email"""
        from components.dialogs import BuscarClienteDialog
        
        dialog = BuscarClienteDialog(self.parent)
        if dialog.resultado:
            email = dialog.resultado["email"]
            cliente = buscar_cliente_por_email(email)
            
            if not cliente:
                messagebox.showinfo("No encontrado", "Cliente no encontrado.")
            else:
                # Resaltar en la tabla
                for row in self.clientes_table.get_children():
                    values = self.clientes_table.item(row)["values"]
                    if values[2] == email:  # columna del email
                        self.clientes_table.selection_set(row)
                        self.clientes_table.focus(row)
                        self.clientes_table.see(row)  # scroll automático
                        self.on_cliente_select(None)  # Actualizar selección
                        break
                
                # Cambiar a la pestaña de clientes
                self.tabs.set("Clientes")
    
    def nueva_venta(self):
        """Abrir ventana para nueva venta"""
        if not self.cliente_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un cliente primero.")
            return
        
        from components.dialogs import VentaDialog
        
        dialog = VentaDialog(self.parent, self.cliente_seleccionado)
        if dialog.resultado:
            # Verificar stock
            producto = obtener_producto_por_id(dialog.resultado["producto_id"])
            if producto and producto["stock_actual"] < dialog.resultado["cantidad"]:
                messagebox.showwarning(
                    "Stock insuficiente",
                    f"No hay suficiente stock. Disponible: {producto['stock_actual']} unidades."
                )
                return
            
            # Registrar venta
            if registrar_venta(
                dialog.resultado["cliente_id"],
                dialog.resultado["producto_id"],
                dialog.resultado["cantidad"],
                dialog.resultado["precio_unitario"]
            ):
                
                # Recargar tabla de ventas
                self.cargar_ventas()
                
                # Mostrar mensaje
                total = dialog.resultado["cantidad"] * dialog.resultado["precio_unitario"]
                messagebox.showinfo("Éxito", f"Venta por ${total} registrada correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo registrar la venta.")