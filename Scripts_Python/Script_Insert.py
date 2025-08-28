import psutil as p
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os

load_dotenv()

def inserir_porcentagem_cpu(porcentagem):

    config = {
      'user': os.getenv("USER_DB"),
      'password': os.getenv("PASSWORD_DB"),
      'host': os.getenv("HOST_DB"),
      'database': os.getenv("DATABASE_DB")
    }

    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.server_info
            print('Connected to MySQL server version -', db_info)
            
            with db.cursor() as cursor:
                query = "INSERT INTO aula_sis.cpu (id, porcentagem) VALUES (null, %s)"
                value = (porcentagem,)
                cursor.execute(query, value)
                
                db.commit()
                print(cursor.rowcount, "registro inserido")
            
            cursor.close()
            db.close()
    
    except Error as e:
        print('Error to connect with MySQL -', e) 
        
        
for i in range(20):

    porcentagem = p.cpu_percent(interval=1, percpu=False)
    print(f"Porcentagem de uso {porcentagem}%")
    inserir_porcentagem_cpu(porcentagem)
