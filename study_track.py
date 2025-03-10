import tkinter as tk
from tkinter import ttk
import ingresar
import pymysql
import bcrypt
import registrarse
import configuracion
from progreso import *
from audio import *
import feedback
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  
import mysql.connector
from mysql.connector import Error
import datetime
from sga_iniciar_session import *  
from notas_extra import * 
from design import *
from notas import *
from notificaciones import Notificaciones
from tkcalendar import Calendar
import csv
import os
from comisiones import *
from crear_db import *
from labels_y_botones import *
from formato_horas import *

# modifique sus datos de SQL
usuario_sql = 'root' 
contra_sql = '1234'  

class StudyTrack():
    def __init__(self,usuario_sql,contra_sql):
        self.usuario_sql = usuario_sql
        self.contra_sql = contra_sql
        self.ventana = tk.Tk()
        self.ventana.geometry('1600x800')
        crear_tablas(self.usuario_sql, self.contra_sql)
        self.inicio_sesion()
        self.ventana.mainloop()

    def inicio_sesion(self):
        establecer_fondo(self.ventana)
        
        # Título
        self.titulo = tk.Label(self.ventana, text="StudyTrack", font=('Futura', 30, 'bold'), bg="#B38F8F", fg='white')
        self.titulo.place(relx=0.4, rely=0.3, relwidth=0.2, relheight=0.1)
        
        # Entradas
        self.usuario, self.usuario_titulo = crear_entrada_con_titulo(self.ventana, "Mail", 0.32, 0.4, 0.07, 0.42, 0.4)
        self.password, self.password_titulo = crear_entrada_con_titulo(self.ventana, "Contraseña", 0.32, 0.46, 0.07, 0.42, 0.46, show='*')
        
        # Botón para mostrar la contraseña
        self.mostrar = tk.Button(self.ventana, text="\U0001F440", command=self.mostrar_contra, font=('Arial', 12))
        self.mostrar.place(relx=0.6, rely=0.46, relheight=0.03, relwidth=0.015)
        self.p = 0

        # Botones de acción
        self.acceder = crear_boton(self.ventana, "Acceder", self.entrar, 0.52, 0.55, 0.08, 0.03)
        self.ventana.bind('<Return>', lambda event: self.entrar())
        self.registro = crear_boton(self.ventana, "Registrarse", self.registrarse, 0.4, 0.55, 0.08, 0.03)
        self.recuperarcontra = crear_boton(self.ventana, "Olvidé mi contraseña", self.recuperar, 0.4, 0.6, 0.2, 0.03)
        
        # Creo las listas de botones y labels
        labels = [self.titulo, self.usuario_titulo, self.password_titulo]
        botones = [self.mostrar, self.acceder, self.registro, self.recuperarcontra]
        
        # Ca,bio el fondo de los labels y botones
        fondo_texto(labels, "#B38F8F")  # Color para las labels
        fondo_texto(botones, "#FFFFCC")  # Color para los botones
        
    def mostrar_contra(self):
        if self.p == 0:
            self.password.configure(show = '')
            self.p = 1
        elif self.p == 1:
            self.password.configure(show = '*')
            self.p = 0
            
    def entrar(self):  
        self.u = self.usuario.get().strip()
        self.passw = self.password.get()
        x = ingresar.ingresar(self.u, self.passw,self.usuario_sql,self.contra_sql)
        
        mensajes = {
            0: 'Ingrese su mail!',
            1: 'Ingrese su contraseña!',
            2: 'Inicio de sesion exitoso!',
            3: 'Usuario o contraseña incorrectos!',
            4: 'Error de formato en la contraseña almacenada!',
            5: 'Usuario no registrado!',
            6: 'Ocurrio un error!'
        }
        
        mensaje_texto = mensajes.get(x, 'Ocurrio un error!')
        
        self.mensaje = tk.Label(self.ventana, text = mensaje_texto)
        self.mensaje.place(relx = 0.6, rely = 0.40, relheight=0.05, relwidth=0.2)
        
        if x == 2:
            self.ventana_principal()
        
        fondo_texto([self.mensaje], color="#B38F8F")

            
    def recuperar(self):
        # Pido al usuario que ingrese su mail
        self.u = tk.Entry(self.ventana)
        self.u.place(relx = 0.4, rely = 0.66, relheight=0.03, relwidth=0.16)

        self.u_titulo = tk.Label(self.ventana, text = "Ingrese su mail")
        self.u_titulo.place(relx = 0.28, rely = 0.66, relheight=0.03, relwidth=0.07)
        
        # Pido al usuario que ingrese la palabra clave con la que se registró
        self.palabra_clave = tk.Entry(self.ventana)
        self.palabra_clave.place(relx=0.4, rely= 0.70, relheight=0.03, relwidth=0.16)
        
        self.palabra_clave_titulo = tk.Label(self.ventana, text= 'Ingrese su palabra clave')
        self.palabra_clave_titulo.place(relx=0.28, rely= 0.70, relheight=0.04, relwidth=0.11)
        
        self.confirmar = tk.Button(self.ventana, text='Aplicar', command = self.aplicar_recuperar)
        self.confirmar.place(relx=0.45, rely=0.8, relheight=0.05, relwidth=0.1)
        
        fondo_texto([self.u_titulo, self.palabra_clave_titulo], color="#B38F8F")  
        fondo_texto([self.confirmar], color="#FFFFCC")
        
    def aplicar_recuperar(self):
        # Obtén los valores ingresados
        mail = self.u.get()
        palabra_clave = self.palabra_clave.get()

        # Conectar a la base de datos
        try:
            conexion = pymysql.connect(host='127.0.0.1', port=3306, user=self.usuario_sql, password=self.contra_sql, database='studytrack')
            cursor = conexion.cursor()

            # Consulta para obtener el hash almacenado para el correo ingresado
            cursor.execute("SELECT palabra_clave FROM usuarios WHERE mail = %s", (mail,))
            resultado = cursor.fetchone()

            if resultado:
                hash_almacenado = resultado[0]

                # Verifica que la palabra clave ingresada es la correcta
                if bcrypt.checkpw(palabra_clave.encode('utf-8'), hash_almacenado.encode('utf-8')):
                    print("Palabra clave correcta")

                    # Oculta los campos de mail y palabra clave
                    self.u.place_forget()
                    self.u_titulo.place_forget()
                    self.palabra_clave.place_forget()
                    self.palabra_clave_titulo.place_forget()
                    self.confirmar.place_forget()

                    # Llama al método para mostrar los campos de cambio de contraseña
                    self.cambiar_pass()
                else:
                    messagebox.showerror("Error", "Palabra clave incorrecta")
            else:
                messagebox.showerror("Error", "Ese mail no está registrado")
        except Exception as e:
            messagebox.showerror("Error", f"Error al conectar con la base de datos: {e}")
        finally:
            conexion.close()
                        
    def registrarse(self):
        establecer_fondo(self.ventana)
        
        # Crear el título
        self.titulo = crear_titulo(self.ventana, "Registro", 0.4, 0.18, 0.2, 0.1)
        
        # Crear las entradas y etiquetas
        self.nombre, self.nombre_titulo = crear_entrada_con_titulo(self.ventana, "Nombre", 0.32, 0.28, 0.07, 0.42, 0.28)
        self.apellido, self.apellido_titulo = crear_entrada_con_titulo(self.ventana, "Apellido", 0.32, 0.34, 0.07, 0.42, 0.34)
        self.usuario, self.usuario_titulo = crear_entrada_con_titulo(self.ventana, "Mail", 0.32, 0.4, 0.07, 0.42, 0.4)
        self.password, self.password_titulo = crear_entrada_con_titulo(self.ventana, "Contraseña", 0.32, 0.46, 0.07, 0.42, 0.46)
        self.new_password, self.new_password_titulo = crear_entrada_con_titulo(self.ventana, 'Confirmar Contraseña', 0.31, 0.52, 0.1, 0.42, 0.52)
        self.palabra_clave, self.palabra_clave_titulo = crear_entrada_con_titulo(self.ventana, 'Palabra clave', 0.31, 0.58, 0.1, 0.42, 0.58)

        # Crear listas de widgets
        textos = [self.titulo , self.nombre_titulo, self.apellido_titulo, self.usuario_titulo, self.password_titulo, self.new_password_titulo, self.palabra_clave_titulo]
        entradas = [self.nombre, self.apellido, self.usuario, self.password, self.new_password, self.palabra_clave]
        
        # Cambiar el fondo de las etiquetas y las entradas
        fondo_texto(textos, color="#B38F8F")  # Labels (rosita)
        fondo_texto(entradas, color="#B38F8F")  # Entradas (rosita)
        
        # Crear los botones
        self.registro = tk.Button(self.ventana, command=self.registrar, text='Registrarse')
        self.registro.place(relx=0.52, rely=0.66, relheight=0.03, relwidth=0.08)
        
        self.acceder = tk.Button(self.ventana, command=self.inicio_sesion, text="Iniciar Sesion")
        self.acceder.place(relx=0.4, rely=0.66, relheight=0.03, relwidth=0.08)
        
        # Crear lista de botones
        botones = [self.registro, self.acceder]
        fondo_texto(botones, color="#FFFFCC")  # Botones (amarillo claro)

        
    def registrar(self):
        nom = self.nombre.get()
        ape = self.apellido.get()
        u = self.usuario.get().strip()
        p = self.password.get()
        confirmar = self.new_password.get()
        c = self.palabra_clave.get()
        x = registrarse.registrarse(nom, ape, u, p, confirmar, c, self.usuario_sql, self.contra_sql)
        
        # Diccionario con los mensajes específicos para cada valor de x
        mensajes = {
            13: 'Registro exitoso!',
            14: 'El apellido ingresado es demasiado largo',
            15: 'El nombre ingresado es demasiado largo',
            3: 'La contraseña debe tener al menos 8 caracteres!',
            4: 'La contraseña debe tener al menos una letra mayuscula!',
            5: 'La contraseña debe contener al menos un numero!',
            8: 'Las contraseñas no coinciden!',
            10: 'Este mail ya esta registrado para una cuenta existente!',
            11: 'Error inesperado!',
            12: 'El mail no es valido!'
        }
        
        # Lista de valores de x que tienen el mensaje común "Complete los campos vacios!"
        campos_vacios = [0, 1, 2, 6, 7, 9]

        # Si x está en campos_vacios, asigna el mensaje correspondiente
        if x in campos_vacios:
            mensaje_texto = 'Complete los campos vacios!'
        else:
            mensaje_texto = mensajes.get(x, 'Error desconocido!')
        
        # Mostrar el mensaje
        self.mensaje = tk.Label(self.ventana, text = mensaje_texto)
        self.mensaje.place(relx = 0.58, rely=0.37, relheight=0.1, relwidth=0.2)
        
        fondo_texto([self.mensaje], color="#B38F8F")

    def ventana_principal(self):
        establecer_fondo(self.ventana)
        carpeta = "StudyTrack"
        self.archivo_csv = os.path.join(carpeta, f"fechas_tareas_{self.u}.csv")
        
        # Crear la carpeta si no existe
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        # Definir los botones 
        font_style = ('Arial', 12, 'bold')

        # Crear los botones con sus comandos
        self.configuracion = tk.Button(self.ventana, command=self.ventana_config, text="Configuración\nperfil", font=font_style)
        self.menu_opciones = tk.Button(self.ventana, command=self.ventana_menu_materias, text='Menú de Opciones', font=font_style)
        self.feedback = tk.Button(self.ventana, command=self.dar_feedback, text='Dejar mi opinión', font=font_style)
        self.cerrar_sesion = tk.Button(self.ventana, command=self.inicio_sesion, text='Cerrar Sesión', font=font_style)
        self.ir_calendario = tk.Button(self.ventana, command=self.ventana_calendario, text='Calendario', font=font_style)
        self.anotar_tareas = tk.Button(self.ventana, command=self.tareas, text='Tareas', font=font_style)

        # Configurar el tamaño y la ubicación de los botones
        button_width = 0.25  # Ancho relativo del botón
        button_height = 0.08  # Alto relativo del botón

        # Espaciado entre botones
        vertical_spacing = 0.1  # Espaciado vertical entre los botones

        # Posicionar los botones usando un bucle
        botones = [
            self.menu_opciones,
            self.anotar_tareas,
            self.ir_calendario,
            self.feedback,
            self.configuracion,
            self.cerrar_sesion
        ]

        # Calcular posición inicial
        start_y = 0.2  # Posición inicial en el eje Y (relativo al alto de la ventana)

        for idx, boton in enumerate(botones):
            boton.place(
                relx=0.5,  # Centrar horizontalmente
                rely=start_y + idx * vertical_spacing,  # Incrementar la posición vertical
                relwidth=button_width,  # Ancho del botón
                relheight=button_height,  # Alto del botón
                anchor="n"  # Anclar desde el centro superior
            )

        # Aplicar fondo a los botones
        fondo_texto(botones, color="#FFFFCC")  


    def tareas(self):
        establecer_fondo(self.ventana)
        
        # Campo de selección de fechas
        self.seleccionar = tk.StringVar()
        self.calendario = DateEntry(self.ventana, selectmode='day', textvariable=self.seleccionar)
        self.calendario.place(relx = 0.45, rely = 0.35, relheight = 0.03, relwidth = 0.1)
        
        # Campo para ingresar la tarea
        tk.Label(self.ventana, text="Tarea/Evento:").place(relx=0.3, rely = 0.45, relheight=0.03, relwidth=0.08)
        self.tarea_var = tk.StringVar()
        entrada_tarea = tk.Entry(self.ventana, textvariable=self.tarea_var, width=30)
        entrada_tarea.place(relx=0.4, rely=0.45, relheight=0.03, relwidth=0.2)
        
        # Botones
        boton_guardar = tk.Button(self.ventana, text="Guardar Tarea", command=self.guardar_fecha_tarea, bg="green")
        boton_guardar.place(relx=0.35, rely=0.55, relheight=0.05, relwidth=0.1)

        boton_borrar = tk.Button(self.ventana, text="Borrar Ultima Tarea", command=self.borrar_fecha_tarea, bg="red")
        boton_borrar.place(relx=0.55, rely=0.55, relheight=0.05, relwidth=0.12)
        
        #mensaje
        self.mensaje = tk.Label(self.ventana, text="", fg="black")
        self.mensaje.place(relx=0.4, rely=0.65, relheight=0.05, relwidth=0.2)
        fondo_texto([self.mensaje], color="#b38f8f")
        
        self.volver = tk.Button(self.ventana, text='Menu Inicial', command=self.ventana_principal, font=('Arial', 12, 'bold'), bg="#ffffcc")
        self.volver.place(relx=0.5, rely=0.03, anchor="n", relheight=0.1, relwidth=0.1)
        
        fondo_texto([tk.Label] , color="#B38F8F")
        fondo_texto([boton_borrar, boton_guardar] , color="#FFFFCC")

    def guardar_fecha_tarea(self):
        fecha = self.seleccionar.get()
        tarea = self.tarea_var.get().strip()  # Elimina espacios antes y después del texto

        if not tarea:
            self.mensaje.config(text="Por favor, escribe una tarea.", fg="red")
            return

        # Verificar si el archivo ya existe y leer las entradas existentes
        entradas_existentes = []
        if os.path.exists(self.archivo_csv):
            with open(self.archivo_csv, mode="r") as archivo:
                reader = csv.reader(archivo)
                entradas_existentes = list(reader)

        # Verificar si ya existe la combinación de fecha y tarea
        if [fecha, tarea] not in entradas_existentes:
            with open(self.archivo_csv, mode="a", newline="") as archivo:
                writer = csv.writer(archivo)
                writer.writerow([fecha, tarea])
            self.mensaje.config(text=f"Tarea guardada: {tarea} ({fecha})", fg="green")
        else:
            self.mensaje.config(text="Esta tarea ya está registrada para esa fecha.", fg="orange")
        
    def borrar_fecha_tarea(self):
        fecha = self.seleccionar.get()
        tarea = self.tarea_var.get().strip()

        if not os.path.exists(self.archivo_csv):
            self.mensaje.config(text="No hay tareas registradas para borrar.", fg="red")
            return

        # Leer todas las entradas del archivo
        with open(self.archivo_csv, mode="r") as archivo:
            reader = csv.reader(archivo)
            entradas = list(reader)

        # Eliminar la combinación de fecha y tarea si existe
        nuevas_entradas = [entrada for entrada in entradas if entrada != [fecha, tarea]]

        if len(entradas) == len(nuevas_entradas):
            self.mensaje.config(text="Tarea no encontrada para borrar.", fg="red")
        else:
            # Reescribir el archivo con las entradas restantes
            with open(self.archivo_csv, mode="w", newline="") as archivo:
                writer = csv.writer(archivo)
                writer.writerows(nuevas_entradas)
            self.mensaje.config(text=f"Tarea borrada: {tarea} ({fecha})", fg="green")
            

    def ventana_calendario(self):
        establecer_fondo(self.ventana)

        self.volver = tk.Button(self.ventana, text='Menu Inicial', command=self.ventana_principal, font=('Arial', 12, 'bold'), bg="#ffffcc")
        self.volver.place(relx=0.5, rely=0.03, anchor="n", relheight=0.1, relwidth=0.1)

        # Calendario
        self.calendario = Calendar(self.ventana, selectmode="day")
        self.calendario.place(relx=0.185, rely=0.2, relheight=0.3, relwidth=0.2)
        
        # Te lleva a mostrar_tarea_dia
        self.calendario.bind("<<CalendarSelected>>", self.mostrar_tarea_dia)

        # Frame para la tabla y la scrollbar
        frame_tabla = tk.Frame(self.ventana)
        frame_tabla.place(relx=0.4, rely=0.2, relheight=0.5, relwidth=0.4)

        # Armo la tabla
        self.tabla = ttk.Treeview(frame_tabla, columns=("Fecha", "Tarea"), show="headings")
        self.tabla.heading("Fecha", text="Fecha")
        self.tabla.heading("Tarea", text="Tarea")
        self.tabla.column("Fecha", width=100, anchor="center")
        self.tabla.column("Tarea", width=200, anchor="w")
        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar vertical
        scrollbar_vertical = tk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tabla.yview)
        scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)

        # Asociar la scrollbar al Treeview
        self.tabla.configure(yscrollcommand=scrollbar_vertical.set)

        boton_recargar = tk.Button(self.ventana, text="Mostrar Tareas", command=self.cargar_datos, bg="blue", fg="white")
        boton_recargar.place(relx=0.1825, rely=0.575, relheight=0.05, relwidth=0.08)

        boton_borrar = tk.Button(self.ventana, text="Borrar Tarea", command=self.borrar_tarea, bg="red", fg="white")
        boton_borrar.place(relx=0.3075, rely=0.575, relheight=0.05, relwidth=0.08)

        self.texto = tk.Label(self.ventana, text="", bg= '#B38F8F')
        self.texto.place(relx=0.1825, rely=0.7, relheight=0.05, relwidth=0.2)

        botones = [self.volver]
        fondo_texto(botones, color="#FFFFCC")

        # Cargar tareas y destacar días en el calendario
        self.destacar_dias()

    def cargar_datos(self):
        # Limpiar la tabla antes de cargar datos
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Verificar si el archivo existe
        if os.path.exists(self.archivo_csv):
            with open(self.archivo_csv, mode="r") as archivo:
                reader = csv.reader(archivo)
                for fila in reader:
                    # Añadir cada fila a la tabla
                        if len(fila) == 2:  
                            self.tabla.insert("", "end", values=(fila[0], fila[1]))
        else:
            self.texto.config(text=f"No tiene tareas", fg="red")
        self.destacar_dias()
        
    def borrar_tarea(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            self.texto.config(text="Por favor, selecciona una tarea para borrar.", fg="red")
            return

        valores = self.tabla.item(seleccion[0], "values")
        fecha, tarea = valores
        self.tabla.delete(seleccion[0])

        # Leer todas las entradas del archivo y excluir la borrada
        nuevas_entradas = []
        if os.path.exists(self.archivo_csv):
            with open(self.archivo_csv, mode="r") as archivo:
                reader = csv.reader(archivo)
                nuevas_entradas = [fila for fila in reader if fila != [fecha, tarea]]

        # Sobrescribir el archivo con las nuevas entradas
        with open(self.archivo_csv, mode="w", newline="") as archivo:
            writer = csv.writer(archivo)
            writer.writerows(nuevas_entradas)

        self.destacar_dias()

        self.texto.config(text=f"Tarea '{tarea}' eliminada.", fg="green")
        
    def mostrar_tarea_dia(self, event):
        fecha_seleccionada = self.calendario.get_date()
            
        # Armo el espacio para que se vean las tareas del dia
        frame_tareas = tk.Frame(self.ventana)
        frame_tareas.place(relx=0.1825, rely=0.7, relheight=0.2, relwidth=0.6)

        # Barrita
        scrollbar = tk.Scrollbar(frame_tareas)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Mensaje
        self.texto_cal = tk.Text(frame_tareas, wrap=tk.WORD, yscrollcommand=scrollbar.set, bg="#B38F8F", fg="black")
        self.texto_cal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.texto_cal.yview)  # Agrega la barrita al texto

        # Si no hay nada
        self.texto_cal.tag_configure("rojo", foreground="red")
        
        # Buscar si hay una tarea asociada a esa fecha
        tarea_encontrada = []
        if os.path.exists(self.archivo_csv):
            with open(self.archivo_csv, mode="r") as archivo:
                reader = csv.reader(archivo)
                for fila in reader:
                    if len(fila) == 2 and fila[0] == fecha_seleccionada:
                        tarea_encontrada.append(fila[1])

        # Mostrar las tareas en el self.text_cal
        if tarea_encontrada:
            for i, tarea in enumerate(tarea_encontrada, 1):
                self.texto_cal.insert(tk.END, f"{i}. {tarea}\n")
        else:
            self.texto_cal.insert(tk.END, "No hay tareas para este día.", "rojo")


    def destacar_dias(self):
        # Verifica si el archivo existe
        if not os.path.exists(self.archivo_csv):
            return

        # Elimina todos los eventos existentes del calendario
        self.calendario.calevent_remove(tag="tarea")

        # Lee las fechas con tareas desde el archivo
        dias_con_tareas = set()
        with open(self.archivo_csv, mode="r") as archivo:
            reader = csv.reader(archivo)
            for fila in reader:
                if len(fila) == 2:  
                    dias_con_tareas.add(fila[0])

        # Recorre los días del calendario y cambia el cloor si hay una tarea
        for dia in dias_con_tareas:
            try:
                # Convierte la fecha de formato mm/dd/yy a un objeto datetime
                fecha_objeto = datetime.datetime.strptime(dia, "%m/%d/%y")
                self.calendario.calevent_create(fecha_objeto, "Tarea", "tarea")
            except ValueError:
                continue

        self.calendario.tag_config("tarea", background="lightgreen", foreground="black")

    
        
    def ventana_config(self):
        establecer_fondo(self.ventana)

        self.titulo = tk.Label(self.ventana, text='Configuracion', font=("", 20, "bold"), fg="white", bg='#B38F8F')
        self.titulo.place(relx = 0.4, rely = 0.22, relwidth = 0.2, relheight= 0.1)

        self.volver = tk.Button(self.ventana, text='Menu Inicial', command=self.ventana_principal, font=('Arial', 12, 'bold'), bg="#ffffcc")
        self.volver.place(relx=0.5, rely=0.03, anchor="n", relheight=0.1, relwidth=0.1)

        self.contra = crear_boton(self.ventana, 'Modificar Contraseña', self.cambiar_pass, 0.225, 0.4, 0.1, 0.1)
        self.nombre = crear_boton(self.ventana, 'Modificar Nombre', self.cambiar_nombre, 0.375, 0.4, 0.1, 0.1)
        self.apellido = crear_boton(self.ventana, 'Modificar Apellido', self.cambiar_apellido, 0.525, 0.4, 0.1, 0.1)
        self.usuario = crear_boton(self.ventana, 'Modificar Mail', self.cambiar_usuario, 0.675, 0.4, 0.1, 0.1)
        
        self.informacion1 = tk.Entry(self.ventana)
        self.informacion_texto1 = tk.Label(self.ventana, text = 'Nueva Contraseña')
        self.informacion2 = tk.Entry(self.ventana)
        self.informacion_texto2 = tk.Label(self.ventana, text = 'Confirmar Contraseña')
        

        botones = [self.contra, self.nombre, self.apellido, self.usuario, self.volver]
        fondo_texto(botones, color="#FFFFCC")  

        etiquetas = [self.titulo, self.informacion_texto1, self.informacion_texto2]
        fondo_texto(etiquetas, color="#B38F8F") 
        
    def cambiar_pass(self): 
        self.informacion1 = tk.Entry(self.ventana)
        self.informacion1.place(relx=0.4, rely= 0.6, relheight=0.04, relwidth=0.2)
        
        self.informacion_texto1 = tk.Label(self.ventana, text = 'Nueva Contraseña')
        self.informacion_texto1.place(relx=0.3, rely=0.6, relheight=0.04, relwidth=0.1)
        
        self.informacion2 = tk.Entry(self.ventana)
        self.informacion2.place(relx=0.4, rely= 0.7, relheight=0.04, relwidth=0.2)
        
        self.informacion_texto2 = tk.Label(self.ventana, text = 'Confirmar Contraseña')
        self.informacion_texto2.place(relx=0.3, rely=0.7, relheight=0.04, relwidth=0.1)
        
        self.mensaje = tk.Label(self.ventana, text = '')
        self.mensaje.place(relx= 0.6, rely=0.6, relheight=0, relwidth=0)
        
        self.confirmar = tk.Button(self.ventana, text='Aplicar', command = self.aplicar_contra)
        self.ventana.bind('<Return>', lambda event: self.aplicar_contra())
        self.confirmar.place(relx=0.45, rely=0.8, relheight=0.05, relwidth=0.1)
        
        botones = [self.confirmar]
        fondo_texto(botones, color="#FFFFCC")  

        etiquetas = [self.informacion_texto1, self.informacion_texto2]
        fondo_texto(etiquetas, color="#B38F8F")

    def aplicar_contra(self):    
       # Defino los mensajes según el código de error
        mensajesCondiciones = {
           '0': 'La contraseña debe tener al menos 8 caracteres!',
           '1': 'La contraseña debe contener al menos una letra mayúscula!',
           '2': 'La contraseña debe contener al menos un número!',
           '3': 'Contraseña no nula!',
           '4': 'Las contraseñas deben coincidir!',
        }

        mensajesCambioContrasenia = {
           '5': 'Cambio de contraseña realizado con éxito!',
           '6': 'Ocurrió un error al actualizar su contraseña!'
        }
        
        if isinstance(self.u, str):
            # Si es un str es pq está en configuracion
            mail = self.u
        else:
            # Si no es un str es pq está en recuperar contraseña
            mail = self.u.get()

        self.x = list(configuracion.modificar_contra(mail, self.informacion1.get(), self.informacion2.get(), self.usuario_sql, self.contra_sql))
        mensajeMostrado = ''
        for mensaje in mensajesCondiciones:
            if mensaje in self.x:
                mensajeMostrado += '❌' + f'{mensajesCondiciones[f'{mensaje}'] }\n'
            else:
                mensajeMostrado += '✔️' + f'{mensajesCondiciones[f'{mensaje}'] }\n'

        # Mostrar el mensaje de éxito o error general
        if '5' in self.x:  # Contraseña válida
            mensajeMostrado += f'{mensajesCambioContrasenia[f'{'5'}']}\n'
        elif '6' in self.x:  # Error al cambiar la contraseña
            mensajeMostrado += f'{mensajesCambioContrasenia[f'{'6'}']}\n'


        self.mensaje = tk.Label(self.ventana, text = mensajeMostrado)
        self.mensaje.place(relx= 0.63, rely=0.6, relheight=0.15, relwidth=0.24)
        self.ventana.after(5000, lambda: self.mensaje.place_forget())
                
        
        fondo_texto([self.mensaje], color="White")  

    def cambiar_nombre(self):
        self.informacion1 = tk.Entry(self.ventana)
        self.informacion1.place(relx=0.4, rely= 0.6, relheight=0.04, relwidth=0.2)
        
        self.informacion_texto1 = tk.Label(self.ventana, text = 'Nuevo nombre')
        self.informacion_texto1.place(relx=0.3, rely=0.6, relheight=0.04, relwidth=0.1)
        
        self.informacion2.place(relx=0.4, rely= 0.7, relheight=0, relwidth=0)
        
        self.informacion_texto2.place(relx=0.3, rely=0.7, relheight=0, relwidth=0)
        
        self.mensaje = tk.Label(self.ventana, text = '')
        self.mensaje.place(relx= 0.6, rely=0.6, relheight=0, relwidth=0)
        
        self.confirmar = tk.Button(self.ventana, text='Aplicar', command = self.aplicar_nombre)
        self.ventana.bind('<Return>', lambda event: self.aplicar_nombre())
        self.confirmar.place(relx=0.45, rely=0.8, relheight=0.05, relwidth=0.1)
        
        botones = [self.confirmar]
        fondo_texto(botones, color="#FFFFCC")  

        etiquetas = [self.informacion_texto1]
        fondo_texto(etiquetas, color="#B38F8F")
        
    def aplicar_nombre(self):
        self.x = configuracion.modificar_nombre(self.u, self.informacion1.get(), self.usuario_sql, self.contra_sql)
        
        if self.x == 0:
            self.mensaje = tk.Label(self.ventana, text = 'Ingrese su nuevo nombre!')
            self.mensaje.place(relx= 0.63, rely=0.595, relheight=0.05, relwidth=0.15)
            self.ventana.after(1000, lambda: self.mensaje.place_forget())
            
        if self.x == 1:
            self.mensaje = tk.Label(self.ventana, text = 'Cambio de nombre realizado con éxito!')
            self.mensaje.place(relx= 0.63, rely=0.595, relheight=0.05, relwidth=0.15)
            self.ventana.after(1000, lambda: self.mensaje.place_forget())
            
        if self.x == 2:
            self.mensaje = tk.Label(self.ventana, text = 'Ocurrió un error al actualizar su nombre!')
            self.mensaje.place(relx= 0.63, rely=0.595, relheight=0.05, relwidth=0.15)
            self.ventana.after(1000, lambda: self.mensaje.place_forget())
            
        fondo_texto([self.mensaje], color="White")
            
    def cambiar_apellido(self):
        self.informacion1 = tk.Entry(self.ventana)
        self.informacion1.place(relx=0.4, rely= 0.6, relheight=0.04, relwidth=0.2)
        
        self.informacion_texto1 = tk.Label(self.ventana, text = 'Nuevo apellido')
        self.informacion_texto1.place(relx=0.3, rely=0.6, relheight=0.04, relwidth=0.1)
        
        self.informacion2.place(relx=0.4, rely= 0.7, relheight=0, relwidth=0)
        
        self.informacion_texto2.place(relx=0.3, rely=0.7, relheight=0, relwidth=0)
        
        self.mensaje = tk.Label(self.ventana, text = '')
        self.mensaje.place(relx= 0.6, rely=0.6, relheight=0, relwidth=0)
        
        self.confirmar = tk.Button(self.ventana, text='Aplicar', command = self.aplicar_apellido)
        self.ventana.bind('<Return>', lambda event: self.aplicar_apellido())
        self.confirmar.place(relx=0.45, rely=0.8, relheight=0.05, relwidth=0.1)
        
        fondo_texto([self.informacion_texto1], color="#B38F8F")
        fondo_texto([self.confirmar], color="#FFFFCC")
        
    def aplicar_apellido(self):
        self.x = configuracion.modificar_apellido(self.u, self.informacion1.get(), self.usuario_sql, self.contra_sql)
        
        messages = {
            0: 'Ingrese su nuevo apellido!',
            1: 'Cambio de apellido realizado con éxito!',
            2: 'Ocurrió un error al actualizar su apellido!'
        }

        # Verifica si self.x tiene un mensaje asociado y lo muestra
        if self.x in messages:
            self.mensaje = tk.Label(self.ventana, text=messages[self.x])
            self.mensaje.place(relx=0.63, rely=0.595, relheight=0.05, relwidth=0.15)
            self.ventana.after(1000, lambda: self.mensaje.place_forget())
                    
        fondo_texto([self.mensaje], color="White") 
        
    def cambiar_usuario(self):
        self.informacion1 = tk.Entry(self.ventana)
        self.informacion1.place(relx=0.4, rely= 0.6, relheight=0.04, relwidth=0.2)
        
        self.informacion_texto1 = tk.Label(self.ventana, text = 'Nuevo mail')
        self.informacion_texto1.place(relx=0.3, rely=0.6, relheight=0.04, relwidth=0.1)
        
        self.informacion2.place(relx=0.4, rely= 0.7, relheight=0, relwidth=0)
        
        self.informacion_texto2.place(relx=0.3, rely=0.7, relheight=0, relwidth=0)
        
        self.mensaje = tk.Label(self.ventana, text = '')
        self.mensaje.place(relx= 0.6, rely=0.6, relheight=0, relwidth=0)
        
        self.confirmar = tk.Button(self.ventana, text='Aplicar', command = self.aplicar_usuario)
        self.ventana.bind('<Return>', lambda event: self.aplicar_usuario())
        self.confirmar.place(relx=0.45, rely=0.8, relheight=0.05, relwidth=0.1)
        
        fondo_texto([self.informacion_texto1], color="#B38F8F")
        fondo_texto([self.confirmar], color="#FFFFCC")
        
    def aplicar_usuario(self):
        self.x = configuracion.modificar_mail(self.u, self.informacion1.get(), self.usuario_sql, self.contra_sql)
    
        mensajes = {
            0: 'Ingrese su nuevo mail!',
            1: 'Cambio de mail realizado con éxito!',
            2: 'Este mail ya esta asociado a una cuenta!',
            3: 'Ocurrió un error al actualizar su mail!'
        }
        
        mensaje_texto = mensajes.get(self.x, 'Opción no válida')
        
        self.mensaje = tk.Label(self.ventana, text=mensaje_texto)
        self.mensaje.place(relx=0.64, rely=0.6, relheight=0.05, relwidth=0.15)
        self.ventana.after(1000, lambda: self.mensaje.place_forget())
        
        if self.x == 1:
            self.u = self.informacion1.get()
       
        fondo_texto([self.mensaje], color="White") 
    
    def dar_feedback(self):
        feedback.Feedback(self.usuario_sql, self.contra_sql, self.ventana) 
        
    def ventana_menu_materias(self):
        # Configuración inicial
        base_path = os.path.dirname(os.path.abspath(__file__)) # IMPORTANTE: como el fondo es distinto y la funcionestablecer_fondo ya estaba creada y llamada varias veces, definimos manualmente el fondo aca. 

        # Ruta de la imagen de fondo
        ruta_imagen = os.path.join(base_path, 'fondo_interfaz2.png')

        # Abro la imagen y redimensiono al tamaño de la ventana
        imagen_original = Image.open(ruta_imagen)
        imagen_redimensionada = imagen_original.resize((1450, 800))  # Cambiar al tamaño de la ventana
        imagen_fondo = ImageTk.PhotoImage(imagen_redimensionada)  # Guardar la referencia

        # Creo un label con la imagen de fondo
        label_fondo = tk.Label(self.ventana, image=imagen_fondo)
        label_fondo.place(relwidth=1, relheight=1)  # Esto hace que la imagen ocupe toda la ventana

        # Mantengo la referencia a la imagen para evitar que sea recolectada por el garbage collector
        self.ventana.imagen_fondo = imagen_fondo

        connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user=self.usuario_sql,
            password=self.contra_sql,
            database='studytrack'
        )
        with connection.cursor() as cursor:
            sql = "SELECT * FROM usuarios WHERE mail = %s"
            cursor.execute(sql, (self.u,))
            result = cursor.fetchone()
        self.id_u = result[0]

        # Configurar la cuadrícula de la ventana
        self.ventana.grid_columnconfigure(0, weight=1)  # Margen izquierdo
        self.ventana.grid_columnconfigure(5, weight=1)  # Margen derecho
        self.ventana.grid_rowconfigure(0, weight=1)     # Margen superior
        self.ventana.grid_rowconfigure(4, weight=1)     # Margen inferior

        # Título principal más grande y más arriba
        self.ventana.grid_rowconfigure(0, weight=2)  # Espacio superior (más peso)
        self.ventana.grid_rowconfigure(1, weight=1)  # Espacio entre título y botones

        self.titulo = tk.Label(self.ventana, text='Menú de Opciones', font=("", 20, "bold"), fg="white", bg='#B38F8F')
        self.titulo.place(relx = 0.4, rely = 0.22, relwidth = 0.2, relheight= 0.1)

        self.volver = tk.Button(self.ventana, text='Menu Inicial', command=self.ventana_principal, font=('Arial', 12, 'bold'), bg="#ffffcc")
        self.volver.place(relx=0.5, rely=0.03, anchor="n", relheight=0.1, relwidth=0.1)
        

        # Botones organizados en una cuadrícula
        botones = [
            ("Mis Materias", self.ventana_mis_materias),
            ("Ver Cronograma", self.ventana_ver_cronograma),
            ("Organizar Cronograma", self.ventana_organizar_cronograma),
            ("Cronómetro", self.ver_cronometro),
            ("Gráficos", self.ver_graficos),
            ("Rachas", self.ver_rachas),
            ("Analizar notas", self.analizar_notas)
        ]

        # Ajustar tamaño de botones y colocar en la cuadrícula
        for idx, (texto, comando) in enumerate(botones):
            fila = idx // 4 + 2  # Botones en filas 2 y 3
            columna = idx % 4 + 1  # Botones en columnas 1 a 4
            boton = tk.Button(self.ventana, text=texto, command=comando, font=('Arial', 12, 'bold'), bg="#ffffcc", width=20, height=3)
            boton.grid(row=fila, column=columna, padx=10, pady=10)  # Espaciado uniforme

        # Configurar filas y columnas para centrar los botones en el rectángulo
        for i in range(5):  # Configura todas las filas y columnas
            self.ventana.grid_rowconfigure(i, weight=0)
            self.ventana.grid_columnconfigure(i, weight=0)

        # Márgenes para centrar los botones dentro del área rosa
        self.ventana.grid_rowconfigure(0, weight=1)  # Espacio superior
        self.ventana.grid_rowconfigure(4, weight=1)  # Espacio inferior
        self.ventana.grid_columnconfigure(0, weight=1)  # Espacio izquierdo
        self.ventana.grid_columnconfigure(5, weight=1)  # Espacio derecho


    def ver_notas(self):
        try:
            connection = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user=self.usuario_sql,
                password=self.contra_sql,
                database='studytrack'
            )
            
            cursor = connection.cursor()
            
            # Crea la ventana para visualizar las notas
            ventana_notas = tk.Toplevel()
            ventana_notas.title("Notas")
            ventana_notas.geometry("800x600")
            
            # Arma los bordes de las tablas
            frame_notas = tk.Frame(ventana_notas)
            frame_notas.pack(pady=10, padx=10, fill='both', expand=True)
            
            frame_notas_extra = tk.Frame(ventana_notas)
            frame_notas_extra.pack(pady=10, padx=10, fill='both', expand=True)
            
            # Títulos
            tk.Label(frame_notas, text="Notas Regulares", font=('Arial', 12, 'bold')).pack()
            tk.Label(frame_notas_extra, text="Notas Extra", font=('Arial', 12, 'bold')).pack()
            
            # Obtiene las notas regulares de las tablas de sql
            cursor.execute("""
                SELECT materia, nota_cursada, nota_final 
                FROM notas 
                WHERE idusuarios = %s
                ORDER BY materia
            """, (self.id_u,))
            
            notas_regulares = cursor.fetchall()
            
            # Arma la tabla de notas regulares
            tree_notas = ttk.Treeview(frame_notas, columns=('Materia', 'Nota Cursada', 'Nota Final'), show='headings')
            tree_notas.heading('Materia', text='Materia')
            tree_notas.heading('Nota Cursada', text='Nota Cursada')
            tree_notas.heading('Nota Final', text='Nota Final')
            
            # Ancho de las columnas
            tree_notas.column('Materia', width=200)
            tree_notas.column('Nota Cursada', width=150)
            tree_notas.column('Nota Final', width=150)
            
            # Barrita para scrollear las notas
            scrollbar_notas = ttk.Scrollbar(frame_notas, orient='vertical', command=tree_notas.yview)
            tree_notas.configure(yscrollcommand=scrollbar_notas.set)
            
            tree_notas.pack(side='left', fill='both', expand=True)
            scrollbar_notas.pack(side='right', fill='y')
            
            # Ingresa la info
            for nota in notas_regulares:
                tree_notas.insert('', 'end', values=nota)

            # Calcula los promedios para las notas regulares como se vería en el sga
            if notas_regulares:
                try:
                    # Separa valores numericos y no numericos para las notas de cursada
                    notas_cursada_numericas = []
                    notas_cursada_texto = []
                    for nota in notas_regulares:
                        if nota[1] and str(nota[1]).replace('.','').isdigit():
                            notas_cursada_numericas.append(float(nota[1]))
                        elif nota[1]:  # Si no es None pero tmp numerico
                            notas_cursada_texto.append(nota[1])

                    # Separa valores numericos y no numericos para las notas de finales
                    notas_final_numericas = []
                    notas_final_texto = []
                    for nota in notas_regulares:
                        if nota[2] and str(nota[2]).replace('.','').isdigit():
                            notas_final_numericas.append(float(nota[2]))
                        elif nota[2]:  # Si no es None pero tmp numerico
                            notas_final_texto.append(nota[2])

                    # Calcula el promedio (para los numeros nomás)
                    if notas_cursada_numericas:
                        avg_cursada = sum(notas_cursada_numericas) / len(notas_cursada_numericas)
                        tk.Label(frame_notas, 
                                text=f"Promedio notas cursada: {avg_cursada:.2f}", 
                                font=('Arial', 10, 'bold')).pack()

                    if notas_final_numericas:
                        avg_final = sum(notas_final_numericas) / len(notas_final_numericas)
                        tk.Label(frame_notas, 
                                text=f"Promedio notas final: {avg_final:.2f}", 
                                font=('Arial', 10, 'bold')).pack()

                except Exception as e:
                    messagebox.showerror("Error", f"Error al calcular el promedio de notas regulares: {str(e)}")
            
            # Mismo procedimiento para las notas extra (las que el usuario puede agregar)
            # Obtiene las notas extra de la tabla del sga
            cursor.execute("""
                SELECT 
                    COALESCE(materia, 'Sin materia') AS materia, 
                    tarea, 
                    nota 
                FROM notas_extra 
                WHERE idusuarios = %s
                ORDER BY materia, tarea
            """, (self.id_u,))

            notas_extra = cursor.fetchall()
            
            # Arma la tabla 
            tree_extra = ttk.Treeview(frame_notas_extra, columns=('Materia', 'Tarea', 'Nota'), show='headings')
            tree_extra.heading('Materia', text='Materia')
            tree_extra.heading('Tarea', text='Tarea')
            tree_extra.heading('Nota', text='Nota')
            
            # Ancho de tabla
            tree_extra.column('Materia', width=200)
            tree_extra.column('Tarea', width=150)
            tree_extra.column('Nota', width=100)
            
            # Agrega la barrita de scrolleo
            scrollbar_extra = ttk.Scrollbar(frame_notas_extra, orient='vertical', command=tree_extra.yview)
            tree_extra.configure(yscrollcommand=scrollbar_extra.set)
            
            tree_extra.pack(side='left', fill='both', expand=True)
            scrollbar_extra.pack(side='right', fill='y')
            
            # Cálculo de promedios
            if notas_extra:
                try:
                    # Separa valores numericos y no numericos
                    notas_numericas = []
                    notas_texto = []
                    for nota in notas_extra:
                        if nota[2] and str(nota[2]).replace('.','').isdigit():
                            notas_numericas.append(float(nota[2]))
                        elif nota[2]:  # Si no es None ni no numerico
                            notas_texto.append(nota[2])

                    # Calcula promedio para numeros
                    if notas_numericas:
                        avg_extra = sum(notas_numericas) / len(notas_numericas)
                        tk.Label(frame_notas_extra, 
                                text=f"Promedio: {avg_extra:.2f}", 
                                font=('Arial', 10, 'bold')).pack()

                    # Muestra notas no numericas (no deberia haber en el sga, pero el usuario las puede introducir)
                    if notas_texto:
                        texto = "Notas no numéricas: " + ", ".join(notas_texto)
                        tk.Label(frame_notas_extra, 
                                text=texto, 
                                font=('Arial', 10)).pack()

                except Exception as e:
                    messagebox.showerror("Error", f"Error al calcular el promedio de notas extra: {str(e)}")

            # Ingresa la info de notas extra
            for nota in notas_extra:
                tree_extra.insert('', 'end', values=nota)
            
            # Botones para manejar la ventana
            self.volver = tk.Button(self.ventana, text = 'Volver', command = self.ventana_menu_materias, font=('Arial', 12, 'bold'), bg="#ffffcc" )
            self.volver.place(relx=0.5, rely=0.03, anchor="n", relheight=0.1, relwidth=0.1)

            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar las notas: {str(e)}")
        finally:
            if 'connection' in locals():
                connection.close()

    def analizar_notas(self):
        # Se abre una ventana diferente
        establecer_fondo(self.ventana)
            
        # Botón para volver al menú de materias
        self.volver = tk.Button(self.ventana, text = 'Volver', command = self.ventana_menu_materias, font=('Arial', 12, 'bold'), bg="#ffffcc" )
        self.volver.place(relx=0.5, rely=0.03, anchor="n", relheight=0.1, relwidth=0.1)

        def cargar_notas_extra():
            try:
                # Llama a la función de cargar notas extra
                notas_extra(self.id_u, self.usuario_sql, self.contra_sql)
            except Exception as e:
                messagebox.showerror("Error", f"Se produjo un error: {e}")
                
        def cargar_notas_sga():
            try:
                # Llama a la funcion de cargar notas del sga
                notas_sga(self.id_u, self.usuario_sql, self.contra_sql)
            except Exception as e:
                messagebox.showerror("Error", f"Se produjo un error: {e}")

        # Botón para cargar notas extras
        self.boton_cargar = tk.Button(self.ventana, text="Agregar notas extra", command=cargar_notas_extra, fg="black", bg="#ffffcc", font=("Helvetica", 14), width=20, height=2)
        self.boton_cargar.place(relx=0.5, rely=0.4, anchor="center")
            
        # Botón para visualizar notas
        self.boton_ver_notas = tk.Button(self.ventana, text="Ver mis notas", command=self.ver_notas, fg="black", bg="#ffffcc", font=("Helvetica", 14), width=20, height=2)
        self.boton_ver_notas.place(relx=0.5, rely=0.5, anchor="center")
        
        # Mensaje de advertencia
        self.advertencia_sga = tk.Label(
            self.ventana,
            text=(
                "Tendrás 30 segundos para ingresar al SGA, caso contrario se cerrará la pestaña por seguridad.\n"
                "No cierres la página del SGA. Cuando termine el proceso, se cerrará automáticamente."),
            fg="red",
            bg="#B38F8F",
            font=("Helvetica", 10), 
            wraplength=400,  # Ajusta el ancho del texto si es demasiado largo
            justify="center"
        )
        self.advertencia_sga.place(relx=0.5, rely=0.6, anchor="center")
        
        # Botón para extraer información del SGA
        self.boton_extraer = tk.Button(self.ventana, text="Extraer mis notas del SGA", command=cargar_notas_sga, fg="black", bg="#ffffcc", font=("Helvetica", 14), width=20, height=2)
        self.boton_extraer.place(relx=0.5, rely=0.7, anchor="center")



    def ver_cronometro(self):
        establecer_fondo(self.ventana)

        materias = self.obtener_materias_usuario(self.id_u)
        
        self.volver = tk.Button(self.ventana, text = 'Volver', command = self.ventana_menu_materias, font=('Arial', 12, 'bold'), bg="#ffffcc" )
        self.volver.place(relx=0.5, rely=0.03, anchor="n", relheight=0.1, relwidth=0.1)


        if materias:
            label_widget = tk.Label(self.ventana, text="Cronómetro de estudio", font=("Arial", 10, "bold"), bg="#ccccff")
            stopwatch_frame = ttk.LabelFrame(self.ventana, labelwidget=label_widget)
            stopwatch_frame.place(relx=0.2, rely=0.2, relheight=0.4, relwidth=0.6)

            
            stopwatch_frame.configure(style="Custom.TLabelframe")  
            style = ttk.Style() 
            style.configure("Custom.TLabelframe", background="#ccccff") 


            ttk.Label(stopwatch_frame, text="Seleccionar materia:", background="#ccccff").pack(pady=5)
            materias = self.obtener_materias_usuario(self.id_u)
            materia_y_id= {s['nombre_materia']: s['id'] for s in materias}
            subject_var = tk.StringVar()
            style = ttk.Style()
            style.configure("Custom.TCombobox", fieldbackground="#ccccff", background="#ccccff")  # Estilo personalizado

            subject_combo = ttk.Combobox(
                stopwatch_frame,
                textvariable=subject_var,
                values=list(materia_y_id.keys()),
                style="Custom.TCombobox"  
            )
            subject_combo.pack(pady=5)

            time_label = tk.Label(
                stopwatch_frame,
                text="00:00:00",
                font=("Helvetica", 48),
                bg="#ccccff" 
            )
            time_label.pack(pady=20)

            self.running = False
            self.empezar_reloj = None
            self.tiempo_corrido = datetime.timedelta()
            
            def actualizar_tiempo():
                if self.running:
                    current_time = datetime.datetime.now()
                    elapsed = current_time - self.empezar_reloj + self.tiempo_corrido
                    horas = int(elapsed.total_seconds() // 3600)
                    minutes = int((elapsed.total_seconds() % 3600) // 60)
                    seconds = int(elapsed.total_seconds() % 60)
                    time_label.config(text=f"{horas:02d}:{minutes:02d}:{seconds:02d}")
                    stopwatch_frame.after(1000, actualizar_tiempo)
            
            def start_stop():
                if not subject_var.get():
                    messagebox.showerror("Error", "Por favor seleccione una materia")
                    return

                if self.running:
                    self.running = False
                    self.tiempo_corrido += datetime.datetime.now() - self.empezar_reloj
                    start_stop_button.config(text="Iniciar")
                    

                    horas = self.tiempo_corrido.total_seconds() / 3600
                    

                    id_materia = materia_y_id[subject_var.get()]
                    

                    try:
                        racha_actual, mejor_racha, message = self.actualizar_racha(
                            self.id_u,
                            id_materia,
                            horas
                        )
                        messagebox.showinfo("Sesion de estudio finalizada", 
                                        f"Tiempo estudiado: {formatear_tiempo(horas)}\n\n{message}")
                    except Exception as e:
                        messagebox.showerror("Error", f"Error al guardar tu tiempo: {str(e)}")
                    

                    self.tiempo_corrido = datetime.timedelta()
                    time_label.config(text="00:00:00")
                    
                else:

                    self.running = True
                    self.empezar_reloj = datetime.datetime.now()
                    start_stop_button.config(text="Parar")
                    actualizar_tiempo()

            def reset_timer():
                self.running = False
                self.tiempo_corrido = datetime.timedelta()
                time_label.config(text="00:00:00")
                start_stop_button.config(text="Iniciar")

            # Botones para empezar y frenar
            button_frame = ttk.Frame(stopwatch_frame)
            button_frame.pack(pady=10)

            start_stop_button = ttk.Button(
                button_frame,
                text="Iniciar",
                command=start_stop,
                width=20,
                style="Custom.TButton"  
            )
            start_stop_button.pack(side=tk.LEFT, padx=5)

            reset_button = ttk.Button(
                button_frame,
                text="Reset",
                command=reset_timer,
                width=20,
                style="Custom.TButton"  
            )
            reset_button.pack(side=tk.LEFT, padx=5)

            # Crear un estilo personalizado para el fondo de los botones
            style = ttk.Style()
            style.configure("Custom.TButton", background="#ccccff")

            # Botón "Audio" debajo del cronómetro
            self.audio = tk.Button(self.ventana, text='Audio', command=self.escuchar_audio, bg="#ffffcc", font=("Arial", 12, "bold"))
            self.audio.place(relx=0.45, rely=0.65, relheight=0.1, relwidth=0.12)

            
        else:
            self.error = tk.Label(self.ventana, text = 'No se encontraron materias, por favor\nregistre una materia y vuelva a intentarlo!')
            self.error.place(relx=0.4, rely=0.4, relheight=0.1, relwidth=0.2)
    
    def escuchar_audio(self):
        try:
            audio()  # Llama a la función de audio definida aparte
        except Exception as e:
            messagebox.showerror("Error", f"Error al reproducir el audio: {str(e)}")
    
    
    def obtener_ultimas_fechas_estudio(self, id_usuario):
        connection = self.get_db_connection()
        if connection is None:
            return {}

        try:
            cursor = connection.cursor()
            
            # Obtener ultima fecha para cada materia
            extraer = """
                SELECT id_materia, MAX(fecha_estudio) as ultima_fecha
                FROM horas_estudiadas 
                WHERE idusuarios = %s
                GROUP BY id_materia
            """
            cursor.execute(extraer, (id_usuario,))
            resultado = cursor.fetchall()
            
            # Crear diccionario para almacenar esta info
            ultimas_fechas = {row[0]: row[1] for row in resultado}
            
            return ultimas_fechas

        except Exception as e:
            print(f"Error accediendo a la base de datos: {e}")
            return {}
        finally:
            if connection:
                connection.close()
    
                    
                    
    def ver_rachas(self):
        establecer_fondo(self.ventana)
        materias = self.obtener_materias_usuario(self.id_u)
        
        self.volver = tk.Button(self.ventana, text = 'Volver', command = self.ventana_menu_materias, font=('Arial', 12, 'bold'), bg="#ffffcc" )
        self.volver.place(relx=0.5, rely=0.03, anchor="n", relheight=0.1, relwidth=0.1)
        
        
        if materias:
        
            rachas_frame = ttk.LabelFrame(self.ventana, text="Rachas actuales")
            rachas_frame.place(relx=0.105, rely=0.15, relheight=0.8, relwidth=0.8)

            button_frame = ttk.Frame(rachas_frame)
            button_frame.pack(fill=tk.X, padx=10, pady=(10,5))

            ttk.Button(
                button_frame,
                text="Actualizar",
                command=lambda: self.ver_rachas(),
                width=15
            ).pack(side=tk.TOP, padx=5)


            tree_frame = ttk.Frame(rachas_frame)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)


            columns = ('Materia', 'Racha actual', 'Mejor racha', 'Ultima fecha de estudio', 'Progreso de hoy')
            tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)


            for col in columns:
                if col == 'Progreso de hoy':
                    tree.heading(col, text=col)
                    tree.column(col, width=400)
                elif col == 'Materia':
                    tree.heading(col, text=col)
                    tree.column(col, width=150)
                elif col == 'Ultima fecha de estudio':
                    tree.heading(col, text=col)
                    tree.column(col, width=200)
                else:
                    tree.heading(col, text=col)
                    tree.column(col, width=41)

            scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            

            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


            materias = self.obtener_materias_usuario(self.id_u)
            ultimas_fechas = self.obtener_ultimas_fechas_estudio(self.id_u)
            
            for subject in materias:
                id_materia = subject['id']
                nombre_materia = subject['nombre_materia']
                ultimo_update = ultimas_fechas.get(id_materia)
                
                #basura para poder seguir usando la funcion pero no me interesa el tercer dato
                racha_actual, mejor_racha, basura= self.cargar_info_rachas(
                    self.id_u, 
                    id_materia
                )
                

                today = datetime.datetime.now()
                horas_totales = self.total_horas_hoy(
                    self.id_u, 
                    id_materia, 
                    today
                )
                

                schedule = self.cargar_cronograma(self.id_u, id_materia, today)
                horas_planeadas = schedule.get(today.strftime('%A'), 0)
                

                if horas_planeadas == 0:
                    progress = "No hay estudio programado"
                else:
                    progress = f"{formatear_tiempo(horas_totales)} de estudio. Objetivo: {formatear_tiempo(horas_planeadas)}"
                

                last_date = ultimo_update.strftime('%Y-%m-%d') if ultimo_update else "Nunca ha estudiado para esta materia"
                

                tags = ()
                if horas_planeadas > 0:
                    if horas_totales >= horas_planeadas:
                        tags = ('completedo',)
                    elif horas_totales == 0:
                        tags = ('sin_iniciar',)
                    else:
                        tags = ('en_progreso',)


                tree.insert('', 'end', values=(
                    nombre_materia,
                    f"{racha_actual} dia(s)",
                    f"{mejor_racha} dia(s)",
                    last_date,
                    progress
                ), tags=tags)


            tree.tag_configure('completado', foreground='blue')
            tree.tag_configure('sin_iniciar', foreground='red')
            tree.tag_configure('en_progreso', foreground='orange')


        else:
            self.error = tk.Label(self.ventana, text = 'No se encontraron materias, por favor\nregistre una materia y vuelva a intentarlo!')
            self.error.place(relx=0.4, rely=0.4, relheight=0.1, relwidth=0.2)
            

    def ver_comisiones_ventana(self): 
        self.background = tk.Label(self.ventana)
        self.background.place(relx=0, rely=0, relheight=1, relwidth=1)
        
        self.volver = tk.Button(self.ventana, text = 'Volver', command = self.ventana_mis_materias, font=('Arial', 12, 'bold'), bg="#ffffcc" )
        self.volver.place(relx=0.5, rely=0.03, anchor="n", relheight=0.1, relwidth=0.1)

        columns = ('Materia', 'Comision', 'Día', 'Horario', 'Aula')
        tree = ttk.Treeview(self.ventana, columns=columns, show='headings')
            
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        tree.place(relx=0.02, rely=0.15, relheight=0.8, relwidth=0.96)
            
        materias, comisiones, dias, horarios, aulas = ver_comision(self.id_u, self.usuario_sql, self.contra_sql)
        
        # Insertar datos en el Treeview
        for materia, comision, dia, horario, aula in zip(materias, comisiones, dias, horarios, aulas):
            tree.insert('', 'end', values=(materia, comision, dia, horario, aula))
    
    def ventana_ver_materias(self):
        self.background = tk.Label(self.ventana)
        self.background.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.volver = tk.Button(self.ventana, text='Volver', command=self.ventana_mis_materias, font=('Arial', 12, 'bold'), bg="#ffffcc")
        self.volver.place(relx=0.5, rely=0.03, anchor="n", relheight=0.1, relwidth=0.1)

        # Columnas del t5reeview
        columns = ('Nombre', 'Cronograma a partir de', 'Última fecha con cronograma')
        tree = ttk.Treeview(self.ventana, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        tree.place(relx=0.02, rely=0.15, relheight=0.6, relwidth=0.96)

        # Obtener materias del usuario y mostrarlas
        materias = self.obtener_materias_usuario(self.id_u)
        for subject in materias:
            tree.insert('', 'end', values=(
                subject['nombre_materia'],
                subject['earliest_schedule'] or 'Sin cronograma',
                subject['latest_schedule'] or 'Sin cronograma'
            ))

        # Función para eliminar materias
        def eliminar_materia():
            
            self.background = tk.Label(self.ventana)
            
            try:
                selected_item = tree.selection()[0] 
                materia_nombre = tree.item(selected_item, 'values')[0]  
                
                # pregunta confirmacion para eliminarlo
                if messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar la materia '{materia_nombre}'?"):
                    self.eliminar_materia_db(self.id_u, materia_nombre) 
                    tree.delete(selected_item)  
                    messagebox.showinfo("Éxito", f"Materia '{materia_nombre}' eliminada correctamente.")
            except IndexError:
                messagebox.showerror("Error", "Por favor selecciona una materia para eliminar.")

        # Botón para eliminar materia
        boton_eliminar = tk.Button(self.ventana, text='Eliminar materia', command=eliminar_materia, font=('Arial', 12, 'bold'), bg="#ffcccc")
        boton_eliminar.place(relx=0.4, rely=0.8, relheight=0.05, relwidth=0.2)

    # Función para eliminarlo de la base de datos
    def eliminar_materia_db(self, user_id, nombre_materia):
        connection = self.get_db_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor()

            # Obtengo el id de la materia a eliminar
            select_sql = "SELECT id FROM materias WHERE idusuarios = %s AND nombre_materia = %s"
            cursor.execute(select_sql, (user_id, nombre_materia))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Error", "La materia no existe.")
                return
            
            materia_id = result[0]

            # asegurarse de que el cursor no tiene resultados pendientes (en el mysql), para descartar cualquier resultado no leído q encuientre
            cursor.fetchall()
            
            # Eliminar de horas_estudiadas
            borrar_tiempo = "DELETE FROM horas_estudiadas WHERE idusuarios = %s AND id_materia = %s"
            cursor.execute(borrar_tiempo, (user_id, materia_id))
            
            # Eliminar de rachas
            borrar_rachas = "DELETE FROM rachas WHERE idusuarios = %s AND id_materia = %s"
            cursor.execute(borrar_rachas, (user_id, materia_id))

            # Eliminar las filas dependientes en la tabla 'cronogramas', sino mysql no lo puede eliminar
            delete_cronogramas_sql = "DELETE FROM cronogramas WHERE id_materia = %s"
            cursor.execute(delete_cronogramas_sql, (materia_id,))

            # Finalmente, eliminar la materia
            delete_sql = "DELETE FROM materias WHERE idusuarios = %s AND nombre_materia = %s"
            cursor.execute(delete_sql, (user_id, nombre_materia))
            connection.commit()

        except Error as e:
            messagebox.showerror("Error", f"Error al eliminar la materia de la base de datos: {e}")
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def agregar_materia(self, user_id, nombre_materia):
        connection = self.get_db_connection()
        if connection is None:
            return None

        try:
            cursor = connection.cursor()
            # veo si la materia ya esta
            check_sql = "SELECT COUNT(*) FROM materias WHERE idusuarios = %s AND nombre_materia = %s"
            cursor.execute(check_sql, (user_id, nombre_materia))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", "Ya ha ingresado esta materia")
                return None
            
            # si la materia no existe, la inserta
            if nombre_materia.strip() == '':
                messagebox.showerror("Error", "Ingrese el nombre de la materia!")
                return None
            else:
                try:
                    insert_sql = "INSERT INTO materias (idusuarios, nombre_materia) VALUES (%s, %s)"
                    cursor.execute(insert_sql, (user_id, nombre_materia))
                    
                    id_materia = cursor.lastrowid
                    connection.commit()
                    return id_materia
                except mysql.connector.IntegrityError as e:
                    messagebox.showerror("Error", "Ya ha ingresado esta materia")
                    connection.rollback()
                    return None
                    
        except Error as e:
            messagebox.showerror("Error", f"Error agregando materia: {e}")
            connection.rollback()
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                
    def ventana_mis_materias(self):
        establecer_fondo(self.ventana)

        self.volver = tk.Button(self.ventana, text = 'Volver', command = self.ventana_menu_materias, font=('Arial', 12, 'bold'), bg="#ffffcc" )
        self.volver.place(relx=0.5, rely=0.03, anchor="n", relheight=0.1, relwidth=0.1)

        self.titulo_nombre = tk.Label(self.ventana, text='Nombre de la materia', font=('Arial', 9, 'bold'), bg="#B38F8F")
        self.titulo_nombre.place(relx=0.3, rely=0.4, relheight=0.03, relwidth=0.1)

        self.nombre = tk.Entry(self.ventana)
        self.nombre.place(relx=0.4, rely=0.4, relheight=0.03, relwidth=0.2)

        def guardar_materia():
            name = self.nombre.get().strip()
            if name:
                id_materia = self.agregar_materia(self.id_u, name)
                if id_materia:
                    messagebox.showinfo("Exito", f"Materia agregada exitosamente!")
            else:
                messagebox.showerror("Error", "Por favor ingresar el nombre de la materia")

        self.agregar = tk.Button(self.ventana, text='Agregar materia', command=guardar_materia)
        self.agregar.place(relx=0.45, rely=0.45, relheight=0.03, relwidth=0.08)
    
        # Botón "Ver comisiones" 
        self.ver_comisiones = tk.Button(self.ventana, text='Ver comisiones', command=self.ver_comisiones_ventana)
        self.ver_comisiones.place(relx=0.35, rely=0.75, relheight=0.05, relwidth=0.12)

        # Botón "Ver Materias" 
        self.agregar_materia_boton = tk.Button(self.ventana, text='Ver Materias', command=self.ventana_ver_materias)
        self.agregar_materia_boton.place(relx=0.5, rely=0.75, relheight=0.05, relwidth=0.12)

        # Mensaje de advertencia
        self.advertencia_sga = tk.Label(
            self.ventana,
            text=(
                "Tendrás 30 segundos para ingresar al SGA, caso contrario se cerrará la pestaña por seguridad.\n"
                "No cierres la página del SGA. Cuando termine el proceso, se cerrará automáticamente."
            ),
            fg="red",
            bg="#B38F8F",  # Fondo a juego con la ventana
            wraplength=400,  # Ajusta el ancho del texto si es demasiado largo
            justify="center"  # Centra el texto
        )
        self.advertencia_sga.place(relx=0.5, rely=0.65, anchor="center")

        self.boton_sga = tk.Button(
            self.ventana, 
            text='Agregar materias automáticamente desde SGA', 
            command=lambda: procesar_comisiones(self.id_u,self.usuario_sql,self.contra_sql)
        )
        self.boton_sga.place(relx=0.35, rely=0.55, relheight=0.05, relwidth=0.3)

        fondo_texto(
            [
                self.volver, self.volver, self.boton_sga, 
                self.agregar, self.ver_comisiones, self.agregar_materia_boton
            ], 
            color="#FFFFCC"
        )

    def ventana_ver_cronograma(self):
        establecer_fondo(self.ventana)

        materias = self.obtener_materias_usuario(self.id_u)
        
        self.volver = tk.Button(self.ventana, text = 'Volver', command = self.ventana_menu_materias, font=('Arial', 12, 'bold'), bg="#ffffcc" )
        self.volver.place(relx=0.5, rely=0.03, anchor="n", relheight=0.1, relwidth=0.1)

        if materias:
            self.materia_titulo = tk.Label(self.ventana, text = 'Materia')
            self.materia_titulo.place(relx=0.25, rely=0.2, relheight=0.03, relwidth=0.1)
            nombre_y_id = {s['nombre_materia']: s['id'] for s in materias}
            subject_var = tk.StringVar()
            subject_combo = ttk.Combobox(
                self.ventana,
                textvariable=subject_var,
                values=list(nombre_y_id.keys()) 
            )
            subject_combo.place(relx=0.35, rely=0.2, relheight=0.03, relwidth=0.1)
        
            self.fecha = tk.Label(self.ventana, text = 'Seleccionar Fecha')
            self.fecha.place(relx=0.55, rely=0.2, relheight=0.03, relwidth=0.1)
            date_entry = DateEntry(self.ventana, width=12, background='darkblue', foreground='white', borderwidth=2)
            date_entry.place(relx = 0.65, rely = 0.2, relheight = 0.03, relwidth = 0.1)

            schedule_text = tk.Text(self.ventana)
            schedule_text.place(relx=0.3, rely=0.3, relheight=0.55, relwidth=0.4)

            def ver_cronograma():
                if not subject_var.get():
                    messagebox.showerror("Error", "Por favor seleccione una materia")
                    return
                
                try:
                    id_materia = nombre_y_id[subject_var.get()]
                    date = date_entry.get_date()
                    
                    schedule = self.cargar_cronograma(self.id_u, id_materia, date)
                    

                    schedule_text.delete('1.0', tk.END)
                    

                    schedule_text.insert('1.0', f"Cronograma para {date.strftime('%Y-%m-%d')}\n")
                    schedule_text.insert(tk.END, "-" * 30 + "\n\n")
                    
                    horas_planeadas = schedule.get(date.strftime('%A'), 0)
                    
                    
                    horas_totales = 0
                    days_translation = {
                        'Monday': 'Lunes',
                        'Tuesday': 'Martes',
                        'Wednesday': 'Miercoles',
                        'Thursday': 'Jueves',
                        'Friday': 'Viernes',
                        'Saturday': 'Sabado',
                        'Sunday': 'Domingo'
                    }

                    for day, horas in schedule.items():
                        if day in days_translation:
                            schedule_text.insert(tk.END, f" {days_translation[day]}: {formatear_tiempo(horas)}\n")
                            horas_totales += horas

                    
                    schedule_text.insert(tk.END, f"\nTiempo de estudio total semanal: {formatear_tiempo(horas_totales)}")
                    

                    horas_estudiadas = self.total_horas_hoy(
                        self.id_u, 
                        id_materia, 
                        date
                    )
                    

                    schedule_text.insert(tk.END, f"\n\nProgreso para hoy:")
                    schedule_text.insert(tk.END, f"\nPlanificadas: {formatear_tiempo(horas_planeadas)}")
                    schedule_text.insert(tk.END, f"\nEstudiadas: {formatear_tiempo(horas_estudiadas)}")
                    
                    if horas_planeadas > 0:
                        progress = (horas_estudiadas / horas_planeadas) * 100
                        schedule_text.insert(tk.END, f"\nProgreso: {progress:.1f}%")
                    
                except ValueError as e:
                    messagebox.showerror("Error", f"Input invalido {str(e)}")
                except Exception as e:
                    messagebox.showerror("Error", f"Ocurrio un error: {str(e)}")

            ttk.Button(
                self.ventana,
                text="Ver cronograma",
                command=ver_cronograma,
                width=20
            ).place(relx=0.46, rely = 0.875, relheight=0.05, relwidth=0.08)
            self.ventana.bind('<Return>', lambda event: ver_cronograma())
        else:
            self.error = tk.Label(self.ventana, text = 'No se encontraron materias, por favor\nregistre una materia y vuelva a intentarlo!')
            self.error.place(relx=0.4, rely=0.4, relheight=0.1, relwidth=0.2)
            
    
    def ventana_organizar_cronograma(self):
        establecer_fondo(self.ventana)
        materias = self.obtener_materias_usuario(self.id_u)

        self.volver = tk.Button(self.ventana, text='Volver', command=self.ventana_menu_materias, font=('Arial', 12, 'bold'), bg="#ffffcc")
        self.volver.place(relx=0.5, rely=0.03, anchor="n", relheight=0.1, relwidth=0.1)

        if materias:
            # Cuadro de set schedule con Scrollbar
            scroll_frame = ttk.LabelFrame(self.ventana, text="Organizar Cronograma")
            scroll_frame.place(relx=0.26, rely=0.15, relheight=0.78, relwidth=0.5)

            # Canvas para el contenido scrollable
            scroll_canvas = tk.Canvas(scroll_frame)
            scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Scrollbar para el Canvas
            scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=scroll_canvas.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            scroll_canvas.configure(yscrollcommand=scrollbar.set)

            # Frame interno dentro del Canvas
            schedule_frame = ttk.Frame(scroll_canvas)
            scroll_canvas.create_window((0, 0), window=schedule_frame, anchor="nw")

            # Actualizar el tamaño del área de scroll
            def actualizar_scroll(event):
                scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

            schedule_frame.bind("<Configure>", actualizar_scroll)

            # Elegir materia
            ttk.Label(schedule_frame, text="Elija la materia:").pack(pady=5)
            nombre_y_id = {s['nombre_materia']: s['id'] for s in materias}
            subject_var = tk.StringVar()
            subject_combo = ttk.Combobox(
                schedule_frame,
                textvariable=subject_var,
                values=list(nombre_y_id.keys()) 
            )
            subject_combo.pack(pady=5)

            # Duración del cronograma
            date_frame = ttk.LabelFrame(schedule_frame, text="Duración de cronograma semanal")
            date_frame.pack(pady=10, padx=10, fill=tk.X)

            # Fecha inicio
            fecha_inicio_frame = ttk.Frame(date_frame)
            fecha_inicio_frame.pack(pady=5, fill=tk.X)
            ttk.Label(fecha_inicio_frame, text="Fecha de inicio:").pack(side=tk.LEFT, padx=5)
            fecha_inicio = DateEntry(fecha_inicio_frame, width=12, background='darkblue',
                                    foreground='white', borderwidth=2)
            fecha_inicio.pack(side=tk.LEFT, padx=5)

            # Fecha final
            fecha_final_frame = ttk.Frame(date_frame)
            fecha_final_frame.pack(pady=5, fill=tk.X)
            ttk.Label(fecha_final_frame, text="Fecha final:").pack(side=tk.LEFT, padx=5)
            fecha_final = DateEntry(fecha_final_frame, width=12, background='darkblue',
                                    foreground='white', borderwidth=2)
            fecha_final.pack(side=tk.LEFT, padx=5)

            # Horas diarias
            horas_frame = ttk.LabelFrame(schedule_frame, text="Horas diarias de estudio")
            horas_frame.pack(pady=10, padx=10, fill=tk.X)

            header_frame = ttk.Frame(horas_frame)
            header_frame.pack(fill=tk.X, pady=5)
            ttk.Label(header_frame, text="Día", width=15).pack(side=tk.LEFT, padx=5)
            ttk.Label(header_frame, text="Horas", width=10).pack(side=tk.LEFT, padx=5)

            # Diccionario para guardar info
            hour_vars = {}

            days_frame = ttk.Frame(horas_frame)
            days_frame.pack(fill=tk.BOTH, expand=True)

            for i, day in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                                    'Friday', 'Saturday', 'Sunday']):
                day_frame = ttk.Frame(days_frame)
                day_frame.pack(fill=tk.X, pady=2)

                semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

                ttk.Label(
                    day_frame, 
                    text=semana[i],
                    width=15
                ).pack(side=tk.LEFT, padx=5)

                hour_var = tk.StringVar(value="0")
                hour_vars[day] = hour_var

                entry = ttk.Entry(
                    day_frame,
                    textvariable=hour_var,
                    width=10
                )
                entry.pack(side=tk.LEFT, padx=5)

            # Botones rápidos
            quick_set_frame = ttk.LabelFrame(schedule_frame, text="Botones rápidos")
            quick_set_frame.pack(pady=10, padx=10)
            
            def validar_horas():
                
                days_translation = {
                        'Monday': 'lunes',
                        'Tuesday': 'martes',
                        'Wednesday': 'miercoles',
                        'Thursday': 'jueves',
                        'Friday': 'viernes',
                        'Saturday': 'sabado',
                        'Sunday': 'domingo'
                    }
                
                try:
                    for day, var in hour_vars.items():
                        if not var.get().replace('.', '', 1).isdigit():
                            raise ValueError(f"Horas para el {days_translation[day]} tienen que ser un numero")
                        horas = float(var.get())
                        if horas < 0:
                            raise ValueError(f"Horas para el {days_translation[day]} no pueden ser un numero negativo")
                        if horas > 24:
                            raise ValueError(f"Horas para el {days_translation[day]} no pueden ser mas que 24")
                    return True
                except ValueError as e:
                    messagebox.showerror("Input invalido", str(e))
                    return False

            def validar_fechas():
                start = fecha_inicio.get_date()
                end = fecha_final.get_date()

                if end < start:
                    messagebox.showerror(
                        "Fechas no coherentes", 
                        "Fecha final no puede ser antes que inicial"
                    )
                    return False
                return True

            def guardar_cronograma():
                # Validar seleccion de materia
                if not subject_var.get():
                    messagebox.showerror("Error", "Por favor seleccionar una materia")
                    return

                # Validar dias y horas
                if not validar_fechas() or not validar_horas():
                    return

                try:
                    id_materia = nombre_y_id[subject_var.get()]

                    horas = {}
                    total_weekly_horas = 0
                    for day, var in hour_vars.items():
                        horas[day] = float(var.get())
                        total_weekly_horas += horas[day]

                    # Pedir confirmacion si las horas semanales son demasiadas
                    if total_weekly_horas > 85:
                        if not messagebox.askyesno(
                            "Confirmar cronograma",
                            f"Total de horas semanales son ({total_weekly_horas}).¿No te parece mucho?.\n"
                            "Confirmas este cronograma?"
                        ):
                            return

                    if self.guardar_cronograma(
                        self.id_u,
                        id_materia,
                        horas,
                        fecha_inicio.get_date(),
                        fecha_final.get_date()
                    ):
                        messagebox.showinfo(
                            "Exito", 
                            f"Cronograma guardado exitosamente!\n"
                            f"Total de tiempo de estudio semanal: {formatear_tiempo(total_weekly_horas)}"
                        )
                        # Mantenerse en la misma ventana sin regresar al menu
                    else:
                        messagebox.showerror(
                            "Error", 
                            "No se pudo guardar el cronograma"
                        )

                except ValueError as e:
                    messagebox.showerror("Error", f"Input invalido: {str(e)}")
                except Exception as e:
                    messagebox.showerror("Error", f"Ocurrio un error: {str(e)}")

            # Botones rapidos
            quick_set_frame = ttk.LabelFrame(schedule_frame, text="Botones rapidos")
            quick_set_frame.pack(pady=10, padx=10, fill=tk.X)

            def quick_set_horas(horas):
                for var in hour_vars.values():
                    var.set(str(horas))

            quick_buttons = [
                ("Borrar todo", 0),
                ("1 hora/dia", 1),
                ("2 horas/dia", 2),
                ("3 horas/dia", 3)
            ]

            for text, horas in quick_buttons:
                ttk.Button(
                    quick_set_frame,
                    text=text,
                    command=lambda h=horas: quick_set_horas(h),
                    width=15
                ).pack(side=tk.LEFT, padx=5, pady=5)

            button_frame = ttk.Frame(schedule_frame)
            button_frame.pack(pady=10, fill=tk.X)

            ttk.Button(
                button_frame,
                text="Guardar cronograma",
                command=guardar_cronograma,
                width=20
            ).pack(side=tk.LEFT, padx=5)
            self.ventana.bind('<Return>', lambda event: guardar_cronograma())

        else:
            # Mostrar mensaje de error
            self.error = tk.Label(self.ventana, text='No se encontraron materias, por favor\nregistre una materia y vuelva a intentarlo!')
            self.error.place(relx=0.4, rely=0.4, relheight=0.1, relwidth=0.2)


    def get_db_connection(self):
        try:
            connection = mysql.connector.connect(
                host='127.0.0.1',
                port = 3306,
                user=self.usuario_sql,
                password=self.contra_sql,
                database='studytrack'
            )
            return connection
        except Error as e:
            messagebox.showerror("Database Error", f"Error conectando a la base de datos: {e}")
            return None
        
    
    def cargar_cronograma(self, user_id, id_materia, date=None):
        connection = self.get_db_connection()
        if connection is None:
            return {}

        try:
            cursor = connection.cursor(dictionary=True)
            
            if date is None:
                date = datetime.datetime.now().date()
            
            cursor.execute("""
                SELECT dia_de_la_semana, horas_planeadas 
                FROM cronogramas 
                WHERE idusuarios = %s 
                AND id_materia = %s
                AND fecha_inicio <= %s 
                AND fecha_final >= %s
            """, (user_id, id_materia, date, date))
            
            schedule = {}
            for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
                schedule[day] = 0
                
            
            for row in cursor.fetchall():
                schedule[row['dia_de_la_semana']] = row['horas_planeadas']
                
            return schedule
            
        except Error as e:
            messagebox.showerror("Error", f"Error cargando cronograma {e}")
            return {}
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def total_horas_hoy(self, user_id, id_materia, date):
            connection = self.get_db_connection()
            if connection is None:
                return 0

            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("""
                    SELECT SUM(horas) as horas_totales
                    FROM horas_estudiadas
                    WHERE idusuarios = %s 
                    AND id_materia = %s
                    AND DATE(fecha_estudio) = DATE(%s)
                """, (user_id, id_materia, date))
                
                result = cursor.fetchone()
                return result['horas_totales'] or 0
                
            except Error as e:
                messagebox.showerror("Error", f"Error obteniendo horas estudiadas: {e}")
                return 0
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

    def guardar_cronograma(self, user_id, id_materia, horas, fecha_inicio, fecha_final):
        connection = self.get_db_connection()
        if connection is None:
            return False

        try:
            cursor = connection.cursor()
            
            # Borrar cronograma exitente para fecha seleccionada
            cursor.execute("""
                DELETE FROM cronogramas 
                WHERE idusuarios = %s AND id_materia = %s 
                AND fecha_inicio = %s AND fecha_final = %s
            """, (user_id, id_materia, fecha_inicio, fecha_final))
            
            # Insertar nuevo cronograma
            for day, horas_planeadas in horas.items():
                cursor.execute("""
                    INSERT INTO cronogramas 
                    (idusuarios, id_materia, dia_de_la_semana, horas_planeadas, fecha_inicio, fecha_final)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (user_id, id_materia, day, horas_planeadas, fecha_inicio, fecha_final))
                
            connection.commit()
            return True
        except Error as e:
            messagebox.showerror("Error", f"Error guardando su cronograma {e}")
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
     
        
    def actualizar_racha(self, user_id, id_materia, horas_estudiadas, date=None):
        # Configuración inicial de la fecha
        if date is None:
            date = datetime.datetime.now()
                    
        if isinstance(date, datetime.date):
            date = datetime.datetime.combine(date, datetime.datetime.min.time())

        # Obtener información actual del cronograma y rachas
        horas = self.cargar_cronograma(user_id, id_materia, date)
        racha_actual, mejor_racha, ultimo_update = self.cargar_info_rachas(user_id, id_materia)

        # Obtener horas planeadas para el día actual
        nombre_dia = date.strftime('%A')
        horas_planeadas = horas.get(nombre_dia, 0)
        
        # Calcular total de horas estudiadas
        total_horas = self.total_horas_hoy(user_id, id_materia, date)
        total_horas += horas_estudiadas

        # Verificar si es la primera vez o actualizar según último registro
        if ultimo_update is None:
            ultimo_update = date
            message = "Primera sesión de estudio registrada."
        else:
            # Convertir último update si es necesario
            if isinstance(ultimo_update, datetime.date):
                ultimo_update = datetime.datetime.combine(ultimo_update, datetime.datetime.min.time())
            
            # Calcular diferencia de días
            fecha_ahora = date.date()
            ultimo_check = ultimo_update.date()
            diff_dias = (fecha_ahora - ultimo_check).days
            updatear = 0
            
            # Verificar días saltados y objetivos no cumplidos
            if diff_dias >= 1:
                # Verificar el día anterior
                dia_anterior = date - datetime.timedelta(days=1)
                horas_dia_anterior = self.total_horas_hoy(user_id, id_materia, dia_anterior)
                nombre_dia_anterior = dia_anterior.strftime('%A')
                horas_planeadas_anterior = self.cargar_cronograma(user_id, id_materia, dia_anterior).get(nombre_dia_anterior, 0)
                
                # Reiniciar racha si se saltó algún día o no se cumplió el objetivo anterior
                if diff_dias > 1 or (horas_dia_anterior < horas_planeadas_anterior and horas_planeadas_anterior > 0):
                    racha_actual = 0
                    updatear = 1
                    message = "Racha reiniciada! Se perdió la racha por días sin completar."
                else:
                    message = "Continuando con la sesión de estudio."
            elif diff_dias < 0:
                raise ValueError("No se puede checkear fechas en el pasado!")
            else:  
                message = "Siguiendo con la sesión de estudio de hoy."

        # Verificar si se cumplió el objetivo del día actual
        if total_horas >= horas_planeadas and horas_planeadas > 0:
            # Incrementar racha solo si es un nuevo día y se cumplió el objetivo
            if ultimo_update is None or date.date() > ultimo_update.date():
                if updatear == 1:
                    racha_actual = 0
                else:
                    racha_actual += 1
                if racha_actual > mejor_racha:
                    mejor_racha = racha_actual
            message = f"¡Gran trabajo! Cumpliste con tu objetivo de hoy! Racha actual: {racha_actual} días"
        else:
            # Mensajes según si hay horas planeadas o no
            if horas_planeadas == 0:
                days = {
                    'Monday': 'lunes',
                    'Tuesday': 'martes',
                    'Wednesday': 'miércoles',
                    'Thursday': 'jueves',
                    'Friday': 'viernes',
                    'Saturday': 'sábado',
                    'Sunday': 'domingo'
                }
                message = f"No hay horas planeadas para el {days.get(nombre_dia, '')}."
            else:
                # Mostrar horas restantes o tiempo estudiado
                horas_restantes = horas_planeadas - total_horas
                if horas_restantes > 0:
                    message = f"Todavía faltan {formatear_tiempo(horas_restantes)} para cumplir con tu objetivo."
                else:
                    message = f"Hoy estudiaste {formatear_tiempo(total_horas)}."

        # Guardar la información en la base de datos
        self.cargar_horas_estudiadas(user_id, id_materia, date, horas_estudiadas)

        # Actualizar información de rachas si se cumplió el objetivo o es un nuevo día
        if total_horas >= horas_planeadas or (ultimo_update and date.date() > ultimo_update.date()):
            self.guardar_info_rachas(user_id, id_materia, racha_actual, mejor_racha, date)

        # Agregar información del tiempo total estudiado al mensaje
        message += f"\nTiempo estudiado hoy: {formatear_tiempo(total_horas)}"
        
        return racha_actual, mejor_racha, message


    
    
    def cargar_horas_estudiadas(self, user_id, id_materia, date, horas):
        connection = self.get_db_connection()
        if connection is None:
            return False

        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO horas_estudiadas (idusuarios, id_materia, fecha_estudio, horas)
                VALUES (%s, %s, %s, %s)
            """, (user_id, id_materia, date.strftime('%Y-%m-%d'), horas))
            
            connection.commit()
            return True
        except Error as e:
            messagebox.showerror("Error", f"Error cargando horas estudiadas: {e}")
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                
    def cargar_info_rachas(self, user_id, id_materia):
        connection = self.get_db_connection()
        if connection is None:
            return 0, 0, None

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT racha_actual, mejor_racha, ultimo_update
                FROM rachas
                WHERE idusuarios = %s AND id_materia = %s
            """, (user_id, id_materia))
            
            info_racha = cursor.fetchone()
            if info_racha:
                return (info_racha['racha_actual'], 
                       info_racha['mejor_racha'], 
                       info_racha['ultimo_update'])
                
        except Error as e:
            messagebox.showerror("Error", f"Error cargando rachas: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        
        return 0, 0, None

    def guardar_info_rachas(self, user_id, id_materia, racha_actual, mejor_racha, ultimo_update):
        connection = self.get_db_connection()
        if connection is None:
            return False

        try:
            cursor = connection.cursor()
            cursor.execute("""
                DELETE FROM rachas 
                WHERE idusuarios = %s AND id_materia = %s
            """, (user_id, id_materia))
            
            cursor.execute("""
                INSERT INTO rachas 
                (idusuarios, id_materia, racha_actual, mejor_racha, ultimo_update)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, id_materia, racha_actual, mejor_racha, ultimo_update))
            
            connection.commit()
            return True
        except Error as e:
            messagebox.showerror("Error", f"Error guardando informacion de la racha: {e}")
            connection.rollback()
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def checkear_racha(self):
        if not self.id_u:
            return
            
        fecha_ahora = datetime.datetime.now().date()
        

        materias = self.obtener_materias_usuario(self.id_u)
        
        for subject in materias:
            id_materia = subject['id']
            

            yesterday = fecha_ahora - datetime.timedelta(days=1)
            horas_totales = self.total_horas_hoy(self.id_u, id_materia, yesterday)
            

            yesterday_schedule = self.cargar_cronograma(self.id_u, id_materia, yesterday)
            horas_planeadas = yesterday_schedule.get(yesterday.strftime('%A'), 0)
            

            if horas_planeadas > 0 and horas_totales < horas_planeadas:
                self.guardar_info_rachas(self.id_u, id_materia, 0, 
                                    self.cargar_info_rachas(self.id_u, id_materia)[1], 
                                    fecha_ahora)
                

    def obtener_materias_usuario(self, user_id):
        connection = self.get_db_connection()
        if connection is None:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT DISTINCT s.id, s.nombre_materia,
                        MIN(sch.fecha_inicio) as earliest_schedule,
                        MAX(sch.fecha_final) as latest_schedule
                FROM materias s
                LEFT JOIN cronogramas sch ON s.id = sch.id_materia
                WHERE s.idusuarios = %s
                GROUP BY s.id, s.nombre_materia
                ORDER BY s.nombre_materia
            """, (user_id,))
            
            return cursor.fetchall()
        except Error as e:
            messagebox.showerror("Error", f"Error extrayendo tus materias: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
            
    def ver_graficos(self):
        try:
            connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user=self.usuario_sql,
            password=self.contra_sql,
            database='studytrack'
        )  
            with connection.cursor() as cursor:
                sql = "SELECT * FROM usuarios WHERE mail = %s"
                cursor.execute(sql, (self.u,))
                result = cursor.fetchone()
            self.id_u = result[0]
            progreso(self.id_u,self.usuario_sql,self.contra_sql)
        except Error as e:
            messagebox.showerror("Error", f"Error generando el grafico: {e}")
            
    def activarNotificaciones(self):
        self.Noti=Notificaciones(self)



sesion = StudyTrack(usuario_sql,contra_sql)
