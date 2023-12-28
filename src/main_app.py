import os
import datetime
import sqlite3
from tkinter import Frame, ttk, messagebox
from customtkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Producto:
    def __init__(self, dia, nombre, hora, precio, vendido):
        self.dia = dia
        self.nombre = nombre
        self.hora = hora
        self.precio = precio
        self.vendido = vendido
        self.ganancia = self.precio * self.vendido


# Conexión a la base de datos y creación de la tabla si no existe
ruta_db = os.path.join(os.path.dirname(__file__), '..',
                       'database', 'productos.db')
conn = sqlite3.connect(ruta_db)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        dia TEXT,
        nombre TEXT,
        hora TEXT,
        precio REAL,
        vendido INTEGER,
        ganancia REAL
    )
''')

# Funciones para manipular la base de datos y la interfaz gráfica


def limpiar_campos():
    dia_entry.delete(0, 'end')
    nombre_entry.delete(0, 'end')
    precio_entry.delete(0, 'end')
    vendido_entry.delete(0, 'end')


def agregar_producto():
    dia = dia_entry.get()
    nombre = nombre_entry.get()
    precio = float(precio_entry.get())
    vendido = int(vendido_entry.get())
    hora = datetime.datetime.now().strftime("%H:%M:%S")

    producto = Producto(dia, nombre, hora, precio, vendido)

    c.execute('''
        INSERT INTO productos (dia, nombre, hora, precio, vendido, ganancia)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (producto.dia, producto.nombre, producto.hora, producto.precio, producto.vendido, producto.ganancia))

    conn.commit()

    actualizar_tabla()
    limpiar_campos()
    messagebox.showinfo("Información", "Producto agregado correctamente")


def actualizar_tabla():
    for i in tabla.get_children():
        tabla.delete(i)

    c.execute('SELECT * FROM productos')
    productos = c.fetchall()

    for producto in productos:
        tabla.insert('', 'end', values=producto)


def eliminar_producto():
    selected_item = tabla.selection()[0]
    producto = tabla.item(selected_item)['values']

    c.execute('DELETE FROM productos WHERE dia = ? AND nombre = ? AND hora = ?',
              (producto[0], producto[1], producto[2]))

    conn.commit()

    actualizar_tabla()
    messagebox.showinfo("Información", "Producto eliminado correctamente")


def editar_producto():
    selected_item = tabla.selection()[0]
    producto = tabla.item(selected_item)['values']

    dia_entry.delete(0, 'end')
    dia_entry.insert(0, producto[0])
    nombre_entry.delete(0, 'end')
    nombre_entry.insert(0, producto[1])
    precio_entry.delete(0, 'end')
    precio_entry.insert(0, producto[3])
    vendido_entry.delete(0, 'end')
    vendido_entry.insert(0, producto[4])

    agregar_button.configure(
        text="Guardar cambios", command=lambda producto=producto: guardar_cambios(producto))


def guardar_cambios(producto_viejo):
    dia = dia_entry.get()
    nombre = nombre_entry.get()
    precio = float(precio_entry.get())
    vendido = int(vendido_entry.get())
    hora = datetime.datetime.now().strftime("%H:%M:%S")

    producto = Producto(dia, nombre, hora, precio, vendido)

    c.execute('''
        UPDATE productos
        SET dia = ?, nombre = ?, hora = ?, precio = ?, vendido = ?, ganancia = ?
        WHERE dia = ? AND nombre = ? AND hora = ?
    ''', (producto.dia, producto.nombre, producto.hora, producto.precio, producto.vendido, producto.ganancia, producto_viejo[0], producto_viejo[1], producto_viejo[2]))

    conn.commit()

    agregar_button.config(text="Agregar producto", command=agregar_producto)
    actualizar_tabla()
    messagebox.showinfo("Información", "Producto editado correctamente")


grafico_mostrado = False
grafico_figura = None
geometria_original = None


def mostrar_grafico():
    global grafico_mostrado, grafico_figura, geometria_original

    if grafico_mostrado:
        grafico_figura.get_tk_widget().destroy()
        grafico_mostrado = False
        if geometria_original:
            app.geometry(geometria_original)
    else:
        geometria_original = app.geometry()

        c.execute('SELECT * FROM productos')
        productos = c.fetchall()

        nombres = []
        ganancias = []

        for producto in productos:
            nombres.append(producto[1])
            ganancias.append(producto[5])

        fig = plt.Figure(figsize=(6, 5), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(nombres, ganancias)
        ax.set_title('Ganancias por producto')
        ax.set_xlabel('Producto')
        ax.set_ylabel('Ganancia')

        canvas = FigureCanvasTkAgg(fig, master=app)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=1, rowspan=3, padx=5, pady=5)

        grafico_figura = canvas
        grafico_mostrado = True

        app.geometry("1225x515")


