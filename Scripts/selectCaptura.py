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


def selecionar_dados(tipo):
    try:
        db = connect(**config)
        if db.is_connected():
            with db.cursor() as cursor:
                if tipo == "cpu":
                    query = "SELECT * FROM vw_cpu;"
                    headers = ["Usuário", "Empresa", "Máquina", "Sistema", "Componente", "CPU %", "Data/Hora", "Hostname"]
                elif tipo == "memoria":
                    query = "SELECT * FROM vw_memoria_ram;"
                    headers = ["Usuário", "Empresa", "Máquina", "Sistema", "Componente", "Memória Livre", "Memória em Uso", "Data/Hora", "Hostname"]
                elif tipo == "disco":
                    query = "SELECT * FROM vw_disco_rigido;"
                    headers = ["Usuário", "Empresa", "Máquina", "Sistema", "Componente", "GB Livre", "GB em Uso", "% Uso", "Data/Hora", "Hostname"]
                else:
                    return [], []  # se passar um tipo errado

                cursor.execute(query)
                resultado = cursor.fetchall()
            db.close()
            return resultado, headers
    except Error as e:
        print("Erro ao conectar no MySQL:", e)
        return [], []

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
        resultado, headers = selecionar_dados("cpu")
        if resultado:
            print(tabulate(resultado, headers=headers, tablefmt="fancy_grid"))
        else:
            print("Nenhum dado encontrado.")

    elif decisao == 2:
        resultado, headers = selecionar_dados("memoria")
        if resultado:
            print(tabulate(resultado, headers=headers, tablefmt="fancy_grid"))
        else:
            print("Nenhum dado encontrado.")

    elif decisao == 3:
        resultado, headers = selecionar_dados("disco")
        if resultado:
            print(tabulate(resultado, headers=headers, tablefmt="fancy_grid"))
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
