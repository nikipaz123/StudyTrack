import pymysql
from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np
import random
from tkinter import messagebox

def generar_color_pastel():
    # Generar un color pastel aleatorio en formato hex
    return f'#{random.randint(200, 255):02X}{random.randint(200, 255):02X}{random.randint(200, 255):02X}'

def progreso(id,u_sql,c_sql):
    # DICCIONARIO para almacenar el tiempo trabajado por día y materia
    tiempos_por_dia = {}

    # Conexión a la base de datos
    connection = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user=u_sql,
        password=c_sql,
        database='studytrack'
    )
    
    with connection.cursor() as cursor:
        # Seleccionar tiempo, fecha y materia de la tabla horas_estudiadas
        sql = """
        SELECT horas, fecha_estudio, id_materia 
        FROM horas_estudiadas 
        WHERE idusuarios = %s
        """
        cursor.execute(sql, (id,))
        resultados = cursor.fetchall()  # Recuperar todos los datos
        
        # Obtener los nombres de las materias desde la tabla materias
        sql_materias = """
        SELECT id, nombre_materia FROM materias WHERE idusuarios = %s
        """
        cursor.execute(sql_materias, (id,))
        materias_info = cursor.fetchall()

    connection.close()
    
    # Crear un diccionario con id_materia como clave y nombre_materia como valor
    materias_nombres = {materia[0]: materia[1] for materia in materias_info}
    
    # Procesar resultados
    for fila in resultados:
        horas, fecha_estudio, materia = fila  # Cada fila contiene tiempo y fecha (fecha es datetime.date)
        
        # Convertir tiempo directamente a float (ya es decimal en horas)
        if isinstance(horas, (float, int)):
            tiempo_horas = horas
        elif isinstance(horas, str):
            tiempo_horas = float(horas)  # Por si viene como cadena
        else:
            raise ValueError(f"Formato desconocido para tiempo: {horas}")
        
        # Crear estructura para la materia si no existe
        if materia not in tiempos_por_dia:
            tiempos_por_dia[materia] = {}
        
        # Sumar la duración al total de esa fecha para la materia
        if fecha_estudio in tiempos_por_dia[materia]:
            tiempos_por_dia[materia][fecha_estudio] += tiempo_horas
        else:
            tiempos_por_dia[materia][fecha_estudio] = tiempo_horas

    # Ordenar fechas
    fechas = sorted({fecha for tiempos in tiempos_por_dia.values() for fecha in tiempos.keys()})
    
    #checkea si hay fechas previas
    if not fechas or len(fechas) == 0:
        messagebox.showinfo("Sin datos", "No hay datos de estudio para mostrar")
        return

    # Crear un rango completo de fechas, asi en los dias que no hay tareas, se marca como q no hizo nada
    rango_fechas = [fechas[0] + timedelta(days=i) for i in range((fechas[-1] - fechas[0]).days + 1)]
    
    # Reducir a los últimos 7 días (si estudia a lo largo de un mes, se muestra por semana)
    rango_fechas = rango_fechas[-7:]  # Tomar los últimos 7 días del rango

    # Rellenar días faltantes con duración cero
    for materia, tiempos in tiempos_por_dia.items():
        for fecha in rango_fechas:
            if fecha not in tiempos:
                tiempos[fecha] = 0      # Hay 0 horas en los dias q no trabaja

    # Preparar datos para el gráfico apilado con todas las materias
    materias = sorted(tiempos_por_dia.keys())
    datos_por_dia = {fecha: [tiempos_por_dia[materia][fecha] for materia in materias] for fecha in rango_fechas}

    # Convertir a formato adecuado para graficar
    fechas_formateadas = [fecha.strftime("%Y-%m-%d") for fecha in rango_fechas]
    valores_por_materia = np.array([datos_por_dia[fecha] for fecha in rango_fechas]).T

    # Crear lista de colores pastel aleatorios, asegurándonos de que no se repitan
    colores_pastel = []
    while len(colores_pastel) < len(materias):
        color = generar_color_pastel()
        if color not in colores_pastel:
            colores_pastel.append(color)
    
    # Graficar
    plt.figure(figsize=(12, 8))
    bottom = np.zeros(len(rango_fechas))

    for i, materia in enumerate(materias):
        # Reemplazar el id de la materia por su nombre en las etiquetas
        plt.bar(fechas_formateadas, valores_por_materia[i], bottom=bottom, label=materias_nombres.get(materia, f"Materia {materia}"), color=colores_pastel[i])
        bottom += valores_por_materia[i]

    plt.title("Tiempo Total Trabajado por Día y Materia (Horas)", fontsize=16)
    plt.xlabel("Fecha", fontsize=12)
    plt.ylabel("Horas Trabajadas", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title="Materias")
    plt.tight_layout()
    plt.show()
