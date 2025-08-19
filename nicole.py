# =================================================================================
# APLICACIÓN DE GESTIÓN DE BASE DE DATOS "N.I.C.O.L.E" - VERSIÓN MEJORADA
# =================================================================================
#
# DESCRIPCIÓN:
# Una aplicación de escritorio con interfaz gráfica (GUI) para visualizar,
# crear, editar y eliminar registros de una base de datos MySQL, con un
# diseño de UI mejorado y funcionalidad de exportación unificada.
#
# TECNOLOGÍAS UTILIZADAS:
# - Python 3, CustomTkinter, PyMySQL, Pillow, OpenPyXL, FPDF
#
# =================================================================================


# -------------------------IMPORTACIÓN DE LIBRERÍAS----------------------------

import hashlib
import re
from datetime import datetime
from tkinter import messagebox, ttk, filedialog

import customtkinter as ctk
import pymysql
from PIL import Image
from pymysql.err import MySQLError

import csv
import openpyxl
from fpdf import FPDF
from dotenv import load_dotenv

import os

load_dotenv() 

# ------------------------CONEXIÓN A LA BASE DE DATOS---------------------------

def conectar_db():
    """
    Establece y retorna una conexión con la base de datos MySQL.
    """
    try:
        return pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE"),
            port=int(os.getenv("DB_PORT"))  
        )
    except MySQLError as err:
        print(f"Error MySQL: No se pudo conectar a MySQL:\n{err}")
        return None

# ------------------------FUNCIONES DE GESTIÓN DE DATOS----------------------------

def init_db():
    """
    Inicializa la base de datos, creando tablas y usuario admin si no existen.
    """
    db = conectar_db()
    if not db:
        return

    try:
        cur = db.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS historial (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario VARCHAR(50),
                fecha DATETIME,
                accion VARCHAR(20),
                tabla VARCHAR(50),
                registro_id VARCHAR(50),
                valores_antes TEXT,
                valores_despues TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios_app (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE,
                password_hash VARCHAR(255),
                es_admin BOOLEAN
            )
        """)

        cur.execute("SELECT * FROM usuarios_app WHERE username='admin'")
        if not cur.fetchone():
            h = hashlib.sha256("admin123".encode()).hexdigest()
            cur.execute("INSERT INTO usuarios_app (username, password_hash, es_admin) VALUES (%s, %s, %s)", ("admin", h, True))

        db.commit()
    except MySQLError as err:
        messagebox.showerror("Error de Inicialización", f"No se pudo inicializar la base de datos:\n{err}")
    finally:
        if db.open:
            cur.close()
            db.close()


def registrar_historial(usuario, accion, tabla, registro_id, antes="", despues=""):
    """
    Registra una acción (INSERT, UPDATE, DELETE) en la tabla 'historial'.
    """
    db = conectar_db()
    if not db:
        return

    try:
        cur = db.cursor()
        cur.execute("""
            INSERT INTO historial (usuario, fecha, accion, tabla, registro_id, valores_antes, valores_despues)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (usuario, datetime.now(), accion, tabla, str(registro_id), antes, despues))
        db.commit()
    except MySQLError as err:
        print(f"Error al registrar en historial: {err}")
    finally:
        if db.open:
            cur.close()
            db.close()


def obtener_tablas():
    """
    Obtiene una lista de las tablas de la BD, excluyendo las internas de la app.
    """
    db = conectar_db()
    if not db:
        return []

    try:
        cur = db.cursor()
        cur.execute("SHOW TABLES")
        tablas = [r[0] for r in cur.fetchall() if r[0] not in ("historial", "usuarios_app")]
        return tablas
    except MySQLError as err:
        messagebox.showerror("Error de Lectura", f"No se pudieron obtener las tablas:\n{err}")
        return []
    finally:
        if db.open:
            cur.close()
            db.close()


def obtener_datos(tabla):
    """
    Obtiene las columnas y todas las filas de una tabla específica.
    """
    db = conectar_db()
    if not db:
        return [], []

    try:
        cur = db.cursor()
        cur.execute(f"SELECT * FROM {tabla}")
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        return cols, rows
    except MySQLError as err:
        messagebox.showerror("Error de Lectura", f"No se pudieron obtener los datos de la tabla '{tabla}':\n{err}")
        return [], []
    finally:
        if db.open:
            cur.close()
            db.close()


