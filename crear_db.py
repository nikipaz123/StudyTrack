import mysql.connector

# La funcion crear tablas crea la base de datos studytrack y todas sus tablas, si es que no existen todavia
# Se debe utilizar cada vez al iniciar el programa
def crear_tablas(usuario_sql,contra_sql):
    try:
        # Conectar a mysql
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            user=usuario_sql,
            password=contra_sql
        )
        
        cursor = connection.cursor()

        # Creala bd si no existia antes
        cursor.execute("CREATE DATABASE IF NOT EXISTS studytrack")
        cursor.execute("USE studytrack")

        # Crea la tabla de usuarios con la info que se saca de registrarse
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                idusuarios INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(45) NOT NULL,
                apellido VARCHAR(45) NOT NULL,
                passw VARCHAR(255) NOT NULL,
                mail VARCHAR(100) NOT NULL UNIQUE,
                palabra_clave VARCHAR(255) NOT NULL
            )
        """)

        # Crea la tabla de materias con la info que va a poner el usuario o cargar de sga
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS materias (
                id INT AUTO_INCREMENT PRIMARY KEY,
                idusuarios INT,
                nombre_materia VARCHAR(255),
                FOREIGN KEY (idusuarios) REFERENCES usuarios(idusuarios),
                UNIQUE KEY unique_materia_usuario (idusuarios, nombre_materia)
            )
        """)
        
        # Crea la tabla cronogramas con los cronogramas que cargue el usuario
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cronogramas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                idusuarios INT,
                id_materia INT,
                dia_de_la_semana VARCHAR(20),
                horas_planeadas FLOAT,
                fecha_inicio DATE,
                fecha_final DATE,
                FOREIGN KEY (idusuarios) REFERENCES usuarios(idusuarios),
                FOREIGN KEY (id_materia) REFERENCES materias(id)
            )
        """)
        
        # Crea la tabla de horas estudiadas para guardar la informacion que se recolecta con el cronometro
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS horas_estudiadas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                idusuarios INT,
                id_materia INT,
                fecha_estudio DATE,
                horas FLOAT,
                FOREIGN KEY (idusuarios) REFERENCES usuarios(idusuarios),
                FOREIGN KEY (id_materia) REFERENCES materias(id)
            )
        """)
        
        # Crea la tabla para administrar las rachas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rachas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                idusuarios INT,
                id_materia INT,
                racha_actual INT,
                mejor_racha INT,
                ultimo_update DATE,
                FOREIGN KEY (idusuarios) REFERENCES usuarios(idusuarios),
                FOREIGN KEY (id_materia) REFERENCES materias(id)
            )
        """)
        
        # Crea la tabla donde se guardan las notas extra que agrega el usuario
        cursor.execute("""
           CREATE TABLE IF NOT EXISTS notas_extra (
            id INT AUTO_INCREMENT PRIMARY KEY,
            idusuarios INT,
            materia VARCHAR(255),
            tarea VARCHAR(255),
            nota DECIMAL(4,2),
            FOREIGN KEY (idusuarios) REFERENCES usuarios(idusuarios)
            )
        """)
        
        # Crea la tabla donde se guardan las notas cargadas del SGA
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notas (
                idnotas INT AUTO_INCREMENT PRIMARY KEY,
                idusuarios INT,
                materia VARCHAR(255),
                nota_cursada VARCHAR(50),
                nota_final VARCHAR(50),
                FOREIGN KEY (idusuarios) REFERENCES usuarios(idusuarios)
            )
        """)
        
        # Crea la tabla donde se guardan las materias y comisiones extraidas de SGA
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comisiones (
                    idcomision INT AUTO_INCREMENT PRIMARY KEY,
                    idusuarios INT,
                    materia VARCHAR(255),
                    comision_id VARCHAR(50),
                    dia VARCHAR(50),
                    horario VARCHAR(50),
                    aula VARCHAR(255),
                    FOREIGN KEY (idusuarios) REFERENCES usuarios(idusuarios)
            )
        """)
        
        # Crea la tabla donde se guarda el feedback del usuario
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre_apellido VARCHAR(255),
                    mensaje TEXT NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        connection.commit()
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            
#crear_tablas()