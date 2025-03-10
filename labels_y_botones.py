import tkinter as tk

import tkinter as tk

def crear_titulo(ventana, texto, relx, rely, relwidth, relheight): 
    titulo = tk.Label(ventana, text=texto, font=("Arial", 16, "bold"))
    titulo.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
    return titulo  # Devuelve el título 

def crear_entrada_con_titulo(ventana, texto_titulo, relx_titulo, rely_titulo, relwidth_titulo, relx_entry, rely_entry, show=None): 
    titulo = tk.Label(ventana, text=texto_titulo)
    titulo.place(relx=relx_titulo, rely=rely_titulo, relwidth=relwidth_titulo, relheight=0.03)
    entrada = tk.Entry(ventana, show=show)
    entrada.place(relx=relx_entry, rely=rely_entry, relwidth=0.16, relheight=0.03)
    return entrada, titulo  # Devuelve  la entrada y el título

def crear_boton(ventana, texto, comando, relx, rely, relwidth, relheight): 
    boton = tk.Button(ventana, text=texto, command=comando)
    boton.place(relx=relx, rely=rely, relwidth=relwidth, relheight=relheight)
    return boton  # Devuelve el botón 



'''este archivo fue creado para evitar repetir código innecesariamente'''