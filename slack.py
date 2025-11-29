import os
import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from mysql.connector import connect, Error
from dotenv import load_dotenv
load_dotenv()

client = WebClient(token=os.environ['TOKEN_SLACK'])


try:
response = client.chat_postMessage(channel='#random', text="Hello world!")
assert response["message"]["text"] == "Hello world!"
except SlackApiError as e:
assert e.response["ok"] is False
assert e.response["error"]
print(f"Got an error: {e.response['error']}")
assert isinstance(e.response.status_code, int)
print(f"Received a response status_code: {e.response.status_code}")



DB_CONFIG = {
'user': os.getenv("USER_DB"),
'password': os.getenv("PASSWORD_DB"),
'host': os.getenv("HOST_DB"),
'database': os.getenv("DATABASE_DB")
}



slack_client = WebClient(token=os.environ['TOKEN_SLACK'])


def executar_query_fetch(query, params=None):
try:
db = connect(**DB_CONFIG)
if db.is_connected():
with db.cursor() as cursor:
cursor.execute(query, params or ())
resultado = cursor.fetchall()
db.close()
return resultado
except Error as e:
print("[NOTIFICADOR] Erro ao conectar no banco:", e)
return None



def procurar_id_canal_slack(idUnidadeDeAtendimento: int):
"""
Retorna o ID_CANAL_SLACK para a empresa que contém a máquina (idMaquina).
"""
if idUnidadeDeAtendimento is None:
return None

q_empresa = """
SELECT u.idUnidadeDeAtendimento
FROM UnidadeDeAtendimento AS u
JOIN Dac AS d ON u.idUnidadeDeAtendimento = m.fkUnidadeDeAtendimento
WHERE m.idMaquina = %s;
"""
res = executar_query_fetch(q_empresa, (int(idDAC),))
if not res:
return None
idDAC = res[0][0]

q_slack = """
SELECT idSlack
FROM UnidadeDeAtendimento
WHERE idUnidadeDeAtendimento = %s;
"""
res2 = executar_query_fetch(q_slack, (int(idUnidadeDeAtendimento),))
if not res2:
return None
return res2[0][0]


ALERTA_IMAGE_LOCAL_PATH = "/mnt/data/2E971AA5-0CD8-450C-BC41-EBCB93AD9CA5.jpeg"

def formatar_mensagem(idDAC, titulo, subtitulo, nomeIdentificacao, nomeDaMedicao, medidaCapturada):
blocks = [
{"type":"header", "text":{"type":"plain_text", "text": titulo}},
{"type":"section", "text":{"type":"mrkdwn", "text": subtitulo}},
{"type":"divider"},
{
"type":"section",
"fields":[
{"type":"mrkdwn","text":f"*Máquina:*\n{nomeIdentificacao}"},
{"type":"mrkdwn","text":f"*ID:*\n{idDAC}"},
]
},
{"type":"divider"},
{
"type":"section",
"fields":[
{"type":"mrkdwn","text":f"*CPU (núcleos):*\n{nomeDaMedicao.get('CPU','-')}"},
{"type":"mrkdwn","text":f"*RAM (GB):*\n{nomeDaMedicao.get('RAM','-')}"},
{"type":"mrkdwn","text":f"*DISCO (GB):*\n{nomeDaMedicao.get('DISCO','-')}"}
]
},
{"type":"divider"},
{
"type":"section",
"fields":[
{"type":"mrkdwn","text":f"*Valor detectado:*\n{medidaCapturada.get('valor','-')}"},
{"type":"mrkdwn","text":f"*Limite:*\n{medidaCapturada.get('limite','-')}"},
{"type":"mrkdwn","text":f"*Tipo:*\n{medidaCapturada.get('tipo','-')}"}
]
},
{"type":"divider"},
]


if os.path.exists(ALERTA_IMAGE_LOCAL_PATH):
blocks.append({
"type": "image",
"image_url": ALERTA_IMAGE_LOCAL_PATH,
"alt_text": "alerta_imagem"
})

return blocks




def notificar(idDAC, titulo, subtitulo, nomeIdentificacao, nomeDaMedicao, medidaCapturada, limite, tipo_alerta):
"""
Monta payload e envia a notificação para o canal obtido no banco.
"""
if not slack_client:
print("[NOTIFICADOR] Bot Slack não inicializado. Ignorando notificação.")
return

canal = "C09TWKNDXGV"
if not canal:
print(f"[NOTIFICADOR] Canal Slack não encontrado para idMaquina={idDAC}.")
return

dados_medicao = {"valor": medidaCapturada, "limite": limite, "tipo": tipo_alerta}
blocks_payload = formatar_mensagem(idDAC, titulo, subtitulo, nomeIdentificacao, nomeDaMedicao, dados_medicao)

try:
slack_client.chat_postMessage(
channel=canal,
text=subtitulo,
blocks=blocks_payload
)
print(f"[NOTIFICADOR] Notificação enviada para canal {canal}.")
except SlackApiError as e:
print(f"[NOTIFICADOR] Erro SlackApi: {e.response.get('error', str(e))}")
except Exception as e:
print(f"[NOTIFICADOR] Erro inesperado ao enviar notificação: {e}")

