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

def inserir_porcentagem_cpu(porcentagem, donoMaquina):
    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.server_info

            with db.cursor() as cursor:
                cursor.execute("SELECT idComponente FROM Componente WHERE nome LIKE 'Processador';")
                resultado_index = cursor.fetchall()

                index_cpu = resultado_index[0][0]

                querySelect = "SELECT idNucleo FROM nucleo;"
                cursor.execute(querySelect)
                resultado_select = cursor.fetchall()
    
                for ax, i in enumerate(resultado_select):
                    fk_nucleo = i[0]
                    percent = porcentagem[ax]
                    query = "INSERT INTO healthguard.captura (fkComponente, fkNucleo, porcentagemDeUso, hostname, dtCaptura) VALUES (%s, %s, %s, %s, %s)"
                    value = (index_cpu, fk_nucleo, percent, dono_maquina, datetime.datetime.now())
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
                cursor.execute("SELECT idComponente FROM Componente WHERE nome LIKE 'Memória RAM';")
                resultado_index = cursor.fetchall()

                id_memoria = resultado_index[0][0]

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
                cursor.execute("SELECT idComponente FROM Componente WHERE nome LIKE 'Disco Rígido';")
                resultado_id = cursor.fetchall()

                id_disco = resultado_id[0][0]
                query = "INSERT INTO healthguard.captura (fkComponente, gbLivre, gbEmUso, porcentagemDeUso, hostname,dtCaptura) VALUES (%s, %s, %s, %s, %s, %s)"
                value = (id_disco,  disco_livre_gb, disco_usado_formatado, disco_percent, dono_maquina, datetime.datetime.now())
                cursor.execute(query, value)
                db.commit()
                print("")
            db.close()  
    except Error as e:
        print('Erro ao conectar com MySQL -', e)         


for i in range(30):
 
    dono_maquina = platform.node()

  

        
    memoria = p.virtual_memory() ## captura dados e métricas da memoria
    memoria_livre = memoria.available   ## memoria livre em bytes
    memoria_GB_free = memoria_livre / (1024**3)   ## memoria convertida pra GB
    memoria_formatada = f"{memoria_GB_free:.2f} GB" ## memoria formatada com 2 casas decimais
   
    memoria_total_GB = memoria.total / (1024**3) # Captura memoria TOTAL
    memoria_livre_GB = memoria.available / (1024**3) # Memória livre em GB, Captura memoria livre
    memoria_usada_GB = memoria_total_GB - memoria_livre_GB # faz oepração aritmetica para saber o GB EM USO
    memoria_formatada_em_uso = f'{memoria_usada_GB:.2f}'

    # Captura o uso do disco da partição raiz '/'
    disco_objeto = p.disk_usage('/')
    disco_percent =  p.disk_usage('/').percent

     
    disco_livre_bytes = disco_objeto.free # Espaço livre em bytes
    disco_livre_gb = disco_livre_bytes / (1024**3) # Espaço livre em GB
    porcentagem_livre = disco_objeto.free / disco_objeto.total * 100 # Porcentagem de espaço livre
    disco_usado_gb = (disco_objeto.total - disco_livre_bytes) / (1024**3) # disco usado captura disco usado

    disco_usado_formatado = f'{disco_usado_gb:.2f}'

    memoria = p.virtual_memory() ## captura dados e métricas da memoria
    memoria_livre = memoria.available   ## memoria livre em bytes
    memoria_GB_free = memoria_livre / (1024**3)   ## memoria convertida pra GB
    memoria_formatada = f"{memoria_GB_free:.2f} GB" ## memoria formatada com 2 casas decimais
    memoria_total_GB = memoria.total / (1024**3) # Captura memoria TOTAL
    memoria_livre_GB = memoria.available / (1024**3) # Memória livre em GB
    memoria_usada_GB = memoria_total_GB - memoria_livre_GB # GB em uso
    memoria_formatada_em_uso = f'{memoria_usada_GB:.2f}'

    # Captura o uso do disco da partição raiz '/'
    disco_objeto = p.disk_usage('/')
    disco_percent = disco_objeto.percent
    disco_livre_bytes = disco_objeto.free
    disco_livre_gb = disco_livre_bytes / (1024**3)
    disco_usado_gb = (disco_objeto.total - disco_livre_bytes) / (1024**3)
    disco_usado_formatado = f'{disco_usado_gb:.2f}'



   
    porcentagem = p.cpu_percent(interval=1, percpu=True)
    dono_maquina = platform.node()


   # Formata os núcleos da CPU de forma bonita
    texto_nucleos = "╔═════════════╦═════════╗\n"
    texto_nucleos += "║ Núcleo      ║ Uso     ║\n"
    texto_nucleos += "╠═════════════╬═════════╣\n"
    for idx, percent in enumerate(porcentagem, start=1):
        texto_nucleos += f"║ Núcleo {idx:<2}    ║ {percent:>5.1f}%   ║\n"
    texto_nucleos += "╚═════════════╩═════════╝"

    # Exibe todos os dados
    print(f"""
    ╔══════════════════════════════════════════════════╗
                ✅ Dados Inseridos no banco de dados!
    ╚══════════════════════════════════════════════════╝
            
    👤 Dono da máquina
    Hostname: {dono_maquina}

    💻 CPU
    ➤ Percentual de uso por núcleo:
    {texto_nucleos}

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