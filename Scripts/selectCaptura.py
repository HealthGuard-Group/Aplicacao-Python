import psutil as p
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os


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
                SELECT 
                    u.nome AS Usuario,
                    c.nome AS Central,
                    m.marca AS Maquina,
                    m.sistemaOperacional AS SistemaOperacional,
                    co.nome AS Componente,
                    CONCAT(cap.porcentagemDeUso, "%") AS Percentual,
                    cap.dtCaptura AS DataCaptura
                FROM Usuario u
                JOIN CentralAtendimento c ON u.fkCentral = c.idCentral
                JOIN Maquina m ON m.fkCentral = c.idCentral
                JOIN Componente co ON m.idMaquina = co.fkMaquina
                LEFT JOIN Captura cap ON co.idComponente = cap.fkComponente
                WHERE co.nome = "Processador"
                ORDER BY cap.dtCaptura DESC;
                """
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
                SELECT 
                    u.nome AS Usuario,
                    c.nome AS Central,
                    m.marca AS Maquina,
                    m.sistemaOperacional AS SistemaOperacional,
                    co.nome AS Componente,
                    CONCAT(cap.gbLivre, " GB") AS MemoriaLivre,
                    CONCAT(cap.gbEmUso, " GB") AS MemoriaEmUso,
                    cap.dtCaptura AS DataCaptura
                FROM Usuario u
                JOIN CentralAtendimento c ON u.fkCentral = c.idCentral
                JOIN Maquina m ON m.fkCentral = c.idCentral
                JOIN Componente co ON m.idMaquina = co.fkMaquina
                LEFT JOIN Captura cap ON co.idComponente = cap.fkComponente
                WHERE co.nome = "Memória RAM"
                ORDER BY cap.dtCaptura DESC;
                """
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
                query = """
                SELECT 
                    u.nome AS Usuario,
                    c.nome AS Central,
                    m.marca AS Maquina,
                    m.sistemaOperacional AS SistemaOperacional,
                    c.nome AS Componente,
                    CONCAT(ROUND(cap.gbLivre,2), " GB") AS GBLivre,
                    CONCAT(ROUND(cap.gbEmUso,2), " GB") AS GBEmUso,
                    CONCAT(cap.porcentagemDeUso, "%") AS Percentual,
                    cap.dtCaptura AS DataCaptura
                FROM Usuario u
                JOIN CentralAtendimento c ON u.fkCentral = c.idCentral
                JOIN Maquina m ON m.fkCentral = c.idCentral
                JOIN Componente co ON m.idMaquina = co.fkMaquina
                LEFT JOIN Captura cap ON co.idComponente = cap.fkComponente
                WHERE co.nome = "Disco Rígido"
                ORDER BY cap.dtCaptura DESC;
                """
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


# Loop do menu
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
        for linha in resultadocpu:
            usuario, empresa, maquina, so, componente, cpupercent, hora = linha
            print(f"""
============================================================
                📊 RELATÓRIO DA CPU
============================================================
👤 Usuário:      {usuario}
🏢 Empresa:      {empresa}
💻 Máquina:      {maquina}
🖥  Sistema:      {so}
🔧 Componente:   {componente}

⚙️  Porcentagem de uso: {cpupercent}

🕒 Data/Hora da Captura: {hora}
============================================================
""")

    elif decisao == 2:
        for linha in resultadomemoria:
            usuario, empresa, maquina, so, componente, memoria_livre, memoria_em_uso, hora = linha
            print(f"""
============================================================
                📊 RELATÓRIO DA MEMÓRIA
============================================================
👤 Usuário:      {usuario}
🏢 Empresa:      {empresa}
💻 Máquina:      {maquina}
🖥  Sistema:      {so}
🔧 Componente:   {componente}

📂 GB livre da Memória RAM: {memoria_livre}
💾 GB em uso da Memória: {memoria_em_uso}

🕒 Data/Hora da Captura: {hora}
============================================================
""")

    elif decisao == 3:
        for linha in resultadodisco:
            usuario, empresa, maquina, so, componente, gblivre, gbuso, percent, hora = linha
            print(f"""
============================================================
                📊 RELATÓRIO DO DISCO
============================================================
👤 Usuário:      {usuario}
🏢 Empresa:      {empresa}
💻 Máquina:      {maquina}
🖥  Sistema:      {so}
🔧 Componente:   {componente}

📂 GB livre do disco: {gblivre}
💾 GB em uso do disco: {gbuso}
📈 Percentual em Uso: {percent}

🕒 Data/Hora da Captura: {hora}
============================================================
""")

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

