import psutil as p
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os
import datetime
import time

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
    index_memoria = 1 
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
                query = "INSERT INTO healthguard.captura (fkComponente, GB_LIVRE, GB_EM_USO, PORCENTAGEM_DE_USO, dtCaptura) VALUES (%s, %s, %s, %s, %s)"
                value = (index_disco, disco_livre_gb, disco_usado_formatado, disco_percent, datetime.datetime.now())
                cursor.execute(query, value)
                db.commit()
                print("")
            db.close()
    except Error as e:
        print('Erro ao conectar com MySQL -', e) 




    #############################################################################################################
        

def inserir_dados_rede(mbps_upload, mbps_download):
    index_rede = 3
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
                query = "INSERT INTO healthguard.captura (fkComponente,  Mbps_upload,  Mbps_download, dtCaptura) VALUES (%s, %s, %s, %s)"
                value = (index_rede, mbps_upload, mbps_download, datetime.datetime.now())
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

    ########################################################################

    initial_bytes_sent = p.net_io_counters().bytes_sent ## quantidade de bytes enviados
    initial_bytes_recv = p.net_io_counters().bytes_recv ## quantidade de bytes recebidos
    time.sleep(1) # Espera por 1 segundo

    final_bytes_sent = p.net_io_counters().bytes_sent # Obtenha as contagens de bytes finais
    final_bytes_recv = p.net_io_counters().bytes_recv # Obtenha as contagens de bytes finais

    bytes_sent_per_second = final_bytes_sent - initial_bytes_sent # Calcula a diferença entre as leituras finais e iniciais para obter os bytes transferidos e divida pelo tempo (1 segundo) para obter a velocidade. 
    bytes_recv_per_second = final_bytes_recv - initial_bytes_recv

    mbps_download = f'{(bytes_recv_per_second * 8) / 1000000:.2f}'
    mbps_upload =  f'{(bytes_sent_per_second * 8) / 1000000:.2f}'

    # Velocidade em Mbps (Megabits por segundo)
    print(f"Mbps de upload: {(bytes_sent_per_second * 8) / 1000000:.2f}")
    print(f"Mbps de download: {(bytes_recv_per_second * 8) / 1000000:.2f}")




    print(f"""

<=============> Dados Inseridos no banco de dados com Sucesso!: <===================>
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

        ###############################################
          
          Mbps de download da rede: {mbps_download}

        ###############################################
          
          Mbps de upload da rede: {mbps_upload}



""")


    inserir_porcentagem_cpu(porcentagem)
    inserir_dados_memoria(memoria_livre_GB, memoria_usada_GB)
    inserir_dados_disco(disco_percent, disco_livre_gb, disco_usado_formatado)
    inserir_dados_rede(mbps_download, mbps_upload)