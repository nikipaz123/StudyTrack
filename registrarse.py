import pymysql
import bcrypt
import re


def validar_email(email):
    # Formato basico de mail
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Checkear si el email coincide
    if not re.match(pattern, email):
        return False
    
    # Checkea largo de email
    if len(email) > 99:  # Largo maximo del mail
        return False
        
    return True

def registrarse(nom, ape, u, p, confirmar, c, usuario_sql, contra_sql):
    # Abro conexion
    connection = pymysql.connect(host='127.0.0.1', port=3306, user=usuario_sql, password=contra_sql, database='studytrack')
    cursor = connection.cursor()

    # Pido inputs, si estan vacios devuelvo error
    while True:
        nombre = nom.strip()
        if nombre:
            if len(nombre) > 45:
                return 15
            break
        return 0


    while True:
        apellido = ape.strip()
        if apellido:
            if len(apellido) > 45:
                return 14
            break
        return 1


    while True:
        mail = u.strip()
        if not mail:
            return 2
        if not validar_email(mail):
            return 12  
        break


    while True:
        passw1 = p.strip()
        if passw1:
            # Checkea el largo
            if len(passw1) < 8:
                return 3
                continue
            
            # Checkea que haya una mayuscula
            if not any(c.isupper() for c in passw1):
                return 4
                continue
            
            # Checkea que haya un numero
            if not any(c.isdigit() for c in passw1):
                return 5
                continue
                
            break
        return 6

        

    while True:
        passw2 = confirmar.strip()
        if not passw2:
            return 7
        elif passw1 != passw2:
            return 8
        else:
            break

    
    while True:
        palabra_clave = c.strip()
        if not c.strip():
            return 9
        else:
            break  

    
    # Hashear la contraseña y la palabra clave
    passw_encriptada = bcrypt.hashpw(passw1.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  # Convertimos a string para almacenarlo
    p_clave_encriptada = bcrypt.hashpw(palabra_clave.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
    sql = f"INSERT INTO usuarios (nombre, apellido, passw, mail, palabra_clave) VALUES ('{nombre}', '{apellido}', '{passw_encriptada}', '{mail}', '{p_clave_encriptada}')"


    try:
        cursor.execute(sql)
        connection.commit()
        return 13
    # Detecta si el mail esta repetido en la base de datos (la base de datos debe tener la fila de mail como principal y sin repetidos)
    except pymysql.err.IntegrityError as e:
        connection.rollback() 
        return 10
    except Exception as e:
        print(f"Error en registro: {e}")
        return 11

    finally:
        cursor.close()
        connection.close()
