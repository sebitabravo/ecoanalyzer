import sys
import os
import sqlite3
import configparser
from tkinter import messagebox, BooleanVar
from customtkinter import *
from PIL import Image
import traceback

# Ruta de la carpeta de logs en la raíz del proyecto
ruta_logs = os.path.join(os.path.dirname(__file__), '..', 'logs')

# Crear la carpeta de logs si no existe
if not os.path.exists(ruta_logs):
    os.makedirs(ruta_logs)

# Ruta del archivo de registro de errores dentro de la carpeta de logs
archivo_errores = os.path.join(ruta_logs, 'errores.log')

# Redirigir la salida de errores a un archivo
sys.stderr = open(archivo_errores, 'w')


try:
    # Funciones para operaciones específicas

    def cargar_imagenes():
        ruta_img = os.path.join(os.path.dirname(__file__), '..', 'img')
        return {
            "side_img": Image.open(os.path.join(ruta_img, "side-img.png")),
            "email_icon": Image.open(os.path.join(ruta_img, "email-icon.png")),
            "password_icon": Image.open(os.path.join(ruta_img, "password-icon.png"))
        }

    def guardar_config(usuario, recordar):
        ruta_config = os.path.join(os.path.dirname(
            __file__), '..', 'config', 'config.ini')
        config = configparser.ConfigParser()
        config['Login'] = {'Usuario': usuario, 'Recordar': str(recordar)}
        with open(ruta_config, 'w') as configfile:
            config.write(configfile)

    def cargar_config():
        ruta_config = os.path.join(os.path.dirname(
            __file__), '..', 'config', 'config.ini')
        config = configparser.ConfigParser()
        if os.path.exists(ruta_config):
            config.read(ruta_config)
            usuario_guardado = config.get('Login', 'Usuario')
            recordar = config.getboolean('Login', 'Recordar')
            return usuario_guardado, recordar
        return None, False

    def verificar_credenciales():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()
        recordar = recordar_var.get()

        try:
            ruta_db = os.path.join(os.path.dirname(
                __file__), '..', 'database', 'usuario.db')
            conn = sqlite3.connect(ruta_db)
            c = conn.cursor()
            c.execute(
                "SELECT * FROM usuarios WHERE usuario = ? AND contrasena = ?", (usuario, contrasena))
            resultado = c.fetchone()
            conn.close()

            if resultado:
                messagebox.showinfo("Login exitoso", "Bienvenido")
                guardar_config(
                    usuario, True) if recordar else guardar_config('', False)
                app.destroy()
                import main_app
                main_app.main()
            else:
                messagebox.showerror(
                    "Error de login", "Credenciales incorrectas")
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error de base de datos", f"Error: {e}")

    # Creación de GUI
    app = CTk()
    app.geometry("600x480+350+20")
    app.resizable(0, 0)
    app.config(bg="#010101")
    app.title("Inicio de Sesión")

    app.side_img_data, app.email_icon_data, app.password_icon_data = cargar_imagenes().values()

    # Creación de imágenes para los widgets
    side_img = CTkImage(dark_image=app.side_img_data,
                        light_image=app.side_img_data, size=(300, 480))
    email_icon = CTkImage(dark_image=app.email_icon_data,
                          light_image=app.email_icon_data, size=(20, 20))
    password_icon = CTkImage(dark_image=app.password_icon_data,
                             light_image=app.password_icon_data, size=(17, 17))

    # Configuración de la interfaz gráfica
    CTkLabel(master=app, text="", image=side_img).pack(
        expand=True, side="left")

    frame = CTkFrame(master=app, width=300, height=480, fg_color="#010101")
    frame.pack_propagate(0)
    frame.pack(expand=True, side="right")

    CTkLabel(master=frame, text="Bienvenido!", text_color="#601E88", anchor="w",
             justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    CTkLabel(master=frame, text="Inicia sesión en tu cuenta", text_color="#7E7E7E",
             anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="  Usuario:", text_color="#601E88", anchor="w", justify="left", font=(
        "Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
    entry_usuario = CTkEntry(master=frame, width=225, fg_color="#010101", border_color="#2cb67d",
                             border_width=1, text_color="#ffffff")
    entry_usuario.pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="  Contraseña:", text_color="#601E88", anchor="w", justify="left", font=(
        "Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
    entry_contrasena = CTkEntry(master=frame, width=225, fg_color="#010101", border_color="#2cb67d",
                                border_width=1, text_color="#ffffff", show="*")
    entry_contrasena.pack(anchor="w", padx=(25, 0))

    # Widget de botón para recordar los datos
    recordar_var = BooleanVar()
    checkbox = CTkCheckBox(master=frame, text="Recordarme", hover_color='#7f5af0',
                           border_color='#2cb67d', fg_color='#2cb67d', variable=recordar_var)
    checkbox.pack(anchor="w", padx=(25, 0), pady=(10, 0))

    # Cargar la configuración previa si existe
    usuario_guardado, recordar = cargar_config()
    if usuario_guardado:
        entry_usuario.insert(0, usuario_guardado)
        recordar_var.set(recordar)

    # Widgets de entrada y botón de inicio de sesión
    CTkButton(master=frame, text="INICIAR SESIÓN", fg_color="#010101", hover_color="#7f5af0", font=(
        "Arial Bold", 12), text_color="#ffffff", width=225, command=verificar_credenciales).pack(anchor="w", pady=(40, 0), padx=(25, 0))

    app.mainloop()

except Exception as e:
    # Captura cualquier excepción y escribe el error en el archivo de registro
    with open(archivo_errores, 'a') as f:
        traceback.print_exc(file=f)
