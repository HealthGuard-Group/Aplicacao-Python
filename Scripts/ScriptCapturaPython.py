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
            id_dac = verificao_dac[1]
            id_monitoramentos_selecionados = acaoComumBanco(f"SELECT fkMedicoesDisponiveis FROM healthguard.MedicoesSelecionadas WHERE fkDac = {id_dac}")
            lista_fks = [id_unidade_de_atendimento,id_dac,id_monitoramentos_selecionados]
            return lista_fks
        else:
            id_unidade_de_atendimento = validacao_dac[0][1]
            id_dac = acaoComumBanco(f"SELECT idDac FROM Dac WHERE codigoValidacao = '{codigo_cofiguracao}'")
            id_dac = id_dac[0][0]
            id_monitoramentos_selecionados = acaoComumBanco(f"SELECT fkMedicoesDisponiveis FROM healthguard.MedicoesSelecionadas WHERE fkDac = {id_dac}")
            lista_fks = [id_unidade_de_atendimento,id_dac,id_monitoramentos_selecionados]
            return lista_fks
            
    else:
        verificao_dac = configurarDac()
        id_unidade_de_atendimento = verificao_dac[0][1]
        id_dac = verificao_dac[1]
        id_monitoramentos_selecionados = acaoComumBanco(f"SELECT fkMedicoesDisponiveis FROM healthguard.MedicoesSelecionadas WHERE fkDac = {id_dac}")
        lista_fks = [id_unidade_de_atendimento,id_dac,id_monitoramentos_selecionados]
        return lista_fks

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
    codigo_configuracao = input()
    if len(codigo_configuracao) != 20:
        print("Código Invalído")
        t.sleep(2)
        configurarDac()
    else:
        validacao_cofiguracao = acaoComumBanco(f"SELECT idCodigoConfiguracao,fkUnidadeDeAtendimento,codigo FROM healthguard.CodigoConfiguracaoMaquina WHERE codigo = '{codigo_configuracao}' AND statusCodigoConfiguracaoMaquina = 'Pendente'")
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
            id_dac = acaoComumBanco(f"SELECT idDac FROM Dac WHERE codigoValidacao = '{codigo_configuracao}'")
            acaoComumBanco(f"UPDATE healthguard.CodigoConfiguracao SET statusCodigoConfiguracaoMaquina = 'Aceito' WHERE idCodigoConfiguracao = {id_codigo_configuracao}")
            acaoComumBanco(f"UPDATE healthguard.Dac SET codigoValidacao = sha2('{codigo_gerado}',256) WHERE codigoValidacao = '{codigo_configuracao}'")
            codigo_configuracao_criptografado = acaoComumBanco(f"SELECT codigoValidacao FROM Dac WHERE idDac = {id_dac[0][0]}")
            validacao_cofiguracao.append(id_dac[0][0])
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

def monitoramentosParaBinario(id_monitoramento_selecionados):
    global id_dac
    # Transoformando monitoramento_selecionados em binário
    numero_monitoramento_disponiveis = acaoComumBanco("SELECT COUNT(nomeDaMedicao) FROM healthguard.MedicoesDisponiveis")
    numero_monitoramento_disponiveis = numero_monitoramento_disponiveis[0][0]
    componentes = [item[0] for item in id_monitoramento_selecionados]
    binario_idMedicoesSelecionadas = []
    binario = []
    for i in range(numero_monitoramento_disponiveis):
        binario.append(0)
    contador = 0;
    while contador < len(componentes):
        binario[componentes[contador]-1] = 1
        contador += 1
    if binario[0] == 1:
        global habilita_usoCPU
        habilita_usoCPU = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 1 AND fkDac = {id_dac}")
        print(id_medicoes_selecionadas)
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    if binario[1] == 1:
        global habilita_freqCPU
        habilita_freqCPU = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 2 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    if binario[2] == 1:
        global habilita_Mem_used
        habilita_Mem_used = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 3 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    if binario[3] == 1:
        global habilita_Mem_total
        habilita_Mem_total = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 4 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    if binario[4] == 1:
        global habilita_usoDisk
        habilita_usoDisk = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 5 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    if binario[5] == 1:
        global habilita_LivreDisk
        habilita_LivreDisk = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 6 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    if binario[6] == 1:
        global habilita_Disco_total
        habilita_Disco_total = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 7 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    return binario_idMedicoesSelecionadas

