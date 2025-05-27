"""
Vista del módulo de Finanzas - ACTUALIZADA
"""

import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from views.base_view import BaseView
from services.departamento_service import obtener_departamentos, insertar_departamento
from services.finanzas_service import obtener_ingresos_finalizados, obtener_egresos_finalizados, calcular_resumen_ingresos, calcular_resumen_egresos

class FinanzasView(BaseView):
    def __init__(self, parent):
        self.departamento_seleccionado = None
        super().__init__(parent)
    
    def crear_vista(self):
        """Crear la vista del módulo de finanzas"""
        # Header
        self.crear_header("Módulo de Finanzas")
        
        # Información del módulo
        info_frame = ctk.CTkFrame(self.parent, fg_color="#2E8B57")
        info_frame.pack(fill="x", padx=20, pady=(10, 0))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="💰 Centro de Control Financiero",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        )
        info_label.pack(pady=10)
        
        info_desc = ctk.CTkLabel(
            info_frame,
            text="Monitorea ingresos por ventas, egresos por compras y gestiona departamentos con sus presupuestos.",
            font=ctk.CTkFont(size=12),
            text_color="lightgray"
        )
        info_desc.pack(pady=(0, 10))
        
        # Pestañas
        self.tabs = ctk.CTkTabview(self.parent)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear pestañas
        self.tab_ingresos = self.tabs.add("Ingresos")
        self.tab_egresos = self.tabs.add("Egresos")
        self.tab_departamentos = self.tabs.add("Departamentos")
        
        # Configurar pestañas
        self.configurar_tab_ingresos()
        self.configurar_tab_egresos()
        self.configurar_tab_departamentos()
    
    def configurar_tab_ingresos(self):
        """Configurar pestaña de ingresos"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.tab_ingresos)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Información de la pestaña
        info_frame = ctk.CTkFrame(main_frame, fg_color="#ffffff")
        info_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="📈 Ingresos por Ventas Finalizadas",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        info_label.pack(pady=10)
        
        info_desc = ctk.CTkLabel(
            info_frame,
            text="Visualiza todos los ingresos generados por ventas completadas exitosamente.",
            font=ctk.CTkFont(size=12)
        )
        info_desc.pack(pady=(0, 10))
        
        # Botón de refrescar
        refresh_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        refresh_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        self.btn_refrescar_ingresos = ctk.CTkButton(
            refresh_frame,
            text="🔄 Refrescar Datos",
            command=self.cargar_ingresos,
            fg_color="#2E8B57",
            hover_color="#228B22"
        )
        self.btn_refrescar_ingresos.pack(side="right", padx=10, pady=5)
        
        # Tabla de ingresos
        columnas = ("ID", "Producto", "Cantidad", "Total")
        self.ingresos_table_frame, self.ingresos_table = self.crear_tabla_frame(main_frame, columnas)
        
        # Configurar columnas específicas
        self.ingresos_table.column("ID", anchor="center", width=80)
        self.ingresos_table.column("Producto", anchor="w", width=250)
        self.ingresos_table.column("Cantidad", anchor="center", width=120)
        self.ingresos_table.column("Total", anchor="e", width=150)
        
        for col in columnas:
            self.ingresos_table.heading(col, text=col)
        
        # Frame para el resumen de ingresos
        self.resumen_ingresos_frame = ctk.CTkFrame(main_frame, fg_color="#1a472a")
        self.resumen_ingresos_frame.pack(fill="x", padx=10, pady=(10, 10))
        
        resumen_title = ctk.CTkLabel(
            self.resumen_ingresos_frame,
            text="📊 Resumen de Ingresos",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        )
        resumen_title.pack(pady=(10, 5))
        
        # Etiquetas de resumen
        self.total_ingresos_label = ctk.CTkLabel(
            self.resumen_ingresos_frame,
            text="Total de ventas: 0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="lightgreen"
        )
        self.total_ingresos_label.pack(side="left", padx=20, pady=10)
        
        self.monto_ingresos_label = ctk.CTkLabel(
            self.resumen_ingresos_frame,
            text="Monto total: $0.00",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="lightgreen"
        )
        self.monto_ingresos_label.pack(side="right", padx=20, pady=10)
        
        # Cargar datos
        self.cargar_ingresos()
    
    def configurar_tab_egresos(self):
        """Configurar pestaña de egresos"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.tab_egresos)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Información de la pestaña
        info_frame = ctk.CTkFrame(main_frame, fg_color="#ffffff")
        info_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="📉 Egresos por Compras Finalizadas",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        info_label.pack(pady=10)
        
        info_desc = ctk.CTkLabel(
            info_frame,
            text="Monitorea todos los gastos realizados en compras de materias primas completadas.",
            font=ctk.CTkFont(size=12)
        )
        info_desc.pack(pady=(0, 10))
        
        # Botones de acción
        controls_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        controls_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        self.btn_refrescar_egresos = ctk.CTkButton(
            controls_frame,
            text="🔄 Refrescar Datos",
            command=self.cargar_egresos,
            fg_color="#8B4513",
            hover_color="#654321"
        )
        self.btn_refrescar_egresos.pack(side="left", padx=5, pady=5)
        
        self.btn_grafica_egresos = ctk.CTkButton(
            controls_frame,
            text="📊 Ver Gráfica",
            command=self.mostrar_grafica_egresos,
            fg_color="#4682B4",
            hover_color="#2F4F4F"
        )
        self.btn_grafica_egresos.pack(side="right", padx=5, pady=5)
        
        # Tabla de egresos
        columnas = ("ID", "Materia Prima", "Cantidad", "Total", "Fecha")
        self.egresos_table_frame, self.egresos_table = self.crear_tabla_frame(main_frame, columnas)
        
        # Configurar columnas específicas
        self.egresos_table.column("ID", anchor="center", width=80)
        self.egresos_table.column("Materia Prima", anchor="w", width=200)
        self.egresos_table.column("Cantidad", anchor="center", width=100)
        self.egresos_table.column("Total", anchor="e", width=120)
        self.egresos_table.column("Fecha", anchor="center", width=120)
        
        for col in columnas:
            self.egresos_table.heading(col, text=col)
        
        # Frame para el resumen de egresos
        self.resumen_egresos_frame = ctk.CTkFrame(main_frame, fg_color="#8B4513")
        self.resumen_egresos_frame.pack(fill="x", padx=10, pady=(10, 10))
        
        resumen_title = ctk.CTkLabel(
            self.resumen_egresos_frame,
            text="📊 Resumen de Egresos",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        )
        resumen_title.pack(pady=(10, 5))
        
        # Etiquetas de resumen
        self.total_egresos_label = ctk.CTkLabel(
            self.resumen_egresos_frame,
            text="Total de compras: 0",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="lightyellow"
        )
        self.total_egresos_label.pack(side="left", padx=20, pady=10)
        
        self.monto_egresos_label = ctk.CTkLabel(
            self.resumen_egresos_frame,
            text="Monto total: $0.00",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="lightyellow"
        )
        self.monto_egresos_label.pack(side="right", padx=20, pady=10)
        
        # Cargar datos
        self.cargar_egresos()
    
    def configurar_tab_departamentos(self):
        """Configurar pestaña de departamentos"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.tab_departamentos)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Información de la pestaña
        info_frame = ctk.CTkFrame(main_frame, fg_color="#ffffff")
        info_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="🏢 Gestión de Departamentos",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        info_label.pack(pady=10)
        
        info_desc = ctk.CTkLabel(
            info_frame,
            text="Administra los departamentos de la empresa y sus presupuestos asignados.",
            font=ctk.CTkFont(size=12)
        )
        info_desc.pack(pady=(0, 10))
        
        # Botones de acción
        botones_config = [
            {
                "name": "agregar",
                "text": "Agregar Departamento",
                "command": self.agregar_departamento,
                "fg_color": "#2E8B57",
                "hover_color": "#228B22"
            },
            {
                "name": "editar",
                "text": "Editar Departamento",
                "command": self.editar_departamento,
                "state": "disabled"
            },
            {
                "name": "eliminar",
                "text": "Eliminar Departamento",
                "command": self.eliminar_departamento,
                "state": "disabled",
                "fg_color": "red",
                "hover_color": "darkred"
            }
        ]
        
        self.botones_frame, self.botones = self.crear_botones_accion(main_frame, botones_config)
        
        # Tabla
        columnas = ("ID", "Nombre", "Presupuesto", "Descripción")
        self.table_frame, self.departamentos_table = self.crear_tabla_frame(main_frame, columnas)
        
        # Configurar columnas específicas
        self.departamentos_table.column("ID", anchor="center", width=80)
        self.departamentos_table.column("Nombre", anchor="w", width=150)
        self.departamentos_table.column("Presupuesto", anchor="e", width=120)
        self.departamentos_table.column("Descripción", anchor="w", width=300)
        
        for col in columnas:
            self.departamentos_table.heading(col, text=col)
        
        # Evento de selección
        self.departamentos_table.bind("<<TreeviewSelect>>", self.on_departamento_select)
        
        # Cargar datos
        self.cargar_departamentos()
    
    def cargar_ingresos(self):
        """Cargar ingresos en la tabla"""
        # Limpiar tabla
        for row in self.ingresos_table.get_children():
            self.ingresos_table.delete(row)
        
        # Obtener ingresos
        ingresos = obtener_ingresos_finalizados()
        
        # Insertar en la tabla
        for ingreso in ingresos:
            # Formatear total
            ingreso_formateado = list(ingreso)
            ingreso_formateado[3] = f"${ingreso[3]}"
            
            self.ingresos_table.insert("", "end", values=ingreso_formateado)
        
        # Actualizar resumen
        total_ventas, monto_total = calcular_resumen_ingresos()
        self.total_ingresos_label.configure(text=f"Total de ventas: {total_ventas}")
        self.monto_ingresos_label.configure(text=f"Monto total: ${monto_total}")
    
    def cargar_egresos(self):
        """Cargar egresos en la tabla"""
        # Limpiar tabla
        for row in self.egresos_table.get_children():
            self.egresos_table.delete(row)
        
        # Obtener egresos
        egresos = obtener_egresos_finalizados()
        
        # Insertar en la tabla
        for egreso in egresos:
            # Formatear total
            egreso_formateado = list(egreso)
            egreso_formateado[3] = f"${egreso[3]}"
            
            self.egresos_table.insert("", "end", values=egreso_formateado)
        
        # Actualizar resumen
        total_compras, monto_total = calcular_resumen_egresos()
        self.total_egresos_label.configure(text=f"Total de compras: {total_compras}")
        self.monto_egresos_label.configure(text=f"Monto total: ${monto_total}")
    
    def cargar_departamentos(self):
        """Cargar departamentos en la tabla"""
        # Limpiar tabla
        for row in self.departamentos_table.get_children():
            self.departamentos_table.delete(row)
        
        # Obtener departamentos
        departamentos = obtener_departamentos()
        
        # Insertar en la tabla
        for departamento in departamentos:
            # Formatear presupuesto
            presupuesto_formateado = f"${departamento[2]}"
            departamento_formateado = list(departamento)
            departamento_formateado[2] = presupuesto_formateado
            self.departamentos_table.insert("", "end", values=departamento_formateado)
    
    def mostrar_grafica_egresos(self):
        """Mostrar gráfica de egresos por fecha"""
        # Obtener datos para la gráfica
        egresos = obtener_egresos_finalizados()
        
        if not egresos:
            messagebox.showinfo("Sin datos", "No hay datos de egresos para mostrar en la gráfica.")
            return
        
        # Procesar datos para la gráfica
        fechas_totales = {}
        for egreso in egresos:
            fecha = egreso[4]  # Fecha
            total = egreso[3]  # Total
            
            if fecha in fechas_totales:
                fechas_totales[fecha] += total
            else:
                fechas_totales[fecha] = total
        
        # Ordenar por fecha
        fechas_ordenadas = sorted(fechas_totales.items())
        fechas = [item[0] for item in fechas_ordenadas]
        totales = [item[1] for item in fechas_ordenadas]
        
        # Crear ventana para la gráfica
        grafica_window = ctk.CTkToplevel(self.parent)
        grafica_window.title("Gráfica de Egresos por Fecha")
        grafica_window.geometry("800x600")
        grafica_window.transient(self.parent)
        grafica_window.grab_set()
        
        # Crear la figura
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(fechas, totales, marker='o', linewidth=2, markersize=6, color='#8B4513')
        ax.set_title('Total de Compras por Fecha', fontsize=16, fontweight='bold')
        ax.set_xlabel('Fecha', fontsize=12)
        ax.set_ylabel('Total ($)', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Formatear eje Y para mostrar valores monetarios
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Rotar etiquetas del eje X si hay muchas fechas
        if len(fechas) > 5:
            plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        # Integrar la gráfica en la ventana
        canvas = FigureCanvasTkAgg(fig, grafica_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
        
        # Botón para cerrar
        close_button = ctk.CTkButton(
            grafica_window,
            text="Cerrar",
            command=grafica_window.destroy,
            fg_color="gray",
            hover_color="darkgray"
        )
        close_button.pack(pady=10)
    
    def on_departamento_select(self, event):
        """Manejar selección de departamento"""
        selected = self.departamentos_table.selection()
        if selected:
            self.departamento_seleccionado = self.departamentos_table.item(selected[0], "values")
            self.botones["editar"].configure(state="normal")
            self.botones["eliminar"].configure(state="normal")
        else:
            self.departamento_seleccionado = None
            self.botones["editar"].configure(state="disabled")
            self.botones["eliminar"].configure(state="disabled")
    
    def agregar_departamento(self):
        """Abrir ventana para agregar departamento"""
        from components.dialogs import DepartamentoDialog
        
        dialog = DepartamentoDialog(self.parent, "agregar")
        if dialog.resultado:
            if insertar_departamento(
                dialog.resultado["nombre"],
                dialog.resultado["presupuesto"],
                dialog.resultado["descripcion"]
            ):
                self.cargar_departamentos()
                messagebox.showinfo("Éxito", "Departamento agregado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo agregar el departamento.")
    
    def editar_departamento(self):
        """Abrir ventana para editar departamento"""
        if not self.departamento_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un departamento primero.")
            return

        from components.dialogs import DepartamentoDialog

        dialog = DepartamentoDialog(self.parent, "editar", self.departamento_seleccionado)
        if dialog.resultado:
            from services.departamento_service import actualizar_departamento
            if actualizar_departamento(
                self.departamento_seleccionado[0],
                dialog.resultado["nombre"],
                dialog.resultado["presupuesto"],
                dialog.resultado["descripcion"]
            ):
                self.cargar_departamentos()
                messagebox.showinfo("Éxito", "Departamento actualizado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el departamento.")

    
    def eliminar_departamento(self):
        """Eliminar departamento seleccionado"""
        if not self.departamento_seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un departamento primero.")
            return

        if messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar el departamento '{self.departamento_seleccionado[1]}'?\n\nEsta acción no se puede deshacer."
        ):
            from services.departamento_service import eliminar_departamento
            if eliminar_departamento(self.departamento_seleccionado[0]):
                self.cargar_departamentos()
                messagebox.showinfo("Éxito", "Departamento eliminado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el departamento.")
