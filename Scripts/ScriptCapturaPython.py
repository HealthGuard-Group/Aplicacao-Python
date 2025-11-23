import psutil as p
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os
import datetime
import time as t
import random
import json

load_dotenv()

config = {
      'user': os.getenv("USER_DB"),
      'password': os.getenv("PASSWORD_DB"),
      'host': os.getenv("HOST_DB"),
      'database': os.getenv("DATABASE_DB"),
    }
tokenSlack = os.getenv("TOKEN_SLACK")
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
        validacao_dac = acaoComumBanco(f"SELECT idDac,fkUnidadeDeAtendimento FROM Dac WHERE statusDac != 'Excluido' AND codigoValidacao = '{codigo_cofiguracao}' ")
        if validacao_dac == []:
            os.remove(nome_arquivo)
            verificao_dac = configurarDac()
            id_unidade_de_atendimento = verificao_dac[0][1]
            id_dac = verificao_dac[1]
            id_monitoramentos_selecionados = acaoComumBanco(f"SELECT fkMedicoesDisponiveis FROM MedicoesSelecionadas WHERE fkDac = {id_dac}")
            lista_fks = [id_unidade_de_atendimento,id_dac,id_monitoramentos_selecionados]
            return lista_fks
        else:
            id_unidade_de_atendimento = validacao_dac[0][1]
            id_dac = acaoComumBanco(f"SELECT idDac FROM Dac WHERE codigoValidacao = '{codigo_cofiguracao}'")
            id_dac = id_dac[0][0]
            id_monitoramentos_selecionados = acaoComumBanco(f"SELECT fkMedicoesDisponiveis FROM MedicoesSelecionadas WHERE fkDac = {id_dac}")
            lista_fks = [id_unidade_de_atendimento,id_dac,id_monitoramentos_selecionados]
            return lista_fks
            
    else:
        verificao_dac = configurarDac()
        id_unidade_de_atendimento = verificao_dac[0][1]
        id_dac = verificao_dac[1]
        id_monitoramentos_selecionados = acaoComumBanco(f"SELECT fkMedicoesDisponiveis FROM MedicoesSelecionadas WHERE fkDac = {id_dac}")
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
        validacao_cofiguracao = acaoComumBanco(f"SELECT idCodigoConfiguracao,fkUnidadeDeAtendimento,codigo FROM CodigoConfiguracaoMaquina WHERE codigo = '{codigo_configuracao}' AND statusCodigoConfiguracaoMaquina = 'Pendente'")
        print("Fiz o select recebi ", validacao_cofiguracao)
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
            print("Inicei o processo de configuração")
            id_codigo_configuracao = validacao_cofiguracao[0][0]
            codigo_gerado = sorteadorTexto(20)
            id_dac = acaoComumBanco(f"SELECT idDac FROM Dac WHERE codigoValidacao = '{codigo_configuracao}'")
            acaoComumBanco(f"UPDATE CodigoConfiguracaoMaquina SET statusCodigoConfiguracaoMaquina = 'Aceito' WHERE idCodigoConfiguracao = {id_codigo_configuracao}")
            acaoComumBanco(f"UPDATE Dac SET codigoValidacao = sha2('{codigo_gerado}',256) WHERE codigoValidacao = '{codigo_configuracao}'")
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
    numero_monitoramento_disponiveis = acaoComumBanco("SELECT COUNT(nomeDaMedicao) FROM MedicoesDisponiveis")
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
    print(binario)
    if binario[0] == 1:
        global habilita_usoCPU
        habilita_usoCPU = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 1 AND fkDac = {id_dac}")
        print(id_medicoes_selecionadas)
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    else:
        binario_idMedicoesSelecionadas.append(0)
    if binario[1] == 1:
        global habilita_processosAtivos
        habilita_processosAtivos = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 2 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    else:
        binario_idMedicoesSelecionadas.append(0)
    if binario[2] == 1:
        global habilita_quantidadeNucleos
        habilita_quantidadeNucleos = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 3 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    else:
        binario_idMedicoesSelecionadas.append(0)
    if binario[3] == 1:
        global habilita_threads
        habilita_threads = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 4 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    else:
        binario_idMedicoesSelecionadas.append(0)
    if binario[4] == 1:
        global habilita_frequenciaAtual
        habilita_frequenciaAtual = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 5 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    else:
        binario_idMedicoesSelecionadas.append(0)
    if binario[5] == 1:
        global habilita_Mem_used
        habilita_Mem_used = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 6 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    else:
        binario_idMedicoesSelecionadas.append(0)
    if binario[6] == 1:
        global habilita_MemoriaTotal
        habilita_MemoriaTotal = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 7 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    else:
        binario_idMedicoesSelecionadas.append(0)
    if binario[7] == 1:
        global habilita_MemoriaSwap_used
        habilita_MemoriaSwap_used = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 8 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    else:
        binario_idMedicoesSelecionadas.append(0)
    if binario[8] == 1:
        global habilita_MemoriaSwap_Total
        habilita_MemoriaSwap_Total = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 9 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    else:
        binario_idMedicoesSelecionadas.append(0)
    if binario[9] == 1:
        global habilita_usoDisco
        habilita_usoDisco = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 10 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    else:
        binario_idMedicoesSelecionadas.append(0)
    if binario[10] == 1:
        global habilita_rede
        habilita_rede = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 11 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    else:
        binario_idMedicoesSelecionadas.append(0)
    if binario[11] == 1:
        global habilita_frequencia_maxima
        habilita_frequencia_maxima = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 12 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    else:
        binario_idMedicoesSelecionadas.append(0)
    if binario[12] == 1:
        global habilita_tempo_atividade
        habilita_tempo_atividade = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 13 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    else:
        binario_idMedicoesSelecionadas.append(0)
    if binario[13] == 1:
        global habilita_espaco_livre_disco
        habilita_espaco_livre_disco = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 14 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    else:
        binario_idMedicoesSelecionadas.append(0)
    if binario[14] == 1:
        global habilita_iops
        habilita_iops = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 15 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    else:
        binario_idMedicoesSelecionadas.append(0)
    if binario[15] == 1:
        global habilita_particao_disco
        habilita_particao_disco = True
        id_medicoes_selecionadas = acaoComumBanco(f"SELECT idMedicoesSelecionadas FROM MedicoesSelecionadas WHERE fkMedicoesDisponiveis = 16 AND fkDac = {id_dac}")
        if id_monitoramento_selecionados == []:
            binario_idMedicoesSelecionadas.append(0)
        else:
            binario_idMedicoesSelecionadas.append(id_medicoes_selecionadas[0][0])
    else:
        binario_idMedicoesSelecionadas.append(0)
    print(binario_idMedicoesSelecionadas)
    return binario_idMedicoesSelecionadas

