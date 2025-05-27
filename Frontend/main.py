"""
KTech ERP - Sistema Integral
Archivo principal de la aplicación
"""

import customtkinter as ctk
from components.sidebar import Sidebar
from views.ventas_view import VentasView
from views.recursos_humanos_view import RecursosHumanosView
from views.finanzas_view import FinanzasView
from views.inventario_view import InventarioView
from views.produccion_view import ProduccionView
from views.compras_view import ComprasView
from views.atencion_cliente_view import AtencionClienteView

# Configuración global de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class KTechERP(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana principal
        self.title("KTech ERP - Sistema Integral")
        self.geometry("1200x700")
        self.minsize(900, 600)
        
        # Variables globales
        self.vista_actual = "ventas"
        self.current_view = None
        
        # Crear estructura principal
        self.crear_interfaz()
        
        # Mostrar vista inicial
        self.mostrar_ventas()
    
    def crear_interfaz(self):
        # Crear sidebar
        self.sidebar = Sidebar(self, self.cambiar_vista)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        
        # Frame principal para el contenido
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=0, pady=0)
    
    def limpiar_main_frame(self):
        """Limpiar el frame principal"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.current_view = None
    
    def cambiar_vista(self, vista):
        """Cambiar entre diferentes vistas del sistema"""
        self.vista_actual = vista
        self.limpiar_main_frame()
        
        if vista == "ventas":
            self.mostrar_ventas()
        elif vista == "productos":
            self.mostrar_productos()
        elif vista == "clientes":
            self.mostrar_clientes()
        elif vista == "recursos_humanos":
            self.mostrar_recursos_humanos()
        elif vista == "finanzas":
            self.mostrar_finanzas()
        elif vista == "inventario":
            self.mostrar_inventario()
        elif vista == "produccion":
            self.mostrar_produccion()
        elif vista == "compras":
            self.mostrar_compras()
        elif vista == "atencion_cliente":
            self.mostrar_atencion_cliente()

    def mostrar_ventas(self):
        """Mostrar módulo de ventas"""
        self.current_view = VentasView(self.main_frame)
        self.sidebar.actualizar_navegacion("ventas")
    
    def mostrar_productos(self):
        """Mostrar módulo de productos"""
        placeholder = ctk.CTkLabel(
            self.main_frame,
            text="Módulo de Productos\n\n(En desarrollo)",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        placeholder.pack(expand=True)
        self.sidebar.actualizar_navegacion("productos")
    
    def mostrar_clientes(self):
        """Mostrar módulo de clientes"""

        placeholder = ctk.CTkLabel(
            self.main_frame,
            text="Módulo de Clientes\n\n(En desarrollo)",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        placeholder.pack(expand=True)
        self.sidebar.actualizar_navegacion("clientes")
    
    def mostrar_recursos_humanos(self):
        """Mostrar módulo de recursos humanos"""
        self.current_view = RecursosHumanosView(self.main_frame)
        self.sidebar.actualizar_navegacion("recursos_humanos")
    
    def mostrar_finanzas(self):
        """Mostrar módulo de finanzas"""
        self.current_view = FinanzasView(self.main_frame)
        self.sidebar.actualizar_navegacion("finanzas")

    def mostrar_inventario(self):
        """Mostrar módulo de inventario"""
        self.current_view = InventarioView(self.main_frame)
        self.sidebar.actualizar_navegacion("inventario")

    def mostrar_produccion(self):
        """Mostrar módulo de producción"""
        self.current_view = ProduccionView(self.main_frame)
        self.sidebar.actualizar_navegacion("produccion")

    def mostrar_compras(self):
        """Mostrar módulo de compras"""
        self.current_view = ComprasView(self.main_frame)
        self.sidebar.actualizar_navegacion("compras")

    def mostrar_atencion_cliente(self):
        """Mostrar módulo de compras"""
        self.current_view = AtencionClienteView(self.main_frame)
        self.sidebar.actualizar_navegacion("atencion_cliente")
    

if __name__ == "__main__":
    app = KTechERP()
    app.mainloop()