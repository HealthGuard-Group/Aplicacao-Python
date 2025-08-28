import psutil as p
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os
import datetime

load_dotenv()
#################################################################


def inserir_porcentagem_cpu(porcentagem):


    index_cpu = 4


    config = {
      'user': os.getenv("USER"),
      'password': os.getenv("PASSWORD"),
      'host': os.getenv("HOST"),
      'database': os.getenv("DATABASE")
    }

    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.server_info
            print('Connected to MySQL server version -', db_info)
           
            with db.cursor() as cursor:
                query = "INSERT INTO healthguard.captura (fkComponente, PORCENTAGEM_DE_USO, dtCaptura) VALUES (%s, %s, %s)"
                value = (index_cpu, porcentagem, datetime.datetime.now())
                cursor.execute(query, value)
               
                db.commit()
                print(cursor.rowcount, )
           
            cursor.close()
            db.close()
   
    except Error as e:
        print('Error to connect with MySQL -', e)

######################################################################################################




def inserir_dados_memoria(memoria_GB_free, memoria_usada_GB):
    index_memoria = 1 # ID do componente 'Memória RAM'
    config = {
        'user': os.getenv("USER"),
        'password': os.getenv("PASSWORD"),
        'host': os.getenv("HOST"),
        'database': os.getenv("DATABASE")
    }
    try:
        db = connect(**config)
        if db.is_connected():
            with db.cursor() as cursor:
                # O comando SQL agora tem duas colunas para a memória
                query = "INSERT INTO healthguard.captura (fkComponente, GB_LIVRE, GB_EM_USO, dtCaptura) VALUES (%s, %s, %s, %s)"
                value = (index_memoria, memoria_GB_free, memoria_usada_GB, datetime.datetime.now())
                cursor.execute(query, value)
                db.commit()
                print("")
            db.close()
    except Error as e:
        print('Erro ao conectar com MySQL -', e)
       
##############################################################################################    

def inserir_dados_disco(disco_percent, disco_livre_gb, disco_usado_formatado):
    index_disco = 2
    config = {
        'user': os.getenv("USER"),
        'password': os.getenv("PASSWORD"),
        'host': os.getenv("HOST"),
        'database': os.getenv("DATABASE")
    }
    try:
        db = connect(**config)
        if db.is_connected():
            with db.cursor() as cursor:
                # O comando SQL agora tem duas colunas para a memória
                query = "INSERT INTO healthguard.captura (fkComponente, GB_LIVRE, GB_EM_USO, PORCENTAGEM_DE_USO, dtCaptura) VALUES (%s, %s, %s, %s, %s)"
                value = (index_disco, disco_livre_gb, disco_usado_formatado, disco_percent, datetime.datetime.now())
                cursor.execute(query, value)
                db.commit()
                print("")
            db.close()
    except Error as e:
        print('Erro ao conectar com MySQL -', e)  


for i in range(4):

    ###############################################################################
    porcentagem = p.cpu_percent(interval=1, percpu=False)
  ###########################################################################

   
    memoria = p.virtual_memory() ## captura dados e métricas da memoria
   

    memoria_livre = memoria.available   ## memoria livre em bytes

    memoria_GB_free = memoria_livre / (1024**3)   ## memoria convertida pra GB
 
    memoria_formatada = f"{memoria_GB_free:.2f} GB" ## memoria formatada com 2 casas decimais
   
  

    ###############################################################################

    memoria_total_GB = memoria.total / (1024**3) # Captura memoria TOTAL


    memoria_livre_GB = memoria.available / (1024**3) # Memória livre em GB, Captura memoria livre


    memoria_usada_GB = memoria_total_GB - memoria_livre_GB # faz oepração aritmetica para saber o GB EM USO

    memoria_formatada_em_uso = f'{memoria_usada_GB:.2f}'

    #################################################################################
    # Captura o uso do disco da partição raiz '/'
    disco_objeto = p.disk_usage('/')
    disco_percent =  p.disk_usage('/').percent



     # Espaço livre em bytes
    disco_livre_bytes = disco_objeto.free

     # Espaço livre em GB
    disco_livre_gb = disco_livre_bytes / (1024**3)

     # Porcentagem de espaço livre
    porcentagem_livre = disco_objeto.free / disco_objeto.total * 100

    # disco usado captura disco usado
    disco_usado_gb = (disco_objeto.total - disco_livre_bytes) / (1024**3) 


    disco_usado_formatado = f'{disco_usado_gb:.2f}'





   

   

    print(f"""

    <=============> Dados Inseridos: <===================>
          Porcentagem de uso da CPU: {porcentagem}%

        ##############################################
         
          GB de Memória RAM Livre: {memoria_GB_free:.2f}GB

        ##############################################
         
          GB de Memória RAM em Uso: {memoria_formatada_em_uso}GB

        ##############################################
         
          Porcentagem de uso do disco: {disco_percent}

        ##############################################

          GB livre do disco: {disco_livre_gb}

        ##############################################

          Disco em uso: {disco_usado_formatado}



""")




    inserir_porcentagem_cpu(porcentagem)
    inserir_dados_memoria(memoria_livre_GB, memoria_usada_GB)
    inserir_dados_disco(disco_percent, disco_livre_gb, disco_usado_formatado)