"""
Configuración de la API y constantes del sistema
"""

# URL base de la API
API_URL = "http://localhost:5000"

# Configuración de la aplicación
APP_CONFIG = {
    "title": "KTech ERP - Sistema Integral",
    "geometry": "1200x700",
    "min_size": (900, 600),
    "theme": "blue",
    "appearance": "System"
}

# Configuración de tablas
TABLE_STYLE_CONFIG = {
    "background": "#ffffff",
    "foreground": "black",
    "rowheight": 25,
    "fieldbackground": "#ffffff",
    "selected_bg": "#22559b",
    "heading_bg": "#565b5e",
    "heading_fg": "white",
    "active_heading_bg": "#3484F0"
}

# Mensajes del sistema
MESSAGES = {
    "connection_error": "Error de conexión con el servidor",
    "success": "Operación realizada con éxito",
    "error": "Ha ocurrido un error",
    "confirm_delete": "¿Estás seguro de que deseas eliminar este registro?\n\nEsta acción no se puede deshacer.",
    "fields_required": "Todos los campos son obligatorios",
    "no_selection": "Debes seleccionar un registro primero"
}