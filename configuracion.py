import pymysql
import bcrypt
from registrarse import validar_email

def modificar_nombre(mail, name, usuario_sql, contra_sql):
    # Abro coneccion
    connection = pymysql.connect(host='127.0.0.1', port=3306, user=usuario_sql, password=contra_sql, database='studytrack')
    cursor = connection.cursor()

    # Pido inputs, si estan vacios devuelvo error
    while True:
        nombre = name.strip()
        if nombre:
            break
        return 0#print("Por favor, ingrese su nombre actualizado")
    
    try:
        cursor.execute(f"UPDATE usuarios SET nombre = '{nombre}' WHERE mail = '{mail}'")
        connection.commit()
        return 1 #print('Cambio realizado con éxito')
        # Hacer los cambios a la bd ---> commit
        
    except:
        # Volver para atras y deshacer los cambios ---> rollback
        return 2 # print('Ocurrió un error al actualizar su nombre')
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

def modificar_apellido(mail, new_ape, usuario_sql, contra_sql):
    # Abro coneccion
    connection = pymysql.connect(host='127.0.0.1', port=3306, user=usuario_sql, password=contra_sql, database='studytrack')
    cursor = connection.cursor()

    # Pido inputs, si estan vacios devuelvo error
    while True:
        apellido = new_ape.strip()
        if apellido:
            break
        return 0 #print("Por favor, ingrese su apellido actualizado")
    
    try:
        cursor.execute(f"UPDATE usuarios SET apellido = '{apellido}' WHERE mail = '{mail}'")
        connection.commit()
        return 1# print('Cambio realizado con éxito')
        # Hacer los cambios a la bd ---> commit
        
    except:
        # Volver para atras y deshacer los cambios ---> rollback
        return 2 #print('Ocurrió un error al actualizar su apellido')
    finally:
        cursor.close()
        connection.close()
        
def modificar_mail(mail, nuevo_mail, usuario_sql, contra_sql):
    # Abro coneccion
    connection = pymysql.connect(host='127.0.0.1', port=3306, user=usuario_sql, password=contra_sql, database='studytrack')
    cursor = connection.cursor()

    # Pido inputs, si estan vacios o no es valido devuelvo error
    while True:
        nombre = nuevo_mail.strip()
        if not validar_email(nombre):
            return 4
        if nombre:
            break
        return 0 #print("Por favor, ingrese su mail actualizado")
        
    
    try:
        cursor.execute(f"UPDATE usuarios SET mail = '{nombre}' WHERE mail = '{mail}'")
        connection.commit()
        return 1 #print('Cambio realizado con éxito')
        # Hacer los cambios a la bd ---> commit

    except pymysql.err.IntegrityError as e:
        connection.rollback() 
        return 2 #print("Error: Este mail ya esta ligado a un usuario existente")
    except:
        # Volver para atras y deshacer los cambios ---> rollback
        return 3 #print('Ocurrió un error al actualizar su mail')
    finally:
        cursor.close()
        connection.close()

def modificar_contra(mail, password, new_password, usuario_sql, contra_sql):
       # Abro coneccion
   connection = pymysql.connect(host='127.0.0.1', port=3306, user=usuario_sql, password=contra_sql, database='studytrack')
   cursor = connection.cursor()
  
   errores = set()


   # Pido inputs, si estan vacios devuelvo error
  
   passw1 = password.strip()
   if passw1:
       # Checkea el largo
       if len(passw1) < 8:
           errores.add('0')
          
       # Checkea que haya una mayuscula
       if not any(c.isupper() for c in passw1):
           errores.add('1')
      
       # Checkea que haya un numero
       if not any(c.isdigit() for c in passw1):
           errores.add('2')
   else:        
       errores.add('3') #esta vacia


   passw2 = new_password.strip()
   if not passw2:
       errores.add('3')
   elif passw1 != passw2:
       errores.add('4')


   # Verifico que no hayan errores antes de cambiar contra
   if list(errores) == []:
       passw_encriptada = bcrypt.hashpw(passw1.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


       try:
           cursor.execute(f"UPDATE usuarios SET passw = '{passw_encriptada}' WHERE mail = '{mail}'")
           connection.commit()
           errores.add('5')  # Cambio realizado con éxito
       except:
           # Volver para atras y deshacer los cambios ---> rollback
           errores.add('6')  # Ocurrió un error al actualizar su contraseña
       finally:
           cursor.close()
           connection.close()
  
   return errores
