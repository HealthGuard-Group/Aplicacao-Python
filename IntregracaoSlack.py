import os
from slack_sdk import WebClient
from mysql.connector import connect, Error
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

load_dotenv()

config = {
      'user': os.getenv("USER_DB"),
      'password': os.getenv("PASSWORD_DB"),
      'host': os.getenv("HOST_DB"),
      'database': os.getenv("DATABASE_DB"),
    }

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
            limparTela()
            return resultado
    
    except Error as e:
        print('Error to connect with MySQL -', e)

token_slack = ""

def configSlack(idUnidade):
    global token_slack
    token_slack = acaoComumBanco(f"SELECT tokenSlack,canalSlack FROM UnidadeDeAtendimento WHERE idUnidadeDeAtendimento = {idUnidade}")
    if token_slack[0][0] == None or len(token_slack) == 0 or token_slack[0][1] == None :
        return True
    else:
        return False

def enviandoMensagem(tipoAlerta,monitoramento,valorMedida,limite,idMaquina,idUnidade):
    global token_slack
    if configSlack(idUnidade):
        print("""
-------------------------------------------------------
|           Código do Slack não foi Configurado       |
|           Fazer insert ou update no Banco           |
-------------------------------------------------------
""")
        return
    print(token_slack)
    client = WebClient(token=token_slack[0][0])
    nome_canal = token_slack[0][1]
    nomeMaquina = acaoComumBanco(f"SELECT nomeIdentificacao FROM Dac WHERE idDac = {idMaquina}")
    nomeMaquina = nomeMaquina[0][0]
    nomeMonitoramento = acaoComumBanco(f"SELECT nomeDaMedicao FROM MedicoesDisponiveis WHERE idMedicoesDisponiveis = {monitoramento}")
    nomeMonitoramento = nomeMonitoramento[0][0]
    recurso = ""
    print(type(monitoramento))
    if monitoramento == 1:
        recurso = "CPU"
    if monitoramento == 6:
        recurso = "RAM"
    if monitoramento == 10:
        recurso = "Disco"
    print("Tentando mandar mensagem no canal ", nome_canal)
    mensagem_formatacao = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"❗{tipoAlerta.upper()}: {nomeMonitoramento}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"O recurso *{recurso}* atingiu *{valorMedida}%* na máquina '{nomeMaquina}'."
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Máquina:*\n{nomeMaquina}"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Valor detectado:*\n{valorMedida}%"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Limite:*\n{limite}%"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Tipo:*\n *{tipoAlerta}*"
                    }
                ]
            },
            {
                "type": "divider"
            }
        ]
    try:
        client.chat_postMessage(channel=nome_canal,text="Olá estou fazendo um teste, será que vai dar certo",blocks=mensagem_formatacao)
        print("Mensagem foi enviada com sucesso")
    except SlackApiError as erro:
        print("Ops ouve um erro, segue a seguir o código do erro:",erro.response['error'])
    