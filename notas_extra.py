import tkinter as tk
from PIL import Image, ImageTk
import os
import pymysql

# Este es el q hay q cambiar
def notas_extra(id, usuario_sql, contra_sql):
    # Ventana principal oculta
    root = tk.Tk()
    root.withdraw()

    def cargar_materias(usuario_sql, contra_sql):
        connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user=usuario_sql,
            password=contra_sql,
            database='studytrack'
        )
        
        cursor = connection.cursor()

        # Obtener materias registradas
        get_materias_sql = """
        SELECT nombre_materia 
        FROM materias 
        WHERE idusuarios = %s
        """
        cursor.execute(get_materias_sql, (id,))
        
        materias = [materia[0] for materia in cursor.fetchall()]
        connection.close()
        return materias

    def guardar_datos():
        materia = materia_var.get() if materias else None  # Selección de materia
        tarea = entry_tarea.get()
        nota = entry_nota.get()

        try:
            nota = float(nota)
        except ValueError:
            mensaje.config(text="La nota debe ser un número válido", fg="red")
            return

        if not tarea:
            mensaje.config(text="Por favor, ingrese el nombre de la tarea", fg="red")
            return

        if nota < 0 or nota > 10:
            mensaje.config(text="La nota debe estar entre 0 y 10", fg="red")
            return

        try:
            connection = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user=usuario_sql,
                password=contra_sql,
                database='studytrack'
            )
            cursor = connection.cursor()

            # Insertar datos
            insert_sql = """
            INSERT INTO notas_extra (idusuarios, materia, tarea, nota)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_sql, (id, materia, tarea, nota))
            connection.commit()

            mensaje.config(text="Nota guardada exitosamente", fg="green")
            entry_tarea.delete(0, tk.END)
            entry_nota.delete(0, tk.END)

        except Exception as e:
            mensaje.config(text=f"Error al guardar la nota: {str(e)}", fg="red")
            connection.rollback()
        finally:
            if connection:
                connection.close()

    # Crear ventana de ingreso
    ventana = tk.Toplevel()
    ventana.title("Ingreso de Notas")
    ventana.geometry("280x280")
    
    # Obtiene el fondo
    base_path = os.path.dirname(os.path.abspath(__file__))
    ruta_imagen = os.path.join(base_path, 'fondo_notas.png')

    if not os.path.isfile(ruta_imagen):
        print(f"No se encontró la imagen en la ruta: {ruta_imagen}")
    else:
        print(f"Imagen encontrada: {ruta_imagen}")

    try:
        imagen_original = Image.open(ruta_imagen)
        imagen_redimensionada = imagen_original.resize((280, 280))
        imagen_fondo = ImageTk.PhotoImage(imagen_redimensionada)

        label_fondo = tk.Label(ventana, image=imagen_fondo)
        label_fondo.image = imagen_fondo  # Asocia la imagen al widget
        label_fondo.place(relwidth=1, relheight=1)
    except FileNotFoundError:
        print(f"El archivo de imagen '{ruta_imagen}' no se encuentra.")

    materias = cargar_materias(usuario_sql, contra_sql)

    if materias:
        materia_var = tk.StringVar(ventana)
        materia_var.set("Sin materia")  # Opción predeterminada
        menu_materias = tk.OptionMenu(ventana, materia_var, *materias, "Sin materia")
        menu_materias.pack(pady=10)
    else:
        materia_var = tk.StringVar(ventana, value="Sin materia")
        tk.Label(ventana, text="No se encontraron materias.", fg="red").pack()

        # Entrada para el examen
    label_tarea = tk.Label(ventana, text="Examen:", fg="#B38F8F")
    label_tarea.pack()
    entry_tarea = tk.Entry(ventana, bg="#FFFFCC")
    entry_tarea.pack(pady=5)

    # Entrada para la nota
    label_nota = tk.Label(ventana, text="Nota:", fg="#B38F8F")
    label_nota.pack()
    entry_nota = tk.Entry(ventana, bg="#FFFFCC")
    entry_nota.pack(pady=5)
    
    # Para feedback
    mensaje = tk.Label(ventana, text="", fg="#B38F8F")
    mensaje.pack(pady=5)

    # Boton de guardado
    boton_guardar = tk.Button(ventana, text="Guardar", command=guardar_datos, fg="black")
    boton_guardar.pack(pady=10)

    label_mensaje = tk.Label(ventana, text="", fg="#CCCCFF")
    label_mensaje.pack()
    
    ventana.mainloop()
