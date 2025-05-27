# KTech ERP

Este proyecto es un sistema ERP educativo desarrollado con Python. Cuenta con un backend en Flask y un frontend con CustomTkinter. Se divide en módulos como ventas, compras, inventario, producción, recursos humanos, finanzas y atención al cliente.

## Requisitos

- Python 3.10 o superior
- MySQL server activo y accesible
- Paquetes del archivo requirements.txt

## Instalación

1. Clona este repositorio o copia los archivos del proyecto.
2. Instala las dependencias:

```
pip install -r requirements.txt
```

3. Crea la base de datos MySQL utilizando el script incluido como ERP_DB.sql (estructura de tablas).
4. Configura la conexión en el backend si es necesario (archivo `get_connection()`).

## Ejecución del Backend

Ejecuta el archivo principal del backend (por ejemplo `app.py`) que contiene los endpoints:

```
python app.py
```

Este comando iniciará el servidor Flask en `http://localhost:5000`.

## Ejecución del Frontend

Ejecuta el archivo combinado que incluye login y sistema completo:

```
python main_combined.py
```

Este archivo abrirá una ventana de login y, si las credenciales son válidas, cargará la interfaz según el rol del usuario.

## Notas

- Las contraseñas no están hasheadas. Este sistema es solo para propósitos educativos.
- Asegúrate de que el backend esté corriendo antes de iniciar el frontend.