"""
Componente de barra lateral
"""

import customtkinter as ctk
from tkinter import messagebox

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, cambiar_vista_callback):
        super().__init__(parent, width=200, corner_radius=0)
        self.pack_propagate(False)
        
        self.cambiar_vista_callback = cambiar_vista_callback
        self.nav_buttons = []
        
        self.crear_sidebar()
    
    def crear_sidebar(self):
        # Logo y título
        self.logo_label = ctk.CTkLabel(
            self, 
            text="KTech ERP", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.logo_label.pack(pady=(20, 20))
        
        # Botones de navegación
        buttons_data = [
            {"text": "Ventas", "vista": "ventas", "active": True},
            {"text": "Recursos Humanos", "vista": "recursos_humanos"},
            {"text": "Finanzas", "vista": "finanzas"},
            {"text": "Inventario", "vista": "inventario"},
            {"text": "Producción", "vista": "produccion"},
            {"text": "Compras", "vista": "compras"},
            {"text": "Atención al Cliente", "vista": "atencion_cliente"},
        ]
        
        for i, data in enumerate(buttons_data):
            button = ctk.CTkButton(
                self,
                text=data["text"],
                fg_color="transparent" if not data.get("active", False) else "gray70",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                anchor="w",
                command=lambda v=data["vista"]: self.cambiar_vista_callback(v),
                height=40
            )
            button.pack(fill="x", padx=10, pady=5)
            self.nav_buttons.append(button)
        
        # Separador
        self.separator = ctk.CTkFrame(self, height=1, fg_color="gray70")
        self.separator.pack(fill="x", padx=10, pady=10)
        
        # Información de usuario
        self.user_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.user_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        self.user_name = ctk.CTkLabel(
            self.user_frame, 
            text="Usuario: Admin",
            anchor="w"
        )
        self.user_name.pack(fill="x", pady=2)
        
        self.logout_button = ctk.CTkButton(
            self.user_frame,
            text="Cerrar Sesión",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            height=30,
            command=self.logout
        )
        self.logout_button.pack(fill="x", pady=5)
    
    def actualizar_navegacion(self, vista_activa):
        """Actualizar colores de los botones de navegación"""
        vistas = ["ventas", "recursos_humanos", "finanzas", "inventario", "produccion", "compras", "atencion_cliente"]
        for i, vista in enumerate(vistas):
            if vista == vista_activa:
                self.nav_buttons[i].configure(fg_color="gray70")
            else:
                self.nav_buttons[i].configure(fg_color="transparent")
    
    def logout(self):
        """Cerrar sesión"""
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que deseas cerrar sesión?"):
            self.master.destroy()