# Configuración de la interfaz gráfica
app = CTk()
app.geometry("620x515+350+20")
app.resizable(0, 0)
app.config(bg="#010101")
app.title("EcoAnalyzer")

# Creación de los widgets de la interfaz gráfica
frame = Frame(master=app, bg="#010101")
frame.grid()

dia_label = CTkLabel(frame, text="Día:", text_color="#601E88",
                     anchor="w", justify="left", font=("Arial Bold", 14),)
dia_label.grid(row=0, column=0, padx=5, pady=5)
dia_entry = CTkEntry(frame, fg_color="#010101", border_color="#2cb67d",
                     border_width=1, text_color="#ffffff")
dia_entry.grid(row=0, column=1, padx=5, pady=5)

nombre_label = CTkLabel(frame, text="Nombre del producto:", text_color="#601E88",
                        anchor="w", justify="left", font=("Arial Bold", 14),)
nombre_label.grid(row=0, column=2, padx=5, pady=5)
nombre_entry = CTkEntry(frame, fg_color="#010101", border_color="#2cb67d",
                        border_width=1, text_color="#ffffff")
nombre_entry.grid(row=0, column=3, padx=5, pady=5)

precio_label = CTkLabel(frame, text="Precio del producto:", text_color="#601E88",
                        anchor="w", justify="left", font=("Arial Bold", 14),)
precio_label.grid(row=1, column=0, padx=5, pady=5)
precio_entry = CTkEntry(frame, fg_color="#010101", border_color="#2cb67d",
                        border_width=1, text_color="#ffffff")
precio_entry.grid(row=1, column=1, padx=5, pady=5)

vendido_label = CTkLabel(frame, text="Productos vendidos:", text_color="#601E88",
                         anchor="w", justify="left", font=("Arial Bold", 14),)
vendido_label.grid(row=1, column=2, padx=5, pady=5)
vendido_entry = CTkEntry(frame, fg_color="#010101", border_color="#2cb67d",
                         border_width=1, text_color="#ffffff")
vendido_entry.grid(row=1, column=3, padx=5, pady=5)

agregar_button = CTkButton(master=frame, text="Agregar producto", fg_color="#010101",
                           hover_color="#7f5af0", font=("Arial Bold", 12), text_color="#ffffff", width=112, command=agregar_producto)
agregar_button.grid(row=2, column=0, pady=5, padx=5)

eliminar_button = CTkButton(master=frame, text="Eliminar producto", fg_color="#010101",
                            hover_color="#7f5af0", font=("Arial Bold", 12), text_color="#ffffff", width=112, command=eliminar_producto)
eliminar_button.grid(row=2, column=1, pady=5, padx=5)

editar_button = CTkButton(master=frame, text="Editar producto", fg_color="#010101",
                          hover_color="#7f5af0", font=("Arial Bold", 12), text_color="#ffffff", width=112, command=editar_producto)
editar_button.grid(row=2, column=2, pady=5, padx=5)

grafico_button = CTkButton(master=frame, text="Mostrar gráfico", fg_color="#010101",
                           hover_color="#7f5af0", font=("Arial Bold", 12), text_color="#ffffff", width=112, command=mostrar_grafico)
grafico_button.grid(row=2, column=3, pady=5, padx=5)

frame2 = Frame(master=app, bg="#010101")
frame2.grid(row=1, column=0)

style = ttk.Style()
style.configure("Treeview", background="#7f5af0", fieldbackground="#010101")
style.configure("Treeview.Heading", background="#7f5af0")

tabla = ttk.Treeview(frame2, height=18, columns=(
    'Día', 'Nombre', 'Hora', 'Precio', 'Vendido', 'Ganancia'), show='headings')
tabla.grid()

for col in ('Día', 'Nombre', 'Hora', 'Precio', 'Vendido', 'Ganancia'):
    tabla.heading(col, text=col)
    tabla.column(col, width=100)

actualizar_tabla()

app.mainloop()

conn.close()
