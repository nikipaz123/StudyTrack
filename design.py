import os
from PIL import Image, ImageTk
import tkinter as tk

def establecer_fondo(ventana):
    # Ruta base para los archivos
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Ruta de la imagen de fondo
    ruta_imagen = os.path.join(base_path, 'fondo_interfaz.png')

    # Abro la imagen y redimensiono al tamaño de la ventana
    imagen_original = Image.open(ruta_imagen)
    imagen_redimensionada = imagen_original.resize((1450, 800))  # Cambiar al tamaño de la ventana
    imagen_fondo = ImageTk.PhotoImage(imagen_redimensionada)  # Guardar la referencia

    # Creo un label con la imagen de fondo
    label_fondo = tk.Label(ventana, image=imagen_fondo)
    label_fondo.place(relwidth=1, relheight=1)  # Esto hace que la imagen ocupe toda la ventana

    # Mantengo la referencia a la imagen para evitar que sea recolectada por el garbage collector
    ventana.imagen_fondo = imagen_fondo

def fondo_texto(widgets, color):
    for widget in widgets:
        try:
            widget.config(bg=color)  # Intento cambiar el color de fondo
        except Exception:
            pass  # Ignoro cualquier error si el widget no soporta esta configuración (en IOS no se permite cambiar el color de los botones)
