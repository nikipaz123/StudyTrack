import datetime
from tkinter import messagebox
import threading

class Notificaciones:
    def __init__(self, studytrack):
        self.studytrack = studytrack 
        self.ejecutar_automatico()  

    def obtener_materias(self):
        return self.studytrack.obtener_materias_usuario(self.studytrack.id_u)

    def calcular_fin_del_dia(self):
        ahora = datetime.datetime.now()
        fin_del_dia = datetime.datetime.combine(ahora.date(), datetime.time(23, 59, 59))
        return (fin_del_dia - ahora).total_seconds() / 3600

    def calcular_horas_minutos(self, horas):
        return divmod(horas * 60, 60)

    def mostrar_mensaje(self, nombre_materia, horas_restantes_h, minutos_restantes, horas_disponibles_h, minutos_disponibles):
        mensaje = (
            f"\u00a1Atención!\n"
            f"Para la materia '{nombre_materia}':\n"
            f"Faltan {int(horas_restantes_h)} horas y {int(minutos_restantes)} minutos para cumplir tu objetivo diario.\n"
            f"El día termina en {int(horas_disponibles_h)} horas y {int(minutos_disponibles)} minutos."
        )
        messagebox.showwarning("Notificación de Estudio", mensaje)

    def notificaciones(self):
        ahora = datetime.datetime.now() 
        materias = self.obtener_materias() 

        if materias: 
            for materia in materias:
                id_materia = materia['id']
                nombre_materia = materia['nombre_materia'] 
                cronograma = self.studytrack.cargar_cronograma(self.studytrack.id_u, id_materia, ahora)
                dia_actual = ahora.strftime('%A')

                horas_planeadas = cronograma.get(dia_actual, 0)  

                if horas_planeadas > 0:  
                    horas_totales_hoy = self.studytrack.total_horas_hoy(self.studytrack.id_u, id_materia, ahora)
                    horas_restantes = max(horas_planeadas - horas_totales_hoy, 0)  

                    horas_disponibles = self.calcular_fin_del_dia()  

                    if horas_restantes > 0:  
                        horas_restantes_h, minutos_restantes = self.calcular_horas_minutos(horas_restantes)
                        horas_disponibles_h, minutos_disponibles = self.calcular_horas_minutos(horas_disponibles)
                        self.mostrar_mensaje(nombre_materia, horas_restantes_h, minutos_restantes, horas_disponibles_h, minutos_disponibles)
        else:
            messagebox.showinfo(
                "Notificación de Estudio",
                "No se encontraron materias registradas. Por favor, registre materias para activar las notificaciones."
            )

    def ejecutar_automatico(self):
        self.notificaciones()
        threading.Timer(3600, self.ejecutar_automatico).start()