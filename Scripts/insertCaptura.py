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


while True:
 
 # HOSTNAME DA MAQUINA
    dono_maquina = platform.node()

# DADOS DA MEMORIA
  

    memoria = p.virtual_memory()  # Captura todas as métricas da memória
    memoria_total_GB = memoria.total / (1024**3)  # Memória total em GB
    memoria_GB_free = memoria.available / (1024**3)  # Memória livre em GB
    memoria_usada_GB = memoria_total_GB - memoria_GB_free  # Memória usada em GB
    memoria_formatada_em_uso = f'{memoria_usada_GB:.2f}'  # Formata em 2 casas decimais


# DADOS DO DISCO

    disco_objeto = p.disk_usage('/')  # Captura o uso do disco da partição raiz '/'
    disco_percent = disco_objeto.percent  # Porcentagem de uso do disco
    disco_livre_gb = disco_objeto.free / (1024**3)  # Espaço livre em GB
    disco_usado_gb = (disco_objeto.total - disco_objeto.free) / (1024**3)  # Espaço usado em GB
    disco_usado_formatado = f'{disco_usado_gb:.2f}'  # Formata em 2 casas decimais


# dados de cpu
    porcentagem = p.cpu_percent(interval=1, percpu=False)
    

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