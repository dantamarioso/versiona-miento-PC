# N.I.C.O.L.E. - Aplicación de gestión de base de datos

## Descripción
Aplicación de escritorio en Python para gestionar tablas MySQL con interfaz gráfica (customtkinter). Permite login, edición, borrado, exportación y registro de usuarios, con historial de cambios y recuperación de contraseña.

## Estructura principal
- `nicole.py`: archivo principal con toda la lógica y la interfaz.
- `requirements.txt`: dependencias necesarias.
- `build/`, `Output/`: carpetas generadas por PyInstaller y exportaciones.

## Ejecución
1. Instala dependencias:
   ```powershell
   pip install -r requirements.txt
   ```
2. Ejecuta la aplicación:
   ```powershell
   python nicole.py
   ```

## Funcionalidades
- Login y gestión de usuarios (admin y estándar)
- Visualización y edición de tablas MySQL
- Exportación a Excel, PDF y CSV
- Recuperación de contraseña por correo
- Historial de cambios
- Interfaz responsiva y animaciones de carga

## Notas
- Requiere archivo `.env` con credenciales de base de datos y correo.
- Los iconos deben estar en la carpeta raíz (PNG).
- Compatible con PyInstaller para generar ejecutable.
