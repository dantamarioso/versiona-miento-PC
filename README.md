# 🧠 N.I.C.O.L.E. – Desktop App (Versión Administrativa)

Aplicación de escritorio de **gestión administrativa** desarrollada en **Python con CustomTkinter**,  
conectada a **TiDB Cloud** como base de datos en la nube.  

Esta es la **versión administrativa de N.I.C.O.L.E.**, diseñada para centralizar el control de usuarios,  
gestionar la información registrada en el sistema y generar reportes exportables en diferentes formatos.  

---

## 🚀 Objetivo del Proyecto

El objetivo de **N.I.C.O.L.E. – Versión Administrativa** es ofrecer una herramienta de escritorio que permita:  
- Administrar de forma segura la información almacenada en la nube.  
- Gestionar usuarios, accesos y contraseñas.  
- Consultar, editar y exportar registros de manera intuitiva.  
- Garantizar trazabilidad mediante historial de acciones.  
- Apoyar el ecosistema **N.I.C.O.L.E.**, sirviendo como módulo de administración complementario a la versión web.  

---

## ✨ Características Clave

- 🔐 **Autenticación segura** con contraseñas cifradas en SHA256.  
- 👥 **Gestión de usuarios** (creación, actualización, roles de administrador).  
- 📑 **Interfaz intuitiva** para navegar entre tablas y registros.  
- 🗃️ **Operaciones CRUD**: insertar, editar y eliminar datos.  
- 📤 **Exportación de reportes** en CSV, Excel y PDF.  
- 📧 **Recuperación de contraseña** mediante correo electrónico con código de verificación.  
- 📝 **Historial/Auditoría** para registrar acciones administrativas.  
- 🖥️ **Interfaz moderna** con CustomTkinter y notificaciones dinámicas.  

---

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python 3.11+  
- **Framework GUI:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)  
- **Base de datos:** [TiDB Cloud](https://tidbcloud.com/) (compatibilidad MySQL)  
- **Dependencias principales:**  
  - `pymysql`
  - `python-dotenv`
  - `Pillow`
  - `fpdf`
  - `openpyxl`

---

## ⚙️ Instalación y Ejecución

1. Clonar este repositorio:  
   ```bash
   git clone https://github.com/tuusuario/nicole-desktop.git
   cd nicole-desktop

Crear entorno virtual e instalar dependencias:


Copiar código
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt


Configurar variables de entorno en .env:
DB_HOST=gateway01.us-west-2.prod.aws.tidbcloud.com
DB_PORT=4000
DB_USER=tu_usuario
DB_PASSWORD=tu_clave
DB_DATABASE=nicole_db

EMAIL_HOST=smtp.tuservidor.com
EMAIL_PORT=465
EMAIL_USER=tu_correo
EMAIL_PASS=tu_password
EMAIL_SENDER="NICOLE <no-reply@tuservidor.com>"
Ejecutar la aplicación:

📂 Estructura del Proyecto
bash
Copiar código
├── nicole.py           # Código principal (UI + lógica + conexión a TiDB Cloud)
├── requirements.txt    # Dependencias del proyecto
├── .env                # Configuración privada (DB y correo)
├── /icons              # Iconos usados en la interfaz
└── /doxygen_doc        # Documentación generada automáticamente


👥 Equipo
Proyecto desarrollado por el equipo ALPHA 22
como módulo administrativo de escritorio de N.I.C.O.L.E.