import psutil as p
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os
import datetime
import time
import platform
from tabulate import tabulate


load_dotenv()

config = {
      'user': os.getenv("USER"),
      'password': os.getenv("PASSWORD"),
      'host': os.getenv("HOST"),
      'database': os.getenv("DATABASE")
    }

def inserir_dados(porcentagem, dono_maquina, memoria_GB_free, memoria_usada_GB, disco_percent, disco_livre_gb, disco_usado_formatado,):
    index_cpu = 3
    index_mem = 1
    index_disco = 2
    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.server_info

            with db.cursor() as cursor:
                if index_cpu == 3:
                 query = "INSERT INTO healthguard.captura (fkComponente, porcentagemDeUso, hostname, dtCaptura) VALUES (%s, %s, %s, %s)"
                 value = (index_cpu, porcentagem, dono_maquina, datetime.datetime.now())
                elif index_mem == 1:
                 query = "INSERT INTO healthguard.captura (fkComponente, gbLivre, gbEmUso, hostname, dtCaptura) VALUES (%s, %s, %s, %s, %s)"
                 value = (index_mem, memoria_GB_free, memoria_usada_GB, dono_maquina, datetime.datetime.now())
                elif index_disco == 2:
                 query = "INSERT INTO healthguard.captura (fkComponente, gbLivre, gbEmUso, porcentagemDeUso, hostname,dtCaptura) VALUES (%s, %s, %s, %s, %s, %s)"
                 value = (index_disco,  disco_livre_gb, disco_usado_formatado, disco_percent, dono_maquina, datetime.datetime.now())
                cursor.execute(query, value)
                   
                db.commit()    
            db.close()
   
    except Error as e:
        print('Error to connect with MySQL -', e)

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


    

    captura = [
        ["Hostname", dono_maquina],
        ["CPU % (USO)", f"{porcentagem}%"],
        ["Memória Livre (GB)", f"{memoria_GB_free:.2f} GB"],
        ["Memória em Uso (GB)", f"{memoria_formatada_em_uso} GB"],
        ["Disco % (USO)", f"{disco_percent:.1f}%"],
        ["Disco Livre (GB)", f"{disco_livre_gb:.2f} GB"],
        ["Disco em Uso (GB)", f"{disco_usado_formatado} GB"]
    ]

    print("""
╔════════════════════════════════════════════╗
║                                            ║
║     ✅ DADOS INSERIDOS COM SUCESSO!        ║
║                                            ║
║   Os dados foram gravados no banco de      ║
║  forma segura e o sistema foi atualizado.  ║
╚════════════════════════════════════════════╝
""")


    print(tabulate(captura, headers=["Componente", "Valor"], tablefmt="fancy_grid"))
    
    inserir_dados(porcentagem, dono_maquina, memoria_GB_free, memoria_usada_GB, disco_percent, disco_livre_gb, disco_usado_formatado,)


    time.sleep(4)