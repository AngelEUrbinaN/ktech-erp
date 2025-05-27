"""
Clase base para todas las vistas
"""

import customtkinter as ctk
from components.table_utils import crear_tabla_con_scrollbar

class BaseView:
    def __init__(self, parent):
        self.parent = parent
        self.crear_vista()
    
    def crear_vista(self):
        """Método que debe ser implementado por las clases hijas"""
        raise NotImplementedError("Las clases hijas deben implementar crear_vista()")
    
    def crear_header(self, titulo):
        """Crear header común para todas las vistas"""
        header_frame = ctk.CTkFrame(self.parent, fg_color="transparent", height=60)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        section_title = ctk.CTkLabel(
            header_frame, 
            text=titulo,
            font=ctk.CTkFont(size=24, weight="bold")
        )
        section_title.pack(side="left", pady=10)
        
        return header_frame
    
    def crear_botones_accion(self, parent, botones_config):
        """Crear frame con botones de acción"""
        botones_frame = ctk.CTkFrame(parent, fg_color="transparent")
        botones_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        botones = {}
        for config in botones_config:
            button = ctk.CTkButton(
                botones_frame,
                text=config["text"],
                command=config["command"],
                state=config.get("state", "normal"),
                fg_color=config.get("fg_color", None),
                hover_color=config.get("hover_color", None)
            )
            button.pack(side="left", padx=5)
            botones[config["name"]] = button
        
        return botones_frame, botones
    
    def crear_tabla_frame(self, parent, columnas, height=12):
        """Crear frame con tabla y scrollbar"""
        table_frame = ctk.CTkFrame(parent)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        table, scrollbar = crear_tabla_con_scrollbar(table_frame, columnas, height)
        table.pack(fill="both", expand=True, padx=5, pady=5)
        
        return table_frame, table