import psutil as p
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os
import platform

load_dotenv()

config = {
  'user': os.getenv("USER"),
  'password': os.getenv("PASSWORD"),
  'host': os.getenv("HOST"),
  'database': os.getenv("DATABASE")
}

def selecionar_porcentagem_cpu():
    try:
        db = connect(**config)
        if db.is_connected():
            print('Connected to MySQL server version -', db.server_info)
            
            with db.cursor() as cursor:
                query = """SELECT 
u.nome              AS Usuario,
e.razaoSocial       AS Empresa,
m.marca             AS Maquina,
m.sistemaOperacional AS SistemaOperacional,
c.nome   AS Componente,
CONCAT(cap.porcentagemDeUso, "%")          AS "Porcentagem EM USO",
cap.dtCaptura       AS DataCaptura,
cap.hostname
FROM Usuario u
JOIN Empresa e     ON u.fkEmpresa = e.idEmpresa
JOIN Lote l        ON e.idEmpresa = l.fkEmpresa
JOIN Maquina m     ON l.idLote = m.fkLote
JOIN Componente c  ON m.idMaquina = c.fkMaquina
LEFT JOIN Captura cap   ON c.idComponente = cap.fkComponente
where c.nome = "Processador";"""
                cursor.execute(query)
                resultado = cursor.fetchall() 
                
            cursor.close()
            db.close()
            return resultado
    
    except Error as e:
        print('Error to connect with MySQL -', e) 
       
        
        
resultadocpu = selecionar_porcentagem_cpu() 

def selecionar_memoria():
    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.server_info
            print()
            
            with db.cursor() as cursor:
    
                query = """SELECT 
u.nome              AS Usuario,
e.razaoSocial       AS Empresa,
m.marca             AS Maquina,
m.sistemaOperacional AS SistemaOperacional,
c.nome   AS Componente,
CONCAT(ROUND(cap.gbEmUso, 1), " GB")          AS "GigaBytes EM USO",
CONCAT(ROUND(gbLivre, 2), " GB" )       AS "GigaBytes Livre",
cap.dtCaptura       AS DataCaptura,
cap.hostname
FROM Usuario u
JOIN Empresa e     ON u.fkEmpresa = e.idEmpresa
JOIN Lote l        ON e.idEmpresa = l.fkEmpresa
JOIN Maquina m     ON l.idLote = m.fkLote
JOIN Componente c  ON m.idMaquina = c.fkMaquina
LEFT JOIN Captura cap   ON c.idComponente = cap.fkComponente
where c.nome = "Memoria RAM";;"""


                cursor.execute(query)
                resultado = cursor.fetchall() 
                
            cursor.close()
            db.close()
            return resultado
    
    except Error as e:
        print('Error to connect with MySQL -', e) 
        
        
resultadomemoria = selecionar_memoria()

def selecionar_disco():
    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.server_info
            print()
            
            with db.cursor() as cursor:
    
                query = """SELECT 
u.nome              AS Usuario,
e.razaoSocial       AS Empresa,
m.marca             AS Maquina,
m.sistemaOperacional AS SistemaOperacional,
c.nome   AS Componente,
CONCAT(cap.porcentagemDeUso, "%")          AS "Porcentagem EM USO",
CONCAT(ROUND(cap.gbEmUso, 1), " GB")          AS "GigaBytes EM USO",
CONCAT(ROUND(cap.gbLivre, 2), " GB" )       AS "GigaBytes Livre",
cap.dtCaptura       AS DataCaptura,
cap.hostname12
FROM Usuario u
JOIN Empresa e     ON u.fkEmpresa = e.idEmpresa
JOIN Lote l        ON e.idEmpresa = l.fkEmpresa
JOIN Maquina m     ON l.idLote = m.fkLote
JOIN Componente c  ON m.idMaquina = c.fkMaquina
LEFT JOIN Captura cap   ON c.idComponente = cap.fkComponente
where c.nome = "Disco Rígido";
;;"""


                cursor.execute(query)
                resultado = cursor.fetchall() 
                
            cursor.close()
            db.close()
            return resultado
    
    except Error as e:
        print('Error to connect with MySQL -', e) 
        
        
resultadodisco = selecionar_disco()

loop = True
tamanho_vetormemoria = len(resultadomemoria)
tamanho_vetorcpu = len(resultadomemoria)
tamanho_vetordisco = len(resultadodisco)

while loop == True:

    decisao = int(input("""
 ╔════════════════════════════════════════════╗
║              🖥  MENU DO CLIENTE            ║
╠════════════════════════════════════════════╣
║ ⿡  Visualizar Porcentagem do uso da CPU    ║
║ ⿢  Visualizar Dados de Memória             ║
║ ⿣  Visualizar Dados do Disco               ║
║ ⿠  Sair                                    ║
╚════════════════════════════════════════════╝
      """))

    if decisao == 1:
        for i in range(tamanho_vetorcpu):
           usuario, empresa, maquina, so, componente, cpu, hora, hostname = resultadocpu[i]
           print(f"""        
============================================================
                📊 RELATÓRIO DA CPU
 ============================================================
 👤 Usuário:      {usuario}
 👤 Hostname:     {hostname}
 🏢 Empresa:      {empresa}
 💻 Máquina:      {maquina}
 🖥  Sistema:      {so}
 🔧 Componente:   {componente}

 📈 Percentual de uso CPU: {cpu}

 🕒 Data/Hora da Captura: {hora}
============================================================
""")
    if decisao == 2:
        for i in range(tamanho_vetormemoria):
            usuario, empresa, maquina, so, componente, memoria_livre, memoria_em_uso, hora,  hostname = resultadomemoria[i]
            print(f"""        
 ============================================================
                📊 RELATÓRIO DA MEMÓRIA
 ============================================================
 👤 Usuário:      {usuario}
 👤 Hostname:     {hostname}
 🏢 Empresa:      {empresa}
 💻 Máquina:      {maquina}
 🖥  Sistema:      {so}
 🔧 Componente:   {componente}

 📂 GB livre da Memória RAM: {memoria_livre}
 💾 GB em uso da Memóra: {memoria_em_uso}

 🕒 Data/Hora da Captura: {hora}
============================================================
""") 
 
    if decisao == 3:
        for i in range(tamanho_vetordisco):
            usuario, empresa, maquina, so, componente, gblivre, gbuso, percent,  hora,  hostname = resultadodisco[i]
            print(f"""        
 ============================================================
                📊 RELATÓRIO DO DISCO
 ============================================================
 👤 Usuário:      {usuario}
 👤 Hostname:     {hostname}
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
    if decisao == 0:
        loop = False
        print("""
╔════════════════════════════════════════════╗
║           👋 ENCERRANDO O SISTEMA          ║
╠════════════════════════════════════════════╣
║ Obrigado por usar o HealthGuard!           ║
║ Tenha um ótimo dia! 🌟                     ║
╚════════════════════════════════════════════╝
""")
                    