def conversorByteParaGb(byte):
    return round(byte / (1024**3),2)

def monitoramentoHardware(id_unidade_atendimento,id_dac,id_monitoramentos_selecionados):
    print(id_monitoramentos_selecionados)
    query = "INSERT INTO Leitura (fkUnidadeDeAtendimento,fkDac,fkMedicoesDisponiveis,fkMedicoesSelecionadas,medidaCapturada) VALUES"
    if habilita_usoCPU == True:
        usoCPU = p.cpu_percent(interval=1, percpu=False)
        query += f"({id_unidade_atendimento},{id_dac},1,{id_monitoramentos_selecionados[0]},'{usoCPU}'),"
    if habilita_Mem_used == True:
        Mem_used = p.virtual_memory().percent
        query += f"({id_unidade_atendimento},{id_dac},6,{id_monitoramentos_selecionados[5]},'{Mem_used}'),"
    if habilita_usoDisco == True:
        if os.name == 'nt':
            memoria_used = p.disk_usage("C:\\").percent
        else:
            memoria_used = p.disk_usage("/").percent
        query += f"({id_unidade_atendimento},{id_dac},10,{id_monitoramentos_selecionados[9]},'{memoria_used}'),"
    if habilita_processosAtivos == True:
        qtd_processo_ativos = len(p.pids())
        query += f"({id_unidade_atendimento},{id_dac},2,{id_monitoramentos_selecionados[1]},'{qtd_processo_ativos}'),"
    if habilita_quantidadeNucleos == True:
        qtd_nucleos = p.cpu_count(logical=False)
        query += f"({id_unidade_atendimento},{id_dac},3,{id_monitoramentos_selecionados[2]},'{qtd_nucleos}'),"
    if habilita_threads == True:
        qtd_threads = p.cpu_count(logical=True)
        query += f"({id_unidade_atendimento},{id_dac},4,{id_monitoramentos_selecionados[3]},'{qtd_threads}'),"
    if habilita_frequenciaAtual == True:
        frequencia_atual = p.cpu_freq().current
        query += f"({id_unidade_atendimento},{id_dac},5,{id_monitoramentos_selecionados[4]},'{frequencia_atual}'),"
    if habilita_frequencia_maxima == True:
        frequencia_maxima = p.cpu_freq().max
        query += f"({id_unidade_atendimento},{id_dac},12,{id_monitoramentos_selecionados[11]},'{frequencia_maxima}'),"
    if habilita_MemoriaTotal == True:
        memoria_total = round(conversorByteParaGb(p.virtual_memory().total),0)
        query += f"({id_unidade_atendimento},{id_dac},7,{id_monitoramentos_selecionados[6]},'{memoria_total}'),"
    if habilita_MemoriaSwap_used == True:
        memoria_swap_uso = p.swap_memory().percent
        query += f"({id_unidade_atendimento},{id_dac},8,{id_monitoramentos_selecionados[7]},'{memoria_swap_uso}'),"
    if habilita_MemoriaSwap_Total == True:
        memoria_swap_total = conversorByteParaGb(p.swap_memory().total)
        query += f"({id_unidade_atendimento},{id_dac},9,{id_monitoramentos_selecionados[8]},'{memoria_swap_total}'),"
    if habilita_tempo_atividade == True:
        tempo_atividade = datetime.datetime.now() - datetime.datetime.fromtimestamp(p.boot_time())
        total_segundos = int(tempo_atividade.total_seconds())
        horas = total_segundos // 3600
        minutos = (total_segundos % 3600) // 60
        segundos = total_segundos % 60
        tempo_atividade = f"{horas:02}:{minutos:02}:{segundos:02}"
        query += f"({id_unidade_atendimento},{id_dac},13,{id_monitoramentos_selecionados[12]},'{tempo_atividade}'),"
    if habilita_espaco_livre_disco == True:
        if os.name == 'nt':
            memoria_free = conversorByteParaGb(p.disk_usage("C:\\").free)
        else:
            memoria_free = conversorByteParaGb(p.disk_usage("/").free)
        query += f"({id_unidade_atendimento},{id_dac},14,{id_monitoramentos_selecionados[13]},'{memoria_free}'),"
    if habilita_iops == True:
        inicio_ciclo = t.time()
        io_inicial = p.disk_io_counters()
        t.sleep(1)
        io_final = p.disk_io_counters()
        tempo_real = t.time() - inicio_ciclo  
        iops = ((io_final.read_count - io_inicial.read_count) + (io_final.write_count - io_inicial.write_count)) / tempo_real
        query += f"({id_unidade_atendimento},{id_dac},15,{id_monitoramentos_selecionados[14]},'{iops}'),"
    if habilita_particao_disco == True:
        partitions = p.disk_partitions(all=False)
        particoes_json = {}
        for partition in partitions:
            try:
                part_usage = p.disk_usage(partition.mountpoint)
                if ':\\' in partition.mountpoint:
                    nome_particao = partition.mountpoint.split(':\\')[0]
                else:
                    nome_particao = partition.mountpoint.replace('/', '')
                    if nome_particao == '':
                        nome_particao = 'root'
                particoes_json[nome_particao] = {
                    'percentual': part_usage.percent,
                    'livre_gb': round(part_usage.free / (1024**3), 1),
                    'total_gb': round(part_usage.total / (1024**3), 1),
                    'montagem': partition.mountpoint
                }   
            except PermissionError:
                continue
        particoes_json_str = json.dumps(particoes_json, ensure_ascii=False)
        query += f"({id_unidade_atendimento},{id_dac},16,{id_monitoramentos_selecionados[15]},'{particoes_json_str}'),"
    if query.endswith(","):
        query = query[:-1] + ";"
    else:
        query = ""
    if query != "":
        acaoComumBanco(query)
    if habilita_usoCPU == True and habilita_iops == True:
        t.sleep(8)
    elif habilita_iops == True or habilita_usoCPU == True:
        t.sleep(9)
    else:
        t.sleep(10)

limparTela()

#  Declaração dos Booleanos para captura
habilita_usoCPU = False
habilita_processosAtivos = False
habilita_quantidadeNucleos = False
habilita_threads = False
habilita_frequenciaAtual = False
habilita_Mem_used = False
habilita_MemoriaTotal = False
habilita_MemoriaSwap_used = False
habilita_MemoriaSwap_Total = False
habilita_usoDisco = False
habilita_rede = False
habilita_frequencia_maxima = False
habilita_tempo_atividade = False
habilita_espaco_livre_disco = False
habilita_iops = False
habilita_particao_disco = False

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
        acaoComumBanco(f"UPDATE Dac SET statusDac = 'Ativo' WHERE idDac = {id_dac}")
        id_monitoramentos_selecionados = monitoramentosParaBinario(id_monitoramentos_selecionados)
        contador = 0
        limparTela()
    monitoramentoHardware(id_unidade_atendimento,id_dac,id_monitoramentos_selecionados)
    contador += 1
    
