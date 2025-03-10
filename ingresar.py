import pymysql
import bcrypt

def ingresar(usuario, password,u_sql,c_sql):
    connection = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user=u_sql,
        password=c_sql,
        database='studytrack'
    )
    
    try:
        while True:
            while True:
                mail =usuario.strip()
                if mail:
                    break
                return 0
            while True:
                passw = password.strip()
                if passw:
                    break
                return 1
            
            with connection.cursor() as cursor:
                sql = "SELECT passw FROM usuarios WHERE mail = %s"
                cursor.execute(sql, (mail,))
                result = cursor.fetchone()
                
                if result:
                    stored_password = str(result[0])                       
                    password_to_check = passw.encode('utf-8')
                    stored_password = stored_password.encode('utf-8')
                    
                    try:
                        if bcrypt.checkpw(password_to_check, stored_password):
                            return 2

                        else:
                            return 3
                    except ValueError as e:
                        return 4
                else:
                    return 5
    
    except Exception as e:
        return 6
    finally:
        connection.close()

