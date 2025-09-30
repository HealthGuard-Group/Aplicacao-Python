import psutil as p
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os
import time as t
import random

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
            codigo_gerado = sorteadorTexto(20)
            id_dac = acaoComumBanco(f"SELECT idDac FROM Dac WHERE codigoValidacao = '{codigoconfiguracao}'")
            acaoComumBanco(f"UPDATE healthguard.CodigoConfiguracao SET statusCodigo = 'Aceito' WHERE idCodigoConfiguracao = {id_codigo_configuracao}")
            acaoComumBanco(f"UPDATE healthguard.Dac SET codigoValidacao = sha2('{codigo_gerado}',256) WHERE codigoValidacao = '{codigoconfiguracao}'")
            codigo_configuracao_criptografado = acaoComumBanco(f"SELECT codigoValidacao FROM Dac WHERE idDac = {id_dac[0][0]}")
            with open(nome_arquivo,'w', encoding='utf-8') as txt:
                txt.write(codigo_configuracao_criptografado[0][0])
            return validacao_cofiguracao
    
def sorteadorTexto(num_caracteres):
    texto_gerado = ""
    vetor_caracteres = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','1', '2', '3', '4', '5', '6', '7', '8', '9','0']
    for a in range(num_caracteres):
        pos_aleatoria = random.randint(0,len(vetor_caracteres) - 1)
        texto_gerado += vetor_caracteres[pos_aleatoria]
    return texto_gerado


limparTela()
validarTxt()