def mostrar_toast(texto, parent):
    """
    Muestra una notificación emergente temporal (toast) en la pantalla.
    """
    toast = ctk.CTkToplevel(parent)
    toast.overrideredirect(True)
    
    # Calcular posición del toast en la esquina inferior derecha de la ventana padre
    x = parent.winfo_rootx() + parent.winfo_width() - 310
    y = parent.winfo_rooty() + parent.winfo_height() - 110
    toast.geometry(f"300x50+{x}+{y}")
    
    ctk.CTkLabel(toast, text=texto, font=ctk.CTkFont(size=14)).pack(expand=True, fill="both", padx=10, pady=5)
    toast.attributes("-topmost", True)
    toast.after(2500, toast.destroy)

# ------------------------CLASE PRINCIPAL DE LA APLICACIÓN---------------------------

class App(ctk.CTk):
    """
    Clase principal que encapsula toda la aplicación, manejando la UI y eventos.
    """
    def __init__(self):
        super().__init__()
        self.withdraw()
        init_db()
        self.usuario = None
        self.is_admin = False
        self.login_usuario()

    def login_usuario(self):
        win = ctk.CTkToplevel(self)
        win.title("🔐 Login")
        win.geometry("300x200")
        win.resizable(False, False)
        win.protocol("WM_DELETE_WINDOW", self.destroy)
        win.after(100, win.grab_set)

        ctk.CTkLabel(win, text="Usuario:").pack(pady=(20, 5))
        entry_user = ctk.CTkEntry(win, placeholder_text="nombre de usuario")
        entry_user.pack(padx=20, fill="x")
        ctk.CTkLabel(win, text="Contraseña:").pack(pady=5)
        entry_pass = ctk.CTkEntry(win, show="*", placeholder_text="contraseña")
        entry_pass.pack(padx=20, fill="x")

        def intentar(event=None):
            u = entry_user.get()
            p = entry_pass.get()
            if not u or not p:
                mostrar_toast("Usuario y contraseña requeridos", win)
                return

            h = hashlib.sha256(p.encode()).hexdigest()
            db = conectar_db()
            if not db: return

            try:
                cur = db.cursor()
                cur.execute("SELECT es_admin FROM usuarios_app WHERE username=%s AND password_hash=%s", (u, h))
                res = cur.fetchone()
                if res:
                    self.usuario = u
                    self.is_admin = bool(res[0])
                    win.destroy()
                    self.mostrar_bienvenida()
                else:
                    mostrar_toast("Credenciales inválidas", win)
            except MySQLError as err:
                messagebox.showerror("Error de Login", f"Ocurrió un error:\n{err}", parent=win)
            finally:
                if db.open: cur.close(); db.close()
        
        ctk.CTkButton(win, text="Entrar", command=intentar).pack(pady=20)
        entry_user.bind('<Return>', intentar)
        entry_pass.bind('<Return>', intentar)

    def mostrar_bienvenida(self):
        self.withdraw()
        win = ctk.CTkToplevel(self)
        win.title("🎉 Bienvenida")
        win.geometry("400x200")
        win.resizable(False, False)
        win.protocol("WM_DELETE_WINDOW", self.destroy)
        win.transient(self)
        win.after(10, win.grab_set)

        ctk.CTkLabel(win, text=f"¡Bienvenido, {self.usuario}!", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(30, 10))
        ctk.CTkLabel(win, text="Has iniciado sesión correctamente.", justify="center").pack()

        def continuar():
            win.destroy()
            self.deiconify()
            self.init_ui()

        ctk.CTkButton(win, text="👉 Continuar", command=continuar).pack(pady=30)
        win.bind('<Return>', lambda event: continuar())


    def cerrar_sesion(self):
        self.withdraw()
        for widget in self.winfo_children():
            widget.destroy()
        self.usuario = None
        self.is_admin = False
        self.login_usuario()

    def init_ui(self):
        """
        ### MODIFICADO ###
        Construye la interfaz de usuario principal con una mejor disposición.
        """
        self.title(f"N.I.C.O.L.E – Sesión de {self.usuario}")
        self.state('zoomed')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Fila del Treeview se expande

        # --- Carga del icono ---
        try:
            image_data = Image.open("brain_icon.png")
            self.brain_icon = ctk.CTkImage(light_image=image_data, dark_image=image_data, size=(40, 40))
        except FileNotFoundError:
            self.brain_icon = None
        
        # --- Frame Superior (Título, Búsqueda, Selector de Tablas) ---
        top_frame = ctk.CTkFrame(self)
        top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        top_frame.grid_columnconfigure(1, weight=1) # Columna de búsqueda se expande

        ctk.CTkLabel(top_frame, text="N.I.C.O.L.E", image=self.brain_icon, compound="left", font=ctk.CTkFont(size=22, weight="bold")).grid(row=0, column=0, padx=10, pady=10)

        self.busc = ctk.CTkEntry(top_frame, placeholder_text="🔍 Buscar en la tabla actual…", height=35)
        self.busc.grid(row=0, column=1, sticky="ew", padx=10)
        self.busc.bind("<KeyRelease>", self.buscar)

        frame_selector = ctk.CTkFrame(top_frame, fg_color="transparent")
        frame_selector.grid(row=0, column=2, padx=10)
        ctk.CTkLabel(frame_selector, text="Tabla:").pack(side="left", padx=(0, 5))
        tablas = obtener_tablas()
        self.combo = ctk.CTkOptionMenu(frame_selector, values=tablas if tablas else ["No hay tablas"], command=self.cargar_tabla, height=35)
        self.combo.pack(side="left")

        # --- Tabla Principal de Datos (Treeview) ---
        ttk_frame = ctk.CTkFrame(self)
        ttk_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        ttk_frame.grid_rowconfigure(0, weight=1)
        ttk_frame.grid_columnconfigure(0, weight=1)
        
        # Estilo del Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=25, fieldbackground="#343638", borderwidth=0)
        style.map('Treeview', background=[('selected', '#245d81')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat", font=('Calibri', 10, 'bold'))
        style.map("Treeview.Heading", background=[('active', '#343638')])

        self.tree = ttk.Treeview(ttk_frame, style="Treeview")
        vsb = ttk.Scrollbar(ttk_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(ttk_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        self.tree.bind("<Double-1>", self.editar_celda)

        # --- Frame de Botones Inferiores ---
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
        bottom_frame.grid_columnconfigure((1, 3), weight=1) # Columnas espaciadoras
        
        # Grupo Izquierdo: Acciones de datos
        frame_acciones = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        frame_acciones.grid(row=0, column=0)
        self.btn_add = ctk.CTkButton(frame_acciones, text="➕ Añadir", command=self.abrir_form)
        self.btn_add.pack(side="left", padx=5)
        self.btn_del = ctk.CTkButton(frame_acciones, text="🗑️ Borrar", fg_color="#D32F2F", hover_color="#B71C1C", command=self.eliminar_registro)
        self.btn_del.pack(side="left", padx=5)

        # Grupo Central: Gestión
        frame_gestion = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        frame_gestion.grid(row=0, column=2)
        ctk.CTkButton(frame_gestion, text="🔄 Recargar", command=self.cargar_tabla_actual).pack(side="left", padx=5)
        ctk.CTkButton(frame_gestion, text="🕵️ Historial", command=self.ver_historial).pack(side="left", padx=5)
        ctk.CTkButton(frame_gestion, text="📦 Exportar", command=self.iniciar_exportacion).pack(side="left", padx=5)
        
        # Grupo Derecho: Sesión
        frame_sesion = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        frame_sesion.grid(row=0, column=4)
        self.btn_user = ctk.CTkButton(frame_sesion, text="👤 Nuevos usuarios", command=self.registrar_usuario)
        self.btn_user.pack(side="left", padx=5)
        ctk.CTkButton(frame_sesion, text="🚪 Salir", command=self.cerrar_sesion).pack(side="left", padx=5)

        # Deshabilitar funcionalidades si no es admin
        if not self.is_admin:
            self.btn_del.configure(state="disabled")
            self.btn_user.configure(state="disabled")
            self.btn_add.configure(state="disabled")
            self.tree.unbind("<Double-1>")

        if tablas:
            self.combo.set(tablas[0])
            self.cargar_tabla(tablas[0])

    ### NUEVO: MÉTODO PARA INICIAR LA EXPORTACIÓN ###
    def iniciar_exportacion(self):
        """
        Abre un diálogo para guardar el archivo, permitiendo al usuario
        elegir el formato (Excel, PDF, CSV) y el nombre del archivo.
        """
        if not hasattr(self, "table") or self.table == "No hay tablas":
            return mostrar_toast("Primero selecciona una tabla con datos.", self)
        
        # Definir los tipos de archivo para el diálogo
        file_types = [
            ("Archivos Excel", "*.xlsx"),
            ("Archivos PDF", "*.pdf"),
            ("Archivos CSV", "*.csv")
        ]
        
        filepath = filedialog.asksaveasfilename(
            filetypes=file_types,
            defaultextension=".xlsx", # Extensión por defecto
            initialfile=f"export_{self.table}_{datetime.now():%Y-%m-%d}",
            title="Exportar datos de la tabla"
        )

        if not filepath: # Si el usuario cancela
            return

        # Llamar a la función de exportación correspondiente según la extensión elegida
        if filepath.endswith('.xlsx'):
            self._exportar_excel(filepath)
        elif filepath.endswith('.csv'):
            self._exportar_csv(filepath)
        elif filepath.endswith('.pdf'):
            self._exportar_pdf(filepath)

    ### MODIFICADO: Métodos de exportación ahora son "privados" y reciben la ruta ###
    def _exportar_csv(self, filepath):
        try:
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.col) # Cabeceras
                for item_id in self.tree.get_children():
                    writer.writerow(self.tree.item(item_id)['values'])
            mostrar_toast("CSV exportado con éxito", self)
        except Exception as e:
            messagebox.showerror("Error de Exportación", f"No se pudo exportar a CSV:\n{e}")

    def _exportar_excel(self, filepath):
        try:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = self.table
            sheet.append(self.col) # Cabeceras
            for item_id in self.tree.get_children():
                sheet.append(self.tree.item(item_id)['values'])
            workbook.save(filepath)
            mostrar_toast("Excel exportado con éxito", self)
        except Exception as e:
            messagebox.showerror("Error de Exportación", f"No se pudo exportar a Excel:\n{e}")

    def _exportar_pdf(self, filepath):
        try:
            pdf = FPDF(orientation='L', unit='mm', format='A4')
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, f'Reporte de Tabla: {self.table}', 0, 1, 'C')
            pdf.ln(5)

            pdf.set_font("Arial", 'B', 8)
            num_cols = len(self.col)
            # Ancho de página usable (A4 apaisado = 297mm, menos márgenes)
            page_width = 297 - 2 * 10 
            col_width = page_width / num_cols if num_cols > 0 else 10

            # Cabeceras
            pdf.set_fill_color(224, 224, 224) # Gris claro
            for header in self.col:
                pdf.cell(col_width, 8, str(header), 1, 0, 'C', fill=True)
            pdf.ln()

            # Datos
            pdf.set_font("Arial", '', 7)
            pdf.set_fill_color(255, 255, 255)
            fill = False
            for item_id in self.tree.get_children():
                row = self.tree.item(item_id)['values']
                for item in row:
                    pdf.cell(col_width, 8, str(item), 1, 0, 'L', fill=fill)
                pdf.ln()
                fill = not fill # Alternar color de fila

            pdf.output(filepath)
            mostrar_toast("PDF exportado con éxito", self)
        except Exception as e:
            messagebox.showerror("Error de Exportación", f"No se pudo exportar a PDF:\n{e}")

    # ... (El resto del código de la clase App se mantiene igual) ...
    def registrar_usuario(self):
        if not self.is_admin: return

        win = ctk.CTkToplevel(self)
        win.title("➕ Nuevo Usuario")
        win.geometry("350x300")
        win.resizable(False, False)
        win.transient(self)
        win.after(10, win.grab_set)

        ctk.CTkLabel(win, text="Nombre de Usuario:").pack(pady=(20, 5))
        e_user = ctk.CTkEntry(win)
        e_user.pack(padx=20, fill="x")
        ctk.CTkLabel(win, text="Contraseña:").pack(pady=5)
        e_pass = ctk.CTkEntry(win, show="*")
        e_pass.pack(padx=20, fill="x")
        val_admin = ctk.CTkCheckBox(win, text="Otorgar privilegios de Administrador")
        val_admin.pack(pady=10)

        def guardar_user():
            u = e_user.get().strip()
            p = e_pass.get().strip()
            if not u or not p:
                return mostrar_toast("Completa todos los campos", win)

            h = hashlib.sha256(p.encode()).hexdigest()
            esadm = val_admin.get()
            
            db = conectar_db()
            if not db: return
            
            try:
                cur = db.cursor()
                cur.execute("INSERT INTO usuarios_app (username, password_hash, es_admin) VALUES (%s, %s, %s)", (u, h, esadm))
                db.commit()
                mostrar_toast("Usuario creado correctamente", self)
                win.destroy()
            except pymysql.err.IntegrityError:
                messagebox.showerror("Error", f"El usuario '{u}' ya existe.", parent=win)
            except MySQLError as err:
                messagebox.showerror("Error", f"No se pudo crear el usuario:\n{err}", parent=win)
            finally:
                if db.open: cur.close(); db.close()

        ctk.CTkButton(win, text="💾 Guardar Usuario", command=guardar_user).pack(pady=20)

    def cargar_tabla(self, tabla):
        if tabla == "No hay tablas":
            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = []
            return
            
        self.tree.delete(*self.tree.get_children())
        self.col, rows = obtener_datos(tabla)
        if not self.col:
            return

        self.table = tabla
        self.tree["columns"] = self.col
        self.tree["show"] = "headings"
        for c in self.col:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="w", width=150, minwidth=100) # Ancho por defecto y mínimo
        for r in rows:
            self.tree.insert("", "end", values=r)

    def cargar_tabla_actual(self):
        if hasattr(self, "table"):
            self.cargar_tabla(self.table)

    def buscar(self, ev=None):
        if not hasattr(self, "table"): return
        txt = self.busc.get().lower()
        self.tree.delete(*self.tree.get_children())
        _, rows = obtener_datos(self.table)
        for r in rows:
            if any(txt in str(v).lower() for v in r):
                self.tree.insert("", "end", values=r)

    def abrir_form(self):
        if not hasattr(self, "table"):
            return mostrar_toast("Selecciona una tabla primero", self)

        win = ctk.CTkToplevel(self)
        win.title(f"➕ Agregar registro a {self.table}")
        win.geometry("420x500")
        win.transient(self)
        win.after(10, win.grab_set)

        scroll = ctk.CTkScrollableFrame(win)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        cols, _ = obtener_datos(self.table)
        cols_no_id = [c for c in cols if c.lower() != "id"]
        entries = {}

        for c in cols_no_id:
            ctk.CTkLabel(scroll, text=f"{c}:").pack(anchor="w", padx=5, pady=(10, 0))
            if "fecha" in c.lower():
                ent = ctk.CTkEntry(scroll)
                ent.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                ent.configure(state="readonly")
            else:
                ent = ctk.CTkEntry(scroll, show="*" if "pass" in c.lower() else None)
            ent.pack(fill="x", padx=5)
            entries[c] = ent

        def insertar():
            vals = []
            for c in cols_no_id:
                v = entries[c].get()
                if "pass" in c.lower() and "password_hash" not in c.lower():
                    v = hashlib.sha256(v.encode()).hexdigest()
                vals.append(v)
                
            if any(not str(x).strip() for x in vals):
                return mostrar_toast("Completa todos los campos", win)
            
            db = conectar_db()
            if not db: return

            try:
                cur = db.cursor()
                query = f"INSERT INTO {self.table} ({','.join(cols_no_id)}) VALUES ({','.join(['%s'] * len(vals))})"
                cur.execute(query, vals)
                rid = cur.lastrowid
                db.commit()
                
                registrar_historial(self.usuario, "INSERT", self.table, rid, "", str(dict(zip(cols_no_id, vals))))
                win.destroy()
                self.cargar_tabla_actual()
                mostrar_toast("Registro insertado", self)
            except MySQLError as err:
                messagebox.showerror("Error al Insertar", f"No se pudo guardar:\n{err}", parent=win)
            finally:
                if db.open: cur.close(); db.close()

        ctk.CTkButton(scroll, text="💾 Insertar Registro", command=insertar).pack(pady=20, padx=5)

    def eliminar_registro(self):
        sel = self.tree.focus()
        if not sel: return

        r = self.tree.item(sel)["values"]
        pk_col_name = self.col[0]
        pk_value = r[0]
        before = str(dict(zip(self.col, r)))

        if messagebox.askyesno("Confirmar Borrado", f"¿Seguro que quieres eliminar el registro con {pk_col_name} = {pk_value}?"):
            db = conectar_db()
            if not db: return
            
            try:
                cur = db.cursor()
                cur.execute(f"DELETE FROM {self.table} WHERE {pk_col_name}=%s", (pk_value,))
                db.commit()
                
                registrar_historial(self.usuario, "DELETE", self.table, pk_value, before, "")
                self.cargar_tabla_actual()
                mostrar_toast("Registro eliminado", self)
            except pymysql.err.IntegrityError as e:
                if e.args[0] == 1451: # Foreign key constraint
                    match = re.search(r"fails \(`\w+`\.`(.+?)`\)", e.args[1])
                    tabla_dependiente = match.group(1) if match else "otra tabla"
                    msg = (f"No se puede eliminar. Este registro está siendo usado por la tabla '{tabla_dependiente}'.\n\n"
                           f"Debes eliminar o actualizar los registros dependientes primero.")
                    messagebox.showerror("Error de Integridad", msg)
                else:
                    messagebox.showerror("Error de BD", f"No se pudo eliminar:\n{e}")
            except MySQLError as err:
                messagebox.showerror("Error de Borrado", f"Ocurrió un error:\n{err}")
            finally:
                if db.open: cur.close(); db.close()

    def editar_celda(self, ev):
        if not self.is_admin: return
            
        sel = self.tree.identify_row(ev.y)
        cid = self.tree.identify_column(ev.x)
        if not sel or not cid: return

        col_index = int(cid.replace("#", "")) - 1
        col_name = self.col[col_index]
        pk_col_name = self.col[0]
        pk_value = self.tree.item(sel)["values"][0]

        if col_name.lower() == pk_col_name.lower():
            return mostrar_toast(f"La clave primaria ({pk_col_name}) no se puede editar.", self)
            
        old_val = self.tree.item(sel)["values"][col_index]
        
        x, y, w, h = self.tree.bbox(sel, cid)
        ent = ctk.CTkEntry(self.tree, width=w, height=h, show="*" if "pass" in col_name.lower() else None)
        ent.place(x=x, y=y)
        ent.insert(0, old_val)
        ent.focus()

        def save(event):
            new_val = ent.get()
            ent.destroy()
            if new_val == old_val: return

            final_val = hashlib.sha256(new_val.encode()).hexdigest() if "pass" in col_name.lower() and "hash" not in col_name.lower() else new_val

            db = conectar_db()
            if not db: return
            
            try:
                cur = db.cursor()
                cur.execute(f"UPDATE {self.table} SET {col_name}=%s WHERE {pk_col_name}=%s", (final_val, pk_value))
                db.commit()
                
                antes = f"{col_name}: {old_val}"
                despues = f"{col_name}: {final_val}"
                registrar_historial(self.usuario, "UPDATE", self.table, pk_value, antes, despues)
                self.cargar_tabla_actual()
                mostrar_toast("Registro actualizado", self)
            except MySQLError as err:
                messagebox.showerror("Error al Actualizar", f"No se pudo guardar:\n{err}")
                self.cargar_tabla_actual()
            finally:
                if db.open: cur.close(); db.close()

        ent.bind("<Return>", save)
        ent.bind("<FocusOut>", lambda e: ent.destroy())

    def ver_historial(self):
        win = ctk.CTkToplevel(self)
        win.title("📋 Historial de Cambios")
        win.geometry("1000x500")
        win.transient(self)
        win.after(10, win.grab_set)
        
        frame = ctk.CTkFrame(win)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        tv = ttk.Treeview(frame)
        tv["columns"] = ("ID", "Usuario", "Fecha", "Acción", "Tabla", "ID Reg.", "Valores Anteriores", "Valores Nuevos")
        tv.column("#0", width=0, stretch="no")
        for col in tv["columns"]:
            tv.column(col, anchor="w", width=120)
            tv.heading(col, text=col, anchor="w")
        
        db = conectar_db()
        if not db: return

        try:
            cur = db.cursor()
            cur.execute("SELECT id, usuario, fecha, accion, tabla, registro_id, valores_antes, valores_despues FROM historial ORDER BY fecha DESC")
            for r in cur.fetchall():
                tv.insert("", "end", values=r)
        except MySQLError as err:
            messagebox.showerror("Error", f"No se pudo cargar el historial:\n{err}", parent=win)
        finally:
            if db.open: cur.close(); db.close()
        
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tv.yview)
        tv.configure(yscrollcommand=vsb.set)
        tv.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")


# ------------------------PUNTO DE ENTRADA DE LA APLICACIÓN---------------------------

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    app = App()
    app.mainloop()