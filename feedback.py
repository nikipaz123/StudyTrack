import mysql.connector
from mysql.connector import Error
import tkinter as t
from tkinter import messagebox
import os
from PIL import Image, ImageTk  # Para gestionar la imagen de fondo

class Feedback():
    def __init__(self, usuario_sql, contra_sql, ventana=None):
            self.usuario_sql=usuario_sql
            self.contra_sql=contra_sql
            # Usa una ventana secundaria si ya existe una ventana principal
            if ventana:
                self.ventana = t.Toplevel(ventana)
            else:
                self.ventana = t.Tk()

            self.ventana.geometry('800x400')
            self.ventana.title("Feedback - Study Track")

            self.configurar_fondo()
            self.crear_tabla_feedback()
            self.dar_feedback()

            self.ventana.mainloop()

    def configurar_fondo(self):
        # Ruta base para los archivos
        base_path = os.path.dirname(os.path.abspath(__file__))

        # Ruta de la imagen de fondo
        ruta_imagen = os.path.join(base_path, 'fondo_feedback.png')

        try:
            # Cargar la imagen original
            self.imagen_original = Image.open(ruta_imagen)
            
            # Crear un label para mostrar el fondo
            self.label_fondo = t.Label(self.ventana)
            self.label_fondo.place(relwidth=1, relheight=1)  # Ocupar toda la ventana
            
            # Detecta el redimensionamiento de la ventana
            self.ventana.bind("<Configure>", self.redimensionar_fondo)
            
            # Redimensionar el fondo inicialmente
            self.redimensionar_fondo(None)
        except Exception as e:
            print(f"Error al cargar la imagen de fondo: {e}")

    def redimensionar_fondo(self, event):
        # Obtener el tamaño actual de la ventana
        ancho = self.ventana.winfo_width()
        alto = self.ventana.winfo_height()

        # Redimensionar la imagen al tamaño de la ventana
        imagen_redimensionada = self.imagen_original.resize((ancho, alto), Image.LANCZOS)
        self.imagen_fondo = ImageTk.PhotoImage(imagen_redimensionada)  # Crear una nueva referencia

        # Actualizar el label con la nueva imagen
        self.label_fondo.config(image=self.imagen_fondo)

    def crear_tabla_feedback(self):
        try:
            conexion = mysql.connector.connect(
                host='127.0.0.1',
                database='studytrack',
                user=self.usuario_sql,
                password=self.contra_sql
            )
            if conexion.is_connected():
                cursor = conexion.cursor()
                tabla_feedback = """
                CREATE TABLE IF NOT EXISTS feedback (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre_apellido VARCHAR(255),
                    mensaje TEXT NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
                cursor.execute(tabla_feedback)
                conexion.commit()
                print("Tabla 'feedback' verificada o creada exitosamente.")
        except Error as e:
            print(f"Error al conectar o crear la tabla: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def dar_feedback(self):
        # Título
        self.feedback_titulo = t.Label(
            self.ventana,
            text="¡Déjanos tu opinión sobre Study Track!",
            font=('Arial', 13, 'bold'), 
            bg="white"  # Fondo del texto para que contraste con la imagen
        )
        self.feedback_titulo.place(relx=0.5, rely=0.1, anchor="center",relheight=0.1, relwidth=0.4)

        # Frame para el nombre
        frame_nombre = t.Frame(self.ventana, bg="#B38F8F")  
        frame_nombre.place(relx=0.3, rely=0.2, relwidth=0.4, relheight=0.07)

        # El usuario puede dejar su nombre si quiere
        self.nombre_titulo = t.Label(
            frame_nombre,
            text='Nombre (opcional):',
            font=('Arial', 10),
            anchor="e",  
            bg="#B38F8F",   
        )
        self.nombre_titulo.place(relx=0, rely=0, relheight=1, relwidth=0.4)


        self.nombre = t.Entry(frame_nombre, font=('Arial', 10))
        self.nombre.place(relx=0.45, rely=0.22, relheight=0.8, relwidth=0.3)

        # Caja de entrada para comentarios
        self.feedback = t.Text(
            self.ventana,
            font=("Arial", 12),
            wrap="word",  # Ajusto el texto automáticamente a la siguiente línea
            borderwidth=2,
            relief="solid"
        )
        self.feedback.place(relx=0.2, rely=0.3, relheight=0.4, relwidth=0.6)

        # Botón para enviar feedback
        self.almacenar_feedback = t.Button(
            self.ventana, 
            command=self.almacenar_feedback_en_db, 
            text="Enviar mi opinión",
            font=('Arial', 10), 
            anchor="center",
            bg="#FFFFCC"
            )
        self.almacenar_feedback.place(relx=0.35, rely=0.75, relheight=0.1, relwidth=0.3)

    def almacenar_feedback_en_db(self):
        nombre = self.nombre.get().strip()
        mensaje = self.feedback.get("1.0", "end").strip()

        if not mensaje:
            messagebox.showerror("Error", "El mensaje no puede estar vacío.")
            return

        try:
            conexion = mysql.connector.connect(
                host='127.0.0.1',
                database='studytrack',
                user=self.usuario_sql,
                password=self.contra_sql
            )
            if conexion.is_connected():
                cursor = conexion.cursor()
                insertar_feedback = """
                INSERT INTO feedback (nombre_apellido, mensaje) VALUES (%s, %s);
                """
                cursor.execute(insertar_feedback, (nombre, mensaje))
                conexion.commit()
                messagebox.showinfo("Éxito", "¡Gracias por tu feedback!")
                self.nombre.delete(0, "end")
                self.feedback.delete("1.0", "end")
        except Error as e:
            messagebox.showerror("Error", f"Error al guardar el feedback: {e}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

