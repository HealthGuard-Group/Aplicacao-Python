import psutil as p
from mysql.connector import connect, Error


def inserir_porcentagem_cpu(porcentagem):

    config = {
      'user': "seu usuário",
      'password': "sua senha",
      'host': 'seu host, (se local é localhost)',
      'database': "seu banco de dados"
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
