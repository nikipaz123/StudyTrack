from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import messagebox
import time
import re
import pymysql
from selenium.webdriver.common.action_chains import ActionChains

def solicitar_link():
    
    # Solicita el enlace de la página del sistema SGA del ITBA.
    link = 'https://sga.itba.edu.ar/app2/wxrISczAPk4'
    print('TIENE 30 SEGUNDOS PARA INICIAR SESION. POR SEGURIDAD, EN CASO CONTRARIO SE CERRARA EL SISTEMA Y TENDRA QUE EMPEZAR DE CERO.')
    return link

def guardar_materias_en_db(materias, id_usuario, connection):
   
    # Guarda las materias en la tabla materias si no existen.

    # param materias: Lista de nombres de materias.
    # param id_usuario: ID del usuario al que pertenecen las materias.
    # param connection: Conexión a la base de datos MySQL
    
    try:
        with connection.cursor() as cursor:

            
            # Primero, obtener las materias existentes del usuario
            select_sql = "SELECT id, nombre_materia FROM materias WHERE idusuarios = %s"
            cursor.execute(select_sql, (id_usuario,))
            materias_existentes = {row[1]: row[0] for row in cursor.fetchall()}
            
            # Insertar o actualizar materias
            insert_sql = """
            INSERT INTO materias (idusuarios, nombre_materia) 
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE nombre_materia = VALUES(nombre_materia)
            """
            for materia in materias:
                cursor.execute(insert_sql, (id_usuario, materia))
            
            
        connection.commit()
        print('Materias actualizadas exitosamente en la base de datos.')
        
    except Exception as e:
        print(f"Error al guardar las materias: {e}")
        connection.rollback()

def obtener_datos(datos_de_comision):
    """
    Procesa los datos de texto de una comisión para obtener su día, horario y aula.

    :param datos_de_comision: Texto con los datos de la comisión.
    :return: Tupla con (día, horario, aula).
    """
    datos_de_comision_en_lista = datos_de_comision.split(' ')
    dia = datos_de_comision_en_lista[0]
    horario = ' '.join(datos_de_comision_en_lista[1:4])
    aula = ' '.join(datos_de_comision_en_lista[4:])
    return dia, horario, aula

def obtener_comisiones(driver, materias):
    
    # Obtiene las comisiones de las materias navegando en la página.

    # param driver: Instancia del navegador Selenium.
    # param materias: Lista de nombres de las materias.
    # return: Lista de diccionarios con los datos de las comisiones.
    
    datos_comisiones = []
    filas = driver.find_elements(By.XPATH, "//tbody/tr/td/a")
    for i in range(1, len(filas) + 1):
        lupita = driver.find_element(By.XPATH, f"//tbody/tr[{str(i)}]/td/a")
        try:
            actions = ActionChains(driver)
            actions.move_to_element(lupita).perform()
            lupita.click()

            boton = driver.find_element(By.XPATH, "//body/div/div/div/div/div/div/ul/li[@class='tab1']/a")
            boton.click()

            filas2 = driver.find_elements(By.XPATH, "//table/tbody/tr")
            for j in range(1, len(filas2) + 1):
                identificador = driver.find_element(By.XPATH, f"//table/tbody/tr[{j}]/td/label[@class='centered']").text
                horarios = driver.find_elements(By.XPATH, f"//table/tbody/tr[{j}]/td[2]/div")
                for comision in horarios:
                    try:
                        dia, horario, aula = obtener_datos(comision.text)
                        datos_comisiones.append({
                            "Materia": materias[i - 1],
                            "ID": identificador,
                            "Dia": dia,
                            "Horario": horario,
                            "Aula": aula,
                        })
                    except Exception as e:
                        print(f"No se encontraron comisiones: {e}")
                        continue

            driver.back()
            driver.back()

        except Exception as e:
            print(f"No se encontró el botón en esta fila: {e}")
            continue

    return datos_comisiones

def checkear_abierto(driver):
    try:
        driver.current_url
        return True
    except:
        return False


def procesar_comisiones(id_usuario,usuario_sql,contra_sql):
    
    # Proceso principal para obtener y guardar las comisiones de las materias.    

    messagebox.Message('Tiene 30 segundos para ingresar al sga. Pasado ese tiempo se cerrará la ventana por seguridad. Una vez ingresad/a a la página, no la cierre hasta que el proceso haya finalizado')
    link = solicitar_link()

    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(link)
    except Exception as e:
        messagebox.showerror('Error', f"ERROR AL INICIALIZAR O ACCEDER AL DRIVER DE CHROME:{str(e)}")
        print("ERROR AL INICIALIZAR O ACCEDER AL DRIVER DE CHROME:", e)
        if driver:
            driver.quit()
        return

    # Si el usuario no ingresa en 30segs o cierra el navegador se cierra el browser
    for _ in range(30):
        if not checkear_abierto(driver):
            messagebox.showerror('Error',f"El navegador fue cerrado prematuramente")
            driver.quit()
            return
        time.sleep(1)
    


    try:
        materias_tags = driver.find_elements(By.XPATH, '//td')
        materia_pattern = re.compile(r'^\d{2}\.\d{2} - .+')
        materias = [tag.text.strip() for tag in materias_tags if materia_pattern.match(tag.text.strip())]
        
        if not materias:
            messagebox.showerror('Error', f"Pasaron los 30 segundos. Por favor intente de nuevo")
            driver.quit()
            return
        
        if not checkear_abierto(driver):
            messagebox.showerror('Error',f"El navegador fue cerrado. Por favor intente de nuevo")
            driver.quit()
            return
                
        
        datos_comisiones = obtener_comisiones(driver, materias)
        

        # Abro la conexion a la base de datos
        connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user=usuario_sql,
            password=contra_sql,
            database='studytrack'
        )

        if not checkear_abierto(driver):
            messagebox.showerror('Error',f"El navegador fue cerrado. Por favor intente de nuevo")
            driver.quit()
            return
        
        try:
            # Obtengo los datos sin repetir, usando un SET!! para eliminar duplicados
            materias_unicas = sorted(set(comision["Materia"] for comision in datos_comisiones))
            
            # Guarda las materias en la tabla de materias
            guardar_materias_en_db(materias_unicas, id_usuario, connection)
            
            with connection.cursor() as cursor:
                
                # Borra info previa (del cuatri anterior por ej)
                delete_sql = "DELETE FROM comisiones WHERE idusuarios = %s"
                cursor.execute(delete_sql, (id_usuario,))
                
                # Ingresa las nuevas materias
                insert_sql = """
                INSERT INTO comisiones (idusuarios, materia, comision_id, dia, horario, aula)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                for comision in datos_comisiones:
                    cursor.execute(insert_sql, (
                        id_usuario,
                        comision["Materia"],
                        comision["ID"],
                        comision["Dia"],
                        comision["Horario"],
                        comision["Aula"]
                    ))
                    
            connection.commit()
            
        except Exception as e:
            messagebox.showerror(f"Error al guardar en la base de datos: {e}", error=True)
            connection.rollback()
            
        finally:
            connection.close()
            if driver:
                driver.quit()
                print("Navegador cerrado correctamente.")
    except Exception as e:
        messagebox.showerror('Error', f"ERROR AL IPROCESAR LAS MATERIAS: {str(e)}")
        print("ERROR AL PROCESAR LAS MATERIAS:", e)
    finally:
        if driver:
            driver.quit()