def monitoramentoHardware(id_unidade_atendimento,id_dac,id_monitoramentos_selecionados):
    query = "INSERT INTO healthguard.leitura (fkUnidadeDeAtendimento,fkDac,fkMedicoesDisponiveis,fkMedicoesSelecionadas,medidaCapturada) VALUES"
    if habilita_usoCPU == True:
        usoCPU = p.cpu_percent(interval=1, percpu=False)
        query += f"({id_unidade_atendimento},{id_dac},1,{id_monitoramentos_selecionados[0]},'{usoCPU}'),"
    if habilita_freqCPU == True:
        freqCPU = round((p.cpu_freq(percpu=False).current)/1000,2)
        query += f"({id_unidade_atendimento},{id_dac},2,{id_monitoramentos_selecionados[1]},'{freqCPU}'),"
    if habilita_Mem_used == True:
        Mem_used = p.virtual_memory().percent
        query += f"({id_unidade_atendimento},{id_dac},3,{id_monitoramentos_selecionados[2]},'{Mem_used}'),"
    if habilita_Mem_total == True:
        Mem_total = round(p.virtual_memory().total / (1024 ** 3),2)
        query += f"({id_unidade_atendimento},{id_dac},4,{id_monitoramentos_selecionados[3]},'{Mem_total}'),"
    if habilita_usoDisk == True:
        usoDisk = round(p.disk_usage("C:/").used/ (1024**3),2)
        query += f"({id_unidade_atendimento},{id_dac},5,{id_monitoramentos_selecionados[4]},'{usoDisk}'),"
    if habilita_LivreDisk == True:
        LivreDisk = round(p.disk_usage("C:/").free/ (1024**3),2)
        query += f"({id_unidade_atendimento},{id_dac},6,{id_monitoramentos_selecionados[5]},'{LivreDisk}'),"
    if habilita_Disco_total == True:
        usoDisk = round(p.disk_usage("C:/").used/ (1024**3),2)
        LivreDisk = round(p.disk_usage("C:/").free/ (1024**3),2)
        Disco_total = usoDisk + LivreDisk
        query += f"({id_unidade_atendimento},{id_dac},7,{id_monitoramentos_selecionados[6]},'{Disco_total}'),"
    if query.endswith(","):
        query = query[:-1] + ";"
    else:
        query = ""
    if query != "":
        acaoComumBanco(query)
    if habilita_usoCPU == True:
        t.sleep(9)
    else:
        t.sleep(10)

limparTela()

#  Declaração dos Booleanos para captura
habilita_usoCPU = False
habilita_freqCPU = False
habilita_Mem_used = False
habilita_Mem_total = False
habilita_usoDisk = False
habilita_LivreDisk = False
habilita_Disco_total = False
# 




id_unidade_atendimento = 0
id_dac = 0
id_monitoramentos_selecionados = 0


contador = (4 * 60 * 60) /10
print(contador)
while True:
    if contador == (4 * 60 * 60) / 10:
        fks = validarTxt()
        id_unidade_atendimento = fks[0]
        id_dac = fks[1]
        id_monitoramentos_selecionados = fks[2]
        print("Id Unidade Atendimento", id_unidade_atendimento)
        print("Id Dac:", id_dac)
        print("Id Monitoramento selecionados:", id_monitoramentos_selecionados)
        acaoComumBanco(f"UPDATE healthguard.Dac SET statusDac = 'Ativo' WHERE idDac = {id_dac}")
        id_monitoramentos_selecionados = monitoramentosParaBinario(id_monitoramentos_selecionados)
        contador = 0
        limparTela()
    monitoramentoHardware(id_unidade_atendimento,id_dac,id_monitoramentos_selecionados)
    contador += 1
    
