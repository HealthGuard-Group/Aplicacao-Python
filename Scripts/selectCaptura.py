import psutil as p
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os
from tabulate import tabulate


load_dotenv()

config = {
    'user': os.getenv("USER"),
    'password': os.getenv("PASSWORD"),
    'host': os.getenv("HOST"),
    'database': os.getenv("DATABASE")
}

# Função para selecionar porcentagem de CPU
def selecionar_porcentagem_cpu():
    try:
        db = connect(**config)
        if db.is_connected():
            print('Connected to MySQL server version -', db.server_info)
            with db.cursor() as cursor:
                query = """ 
               select * from vw_cpu; """
                cursor.execute(query)
                resultado = cursor.fetchall()
            cursor.close()
            db.close()
            return resultado
    except Error as e:
        print('Error to connect with MySQL -', e)
        return []

# Função para selecionar memória
def selecionar_memoria():
    try:
        db = connect(**config)
        if db.is_connected():
            with db.cursor() as cursor:
                query = """
                	select * from vw_memoria_ram;"""
                cursor.execute(query)
                resultado = cursor.fetchall()
            cursor.close()
            db.close()
            return resultado
    except Error as e:
        print('Error to connect with MySQL -', e)
        return []

# Função para selecionar disco
def selecionar_disco():
    try:
        db = connect(**config)
        if db.is_connected():
            with db.cursor() as cursor:
                query = """select * from vw_disco_rigido;"""
                cursor.execute(query)
                resultado = cursor.fetchall()
            cursor.close()
            db.close()
            return resultado
    except Error as e:
        print('Error to connect with MySQL -', e)
        return []


resultadocpu = selecionar_porcentagem_cpu()
resultadomemoria = selecionar_memoria()
resultadodisco = selecionar_disco()




loop = True
while loop:
    decisao = int(input("""
 ╔════════════════════════════════════════════╗
║              🖥  MENU DO CLIENTE            ║
╠════════════════════════════════════════════╣
║ 1  Visualizar Porcentagem do uso da CPU    ║
║ 2  Visualizar Dados de Memória             ║
║ 3  Visualizar Dados do Disco               ║
║ 4  Sair                                    ║
╚════════════════════════════════════════════╝
      """))
   
    if decisao == 1:
        if resultadocpu:
            headers = ["Usuário", "Empresa", "Máquina", "Sistema", "Componente", "CPU %", "Data/Hora", "Hostname"]
            print(tabulate(resultadocpu, headers=headers, tablefmt="fancy_grid"))
        else:
            print("Nenhum dado encontrado.")

    elif decisao == 2:
        if resultadomemoria:
            headers = ["Usuário", "Empresa", "Máquina", "Sistema", "Componente", "Memória Livre", "Memória em Uso", "Data/Hora", "Hostname"]
            print(tabulate(resultadomemoria, headers=headers, tablefmt="fancy_grid"))
        else:
            print("Nenhum dado encontrado.")

    elif decisao == 3:
        if resultadodisco:
            headers = ["Usuário", "Empresa", "Máquina", "Sistema", "Componente", "GB Livre", "GB em Uso", "% Uso", "Data/Hora", "Hostname"]
            print(tabulate(resultadodisco, headers=headers, tablefmt="fancy_grid"))
        else:
            print("Nenhum dado encontrado.")

    elif decisao == 4:
        loop = False
        print("""
╔════════════════════════════════════════════╗
║           👋 ENCERRANDO O SISTEMA          ║
╠════════════════════════════════════════════╣
║ Obrigado por usar o HealthGuard!           ║
║ Tenha um ótimo dia! 🌟                     ║
╚════════════════════════════════════════════╝
""")
    else:
        print("Opção inválida, tente novamente.")

