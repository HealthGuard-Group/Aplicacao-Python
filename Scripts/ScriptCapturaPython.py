import psutil as p
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os
import time as t

load_dotenv()

config = {
      'user': os.getenv("USER_DB"),
      'password': os.getenv("PASSWORD_DB"),
      'host': os.getenv("HOST_DB"),
      'database': os.getenv("DATABASE_DB")
    }
nome_arquivo = "configDAC.txt"

def limparTela():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def acaoComumBanco(query):
    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.server_info
            print('Connected to MySQL server version -', db_info)
            with db.cursor() as cursor:
                cursor.execute(query)
                resultado = cursor.fetchall() 
                db.commit()
                print(cursor.rowcount, "registro inserido")
            cursor.close()
            db.close()
            return resultado
    
    except Error as e:
        print('Error to connect with MySQL -', e)

def validarTxt():
    arquivo_existe = os.path.exists(nome_arquivo)
    if arquivo_existe:
        with open(nome_arquivo,'r', encoding='utf-8') as txt:
            codigo_cofiguracao = txt.read()
        validacao_dac = acaoComumBanco(f"SELECT idDac,fkUnidadeDeAtendimento FROM healthguard.Dac WHERE statusDac != 'Excluido' AND codigoValidacao = '{codigo_cofiguracao}' ")
        if validacao_dac == []:
            os.remove(nome_arquivo)
            verificao_dac = configurarDac()
            id_unidade_de_atendimento = verificao_dac[0][1]
            codigo_validacao = verificao_dac[0][2]
        else:
            id_codigo_configuracao = validacao_dac[0][0]
            id_unidade_de_atendimento = validacao_dac[0][1]
    else:
        verificao_dac = configurarDac()
        id_unidade_de_atendimento = verificao_dac[0][1]
        codigo_validacao = verificao_dac[0][2]

def configurarDac():
    limparTela()
    print(f"""
                     _ _   _       ___                     _ 
     /\  /\___  __ _| | |_| |__   / _ \_   _  __ _ _ __ __| |
    / /_/ / _ \/ _` | | __| '_ \ / /_\/ | | |/ _` | '__/  _`|
   / __  /  __/ (_| | | |_| | | / /_\\ | |_| | (_| | |  | (_||
   \/ /_/ \___|\__,_|_|\__|_| |_\____/ \__,_|\__,_|_|  \__,_|
                                                          

__________________________________________________________________
Para configurar sua maquína insira o código de configuração do DAC:""")
    codigoconfiguracao = input()
    if len(codigoconfiguracao) != 20:
        print("Código Invalído")
        t.sleep(2)
        configurarDac()
    else:
        print("Comecei o select")
        validacao_cofiguracao = acaoComumBanco(f"SELECT idCodigoConfiguracao,fkUnidadeDeAtendimento,codigo FROM healthguard.CodigoConfiguracao WHERE codigo = '{codigoconfiguracao}' AND statusCodigo = 'Pedente'")
        if validacao_cofiguracao == []:
            print("Código Invalído")
            t.sleep(2)
            configurarDac()
        else:
            mensagem = "Código Valído. Iniciando as configurações "
            for a in range(4):
                limparTela()
                print(mensagem)
                mensagem += "."
                t.sleep(1)
            id_codigo_configuracao = validacao_cofiguracao[0][0]
            with open(nome_arquivo,'w', encoding='utf-8') as txt:
                txt.write(codigoconfiguracao)
            acaoComumBanco(f"UPDATE healthguard.CodigoConfiguracao SET statusCodigo = 'Aceito' WHERE idCodigoConfiguracao = {id_codigo_configuracao}")
            return validacao_cofiguracao
    
limparTela()
validarTxt()
