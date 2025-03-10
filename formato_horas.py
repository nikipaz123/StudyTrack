
#esta funcion se utiliza mucho y permite transformar un input de horas a horas, minutos, segundos
def formatear_tiempo(horas):
        # Basado en segundos
        segundos_totales = int(horas * 3600)
        
        # Calcular segun segundos
        horas = segundos_totales // 3600
        segundos_totales %= 3600
        minutos = segundos_totales // 60
        segundos = segundos_totales % 60
        
        # Si hay horas mostrar horas, minutos y segundos
        if horas > 0:
            partes = []
            partes.append(f"{horas} {'hora' if horas == 1 else 'horas'}")
            if minutos > 0:
                partes.append(f"{minutos} {'minuto' if minutos == 1 else 'minutos'}")
            if segundos > 0:
                partes.append(f"{segundos} {'segundo' if segundos == 1 else 'segundos'}")
        # Si hay minutos y no horas solo minutos y segundos
        elif minutos > 0:
            partes = []
            partes.append(f"{minutos} {'minuto' if minutos == 1 else 'minutos'}")
            if segundos > 0:
                partes.append(f"{segundos} {'segundo' if segundos == 1 else 'segundos'}")
        # Si solo hay segundos
        else:
            return f"{segundos} {'segundo' if segundos == 1 else 'segundos'}"
        
        if len(partes) == 1:
            return partes[0]
        elif len(partes) == 2:
            return f"{partes[0]} y {partes[1]}"
        else:
            return f"{partes[0]}, {partes[1]} y {partes[2]}"