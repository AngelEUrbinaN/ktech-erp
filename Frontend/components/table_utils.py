"""
Utilidades para manejo de tablas
"""

from tkinter import ttk
from config.api_config import TABLE_STYLE_CONFIG

def configurar_estilo_tabla():
    """Configurar el estilo global para las tablas"""
    style = ttk.Style()
    style.theme_use("default")
    
    # Configurar estilo del Treeview
    style.configure("Treeview", 
                    background=TABLE_STYLE_CONFIG["background"], 
                    foreground=TABLE_STYLE_CONFIG["foreground"], 
                    rowheight=TABLE_STYLE_CONFIG["rowheight"], 
                    fieldbackground=TABLE_STYLE_CONFIG["fieldbackground"])
    
    style.map('Treeview', background=[('selected', TABLE_STYLE_CONFIG["selected_bg"])])
    
    # Configurar estilo de los encabezados
    style.configure("Treeview.Heading", 
                    background=TABLE_STYLE_CONFIG["heading_bg"], 
                    foreground=TABLE_STYLE_CONFIG["heading_fg"], 
                    relief="flat")
    
    style.map("Treeview.Heading", 
              background=[('active', TABLE_STYLE_CONFIG["active_heading_bg"])])

def crear_tabla_con_scrollbar(parent, columns, height=12):
    """Crear una tabla con scrollbar configurada"""
    import customtkinter as ctk
    
    # Configurar estilo
    configurar_estilo_tabla()
    
    # Crear tabla
    table = ttk.Treeview(
        parent,
        columns=columns,
        show="headings",
        height=height
    )
    
    # Crear scrollbar
    scrollbar = ctk.CTkScrollbar(parent, command=table.yview)
    scrollbar.pack(side="right", fill="y")
    table.configure(yscrollcommand=scrollbar.set)
    
    return table, scrollbar