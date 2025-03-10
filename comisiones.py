#archivo donde desde sql voy a extraer las comisiones y mostrarlas 
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql

def ver_comision(id, usuario_sql, contra_sql):
    
    try:
        # Conexión a la base de datos
        connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user=usuario_sql,
            password=contra_sql,
            database='studytrack'
        )

        # Consulta SQL
        query = "SELECT * FROM comisiones WHERE idusuarios = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, (id, ))
            rows = cursor.fetchall()
        
        # Junto la informacion en listas
        materias = []
        comisiones = []
        dias = []
        horarios = []
        aulas = []
        
        for row in rows:
            materias.append(row[2])
            comisiones.append(row[3])
            dias.append(row[4])
            horarios.append(row[5])
            aulas.append(row[6])
        
        # Devuelvo la info de las comisiones
        return materias, comisiones, dias, horarios, aulas
    except Exception as e:
        messagebox.showerror("Error", f"Error exportando comisiones: {e}")

    finally:
        if connection:
            connection.close() 
