"""
Componente de barra lateral
"""

import customtkinter as ctk
from tkinter import messagebox

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, cambiar_vista_callback, departamento_id):
        super().__init__(parent, width=200, corner_radius=0)
        self.departamento_id = departamento_id
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
        
        # Módulos permitidos por departamento
        modulos_por_departamento = {
            1: ["ventas", "recursos_humanos", "finanzas", "inventario", "produccion", "compras", "atencion_cliente"],
            2: ["ventas"],
            4: ["recursos_humanos"],
            5: ["finanzas"],
            6: ["inventario"],
            7: ["produccion"],
            8: ["compras"],
            9: ["atencion_cliente"]
        }

        # Lista de módulos permitidos para este usuario
        modulos_disponibles = modulos_por_departamento.get(self.departamento_id, [])

        # Definir todos los botones posibles
        buttons_data = [
            {"text": "Ventas", "vista": "ventas"},
            {"text": "Recursos Humanos", "vista": "recursos_humanos"},
            {"text": "Finanzas", "vista": "finanzas"},
            {"text": "Inventario", "vista": "inventario"},
            {"text": "Producción", "vista": "produccion"},
            {"text": "Compras", "vista": "compras"},
            {"text": "Atención al Cliente", "vista": "atencion_cliente"},
        ]

        self.nav_dict = {}
        
        # Crear solo los botones permitidos
        for data in buttons_data:
            if data["vista"] not in modulos_disponibles:
                continue

            button = ctk.CTkButton(
                self,
                text=data["text"],
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                anchor="w",
                command=lambda v=data["vista"]: self.cambiar_vista_callback(v),
                height=40
            )
            button.pack(fill="x", padx=10, pady=5)
            self.nav_buttons.append(button)
            self.nav_dict[data["vista"]] = button
        
        # Separador
        self.separator = ctk.CTkFrame(self, height=1, fg_color="gray70")
        self.separator.pack(fill="x", padx=10, pady=10)
        
        # Información de usuario
        self.user_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.user_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        
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
        for vista, button in self.nav_dict.items():
            if vista == vista_activa:
                button.configure(fg_color="gray70")
            else:
                button.configure(fg_color="transparent")
    
    def logout(self):
        """Cerrar sesión"""
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro de que deseas cerrar sesión?"):
            self.master.destroy()