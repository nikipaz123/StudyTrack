from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pymysql
import re
from tkinter import messagebox

# Solicito el URL de la pagina
def solicitar_link():
    link = 'https://sga.itba.edu.ar/app2/wxrISczAPk4'
    print('TIENE 30 SEGUNDOS PARA INICIAR SESION. POR SEGURIDAD, EN CASO CONTRARIO SE CERRARA EL SISTEMA Y TENDRA QUE EMPEZAR DE CERO.')
    return link

# Funcion para guardar la info en una tabla en sql
def guardar_notas_en_db(notas, id_usuario, u_sql, c_sql):
    # Conexion a la db
    connection = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user=u_sql,
        password=c_sql,
        database='studytrack'
    )
    
    try:
        with connection.cursor() as cursor:
                 
            # Borra entradas previas
            delete_sql = "DELETE FROM notas WHERE idusuarios = %s"
            cursor.execute(delete_sql, (id_usuario,))
            
            # Ingresa la nueva informacion
            for nota in notas:
                # Analiza si la persona sigue cursando o no
                if nota["nota_cursada"] is None:
                    nota_cursada = "Cursando"
                else:
                    nota_cursada = str(nota["nota_cursada"])
                
                # Analiza si la persona ya rindió el final o no
                if isinstance(nota["nota_final"], list):
                    if nota["nota_final"]:
                        nota_final = str(max(nota["nota_final"]))
                    else:
                        nota_final = "DEBE FINAL"
                else:
                    nota_final = str(nota["nota_final"]) if nota["nota_final"] else "DEBE FINAL"
                
                # Caso especial para "Inglés" (pq es cuestion de aprobar)
                if isinstance(nota["materia"], str) and "Inglés" in nota["materia"]:
                    if nota["nota_cursada"] is None and isinstance(nota["nota_final"], str) and "Aprobado" in nota["nota_final"]:
                        nota_cursada = "Cursada aprobada"
                
                # Si la nota de cursada es menor a 4 la nota final queda como "RECURSA"
                if isinstance(nota["nota_cursada"], (int, float)) and nota["nota_cursada"] < 4:
                    nota_final = "RECURSA"
                
                # Ingresa toda esta informacion a la db
                insert_sql = """
                INSERT INTO notas (idusuarios, materia, nota_cursada, nota_final)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_sql, (
                    id_usuario,
                    nota["materia"],
                    nota_cursada,
                    nota_final
                ))
        
        connection.commit()
        print("Notas guardadas exitosamente en la base de datos.")
        
    except Exception as e:
        print(f"Error al guardar las notas: {e}")
        connection.rollback()
    
    finally:
        connection.close()

def checkear_abierto(driver):
    try:
        driver.current_url
        return True
    except:
        return False

def notas_sga(id, u_sql, c_sql):
    # Nombro como variable el enlace que proporciono el usuario
    link = solicitar_link()

    # Configuro el driver de Selenium (usando webdriver-manager para instalar el driver de Chrome)
    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    except Exception as e:
        print("ERROR AL INICIALIZAR EL DRIVER DE CHROME:", e)
        exit()

    try:
        # El programa navega al link proporcionado
        driver.get(link)
    except Exception as e:
        print("ERROR AL INTENTAR ACCEDER AL ENLACE PROPORCIONADO:", e)
        driver.quit()
        exit()

    # Le doy 30 segundos al usuario y checkea si se cerro el browser
    for _ in range(30):
        if not checkear_abierto(driver):
            messagebox.showerror('Error',f"El navegador fue cerrado prematuramente")
            driver.quit()
            return
        time.sleep(1)
    
    
    try:
        # Navegación en la página
        if not checkear_abierto(driver):
            messagebox.showerror('Error',f"El navegador fue cerrado. Por favor intente de nuevo")
            driver.quit()
            return
        
        legajos = driver.find_elements(By.XPATH, "//body/div/div/div/div/div/div/ul[@class='nav']/li[@class='dropdown']/a")
        
        if not legajos:
            messagebox.showerror('Error', f"Pasaron los 30 segundos. Por favor intente de nuevo")
            driver.quit()
            return
        
        legajos[3].click()
        
        if not checkear_abierto(driver):
            messagebox.showerror('Error',f"El navegador fue cerrado. Por favor intente de nuevo")
            driver.quit()
            return
        
        mi_legajo = driver.find_elements(By.XPATH, "//body/div/div/div/div/div/div/ul/li/ul[@class='dropdown-menu']/li/a") # NECESITO EL 5TO
        mi_legajo[4].click()
        
        if not checkear_abierto(driver):
            messagebox.showerror('Error',f"El navegador fue cerrado. Por favor intente de nuevo")
            driver.quit()
            return
        
        datos_del_alumno = driver.find_elements(By.XPATH, "//body/div/div/div/div/div/ul[@class='nav nav-tabs']/li/a") # NECESITO EL 4TO
        datos_del_alumno[3].click()
        
        if not checkear_abierto(driver):
            messagebox.showerror('Error',f"El navegador fue cerrado. Por favor intente de nuevo")
            driver.quit()
            return
        
        historia_academica = driver.find_element(By.XPATH, "//body/div/div/div/div/div/div/div/div/ul[@class='nav nav-tabs']/li[@class='tab3']/a")
        historia_academica.click() 
        
        if not checkear_abierto(driver):
            messagebox.showerror('Error',f"El navegador fue cerrado. Por favor intente de nuevo")
            driver.quit()
            return

        time.sleep(2)

        # Creo una lista para guardar los resultados procesados
        resultados = []

        # Uso un for loop para recorrer las filas de las tablas
        driverTablas = driver.find_elements(By.XPATH, "//div[@class='backgroundBordered']/div/div/div/div/div/div/div/div")

        for i in range(len(driverTablas) - 1):
            materias = driver.find_elements(By.XPATH, f"//div[@class='backgroundBordered']/div/div/div/div/div/div/div/div[{i+1}]/div/table/tbody/tr")            
            for j in range(len(materias)):
                print(j+1)
                nombre_materia = driver.find_element(By.XPATH, f".//div[@class='backgroundBordered']/div/div/div/div/div/div/div/div[{i+1}]/div/table/tbody/tr[{j+1}]/td[2]/span[@class='bold']").text
                cursada_valor = driver.find_element(By.XPATH, f".//div[@class='backgroundBordered']/div/div/div/div/div/div/div/div[{i+1}]/div/table/tbody/tr[{j+1}]/td[3]").text
                final_valor = driver.find_element(By.XPATH, f".//div[@class='backgroundBordered']/div/div/div/div/div/div/div/div[{i+1}]/div/table/tbody/tr[{j+1}]/td[4]").text

                # Procesar los datos de las notas
                if cursada_valor == '':
                    cursada_nota = None    
                else:
                    cursada_nota = float(cursada_valor.split()[0].replace(",", ".")) if cursada_valor.split()[0].replace(",", ".").replace(".", "").isdigit() else None
                
                if 'Aprobado' in final_valor:
                    final_notas = 'Aprobado'
                else:
                    final_notas_sucio = [float(x.replace(",", ".")) for x in re.findall(r"\d+[,\.\d]*", final_valor)] #importante que puede ser mas de 1 final
                    final_notas = []
                    for k, elemento in enumerate(final_notas_sucio):
                        if int(k) % 5 == 0:
                            final_notas.append(elemento)

                # Agregar los datos procesados a la lista de resultados para hacer la tabla
                resultados.append({
                    "materia": nombre_materia,
                    "nota_cursada": cursada_nota,
                    "nota_final": final_notas
                })

    except Exception as e:
        print(f"No se pudo descargar las notas: {e}")   

    guardar_notas_en_db(resultados, id, u_sql, c_sql)  
    driver.quit()

