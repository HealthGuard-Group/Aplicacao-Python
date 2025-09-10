import psutil as p
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os
import datetime
import time
import platform

load_dotenv()

config = {
      'user': os.getenv("USER"),
      'password': os.getenv("PASSWORD"),
      'host': os.getenv("HOST"),
      'database': os.getenv("DATABASE")
    }

def inserir_porcentagem_cpu(porcentagem, dono_maquina):
    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.server_info

            with db.cursor() as cursor:
                
                index_cpu = 3
    
                query = "INSERT INTO healthguard.captura (fkComponente, porcentagemDeUso, hostname, dtCaptura) VALUES (%s, %s, %s, %s)"
                value = (index_cpu, porcentagem, dono_maquina, datetime.datetime.now())
                cursor.execute(query, value)
                   
                db.commit()    
            db.close()
   
    except Error as e:
        print('Error to connect with MySQL -', e)


def inserir_dados_memoria(memoria_GB_free, memoria_usada_GB, dono_maquina):
    try:
        db = connect(**config)
        if db.is_connected():
            with db.cursor() as cursor:

                id_memoria = 1

                query = "INSERT INTO healthguard.captura (fkComponente, gbLivre, gbEmUso, hostname, dtCaptura) VALUES (%s, %s, %s, %s, %s)"
                value = (id_memoria, memoria_GB_free, memoria_usada_GB, dono_maquina, datetime.datetime.now())

                cursor.execute(query, value)
                db.commit()
                print("")
            db.close()
    except Error as e:
        print('Erro ao conectar com MySQL -', e)

def inserir_dados_disco(disco_percent, disco_livre_gb, disco_usado_formatado, dono_maquina):
    try:
        db = connect(**config)
        if db.is_connected():
            with db.cursor() as cursor:
                
                id_disco = 2
                query = "INSERT INTO healthguard.captura (fkComponente, gbLivre, gbEmUso, porcentagemDeUso, hostname,dtCaptura) VALUES (%s, %s, %s, %s, %s, %s)"
                value = (id_disco,  disco_livre_gb, disco_usado_formatado, disco_percent, dono_maquina, datetime.datetime.now())
                cursor.execute(query, value)
                db.commit()
                print("")
            db.close()  
    except Error as e:
        print('Erro ao conectar com MySQL -', e)         


for i in range(30):
 
 # HOSTNAME DA MAQUINA
    dono_maquina = platform.node()

# DADOS DA MEMORIA
  

    memoria = p.virtual_memory() # CAPTURA TODAS AS METRICAS DA MEMORIA
    memoria_livre = memoria.available  # MEMORIA LIVRE EM BYTES
    memoria_GB_free = memoria_livre / (1024**3)   # CONVERTE OS BYTES DA MEMORIA LIVRE EM GB
    memoria_formatada = f"{memoria_GB_free:.2f} GB" #  FORMATA COM 2 CADAS DECIMAIS
   
    memoria_total_GB = memoria.total / (1024**3) # CAPTURA MEMORIA TOTAL
    memoria_livre_GB = memoria.available / (1024**3) # Memória livre em GB, Captura memoria livre
    memoria_usada_GB = memoria_total_GB - memoria_livre_GB # Faz a conta: total - livre = usada (quanto de memória está ocupada).
    memoria_formatada_em_uso = f'{memoria_usada_GB:.2f}' # Formata a memoria usada em gb com 2 casas decimais

# DADOS DO DISCO

    disco_objeto = p.disk_usage('/')  # Captura o uso do disco da partição raiz '/'
    disco_percent =  p.disk_usage('/').percent # Captura a porcentagem de uso total do disco (quanto está ocupado)
    disco_livre_bytes = disco_objeto.free # Espaço livre em bytes
    disco_livre_gb = disco_livre_bytes / (1024**3) # Espaço livre em GB converte de bytes para GB
    porcentagem_livre = disco_objeto.free / disco_objeto.total * 100 # Porcentagem de espaço livre do disco
    disco_usado_gb = (disco_objeto.total - disco_livre_bytes) / (1024**3) # Faz a conta: total - livre = usado e converte para GB.
    disco_usado_formatado = f'{disco_usado_gb:.2f}'

    
    porcentagem = p.cpu_percent(interval=1, percpu=False)
    dono_maquina = platform.node()

    # Exibe todos os dados
    print(f"""
    ╔══════════════════════════════════════════════════╗
                ✅ Dados Inseridos no banco de dados!
    ╚══════════════════════════════════════════════════╝
            
    👤 Dono da máquina
    Hostname: {dono_maquina}

    ⚙️  CPU
    ➤ Porcentagem de uso: {porcentagem}%


    🧠 Memória RAM
    ➤ GB Livre: {memoria_GB_free:.2f} GB
    ➤ GB em Uso: {memoria_formatada_em_uso} GB

    💾 Disco
    ➤ Percentual de uso: {disco_percent:.1f}%
    ➤ GB Livre: {disco_livre_gb:.2f} GB
    ➤ GB em Uso: {disco_usado_formatado} GB

    ═══════════════════════════════════════════════════
    """)


    inserir_porcentagem_cpu(porcentagem, dono_maquina)
    inserir_dados_memoria(memoria_GB_free, memoria_usada_GB, dono_maquina)
    inserir_dados_disco(disco_percent, disco_livre_gb, disco_usado_formatado, dono_maquina)

    time.sleep(5)