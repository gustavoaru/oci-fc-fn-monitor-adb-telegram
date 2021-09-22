#
# Notifica os funcionarios de plantao de acordo
# usando um bot do telegram
#
# Gustavo Costa
# gustavo.aru@gmail.com
# 2021-04-19
#

import urllib.request
import json
import sys
import base64
import telegram
import io



def enviaMensagem(data, descricao, mensagem, telegram_token):
    # Use the json module to load the string data into a dictionary
    theJSON = json.loads(data)
    j = 0
    try:
        for i in theJSON['items']:
            apelido = i['apelido']
            id_telegram = i['id_telegram']
            print('INFO: Enviando mensagem para ' + apelido + ' no chat do telegram ' + str(id_telegram))
            texto = "Oi " + apelido + ", \n\n"
            texto += "*ATENÇÃO:*\n"
            texto += mensagem

            print(texto)
            bot = telegram.Bot(token=telegram_token)
            bot.send_message(chat_id=id_telegram, text=texto, parse_mode=telegram.ParseMode.MARKDOWN)
            j += 1
        if (j == 0):
            print(descricao + ' não encontrado(s).')
            return j
        else:
            print(f'{j} ' + descricao + ' encontrados.')
            return j
    except:
        print(f'2 Ocorreu um erro: {sys.exc_info()}')


def urlOrds(urlData, username, password):
    req = urllib.request.Request(urlData)
    credentials = ('%s:%s' % (username, password))
    encoded_credentials = base64.b64encode(credentials.encode('ascii'))
    req.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))
    return urllib.request.urlopen(req)


def handler(ctx, data: io.BytesIO=None):
    alarm_msg = {}
    mensagem = message_id = func_response = ""
    urlPlantonista = urlTrabalhando = dbuser = dbpwd = TELEGRAM_TOKEN = ""

    # parametros
    try:
        cfg = ctx.Config()
        urlPlantonista = cfg["URLPLANTONISTA"]
        urlTrabalhando = cfg["URLTRABALHANDO"]
        dbuser = cfg["DBUSER"]
        dbpwd = cfg["DBPWD"]
        TELEGRAM_TOKEN = cfg["TELEGRAM_TOKEN"]
    except Exception as e:
        print('ERROR: Parametros ausentes: urlPlantonista, urlTrabalhando, dbuser, dbpwd, telegram_token', flush=True)
        raise

    # mensagem do alarme
    try:
        alarm_msg = json.loads(data.getvalue())
        if "title" in alarm_msg:
            mensagem  = "- ASSUNTO = " + alarm_msg["title"] + "\n"
        if "timestamp" in alarm_msg:
            mensagem += "- HORA    = " + alarm_msg["timestamp"] + "\n"
        if "severity" in alarm_msg:
            mensagem += "- NIVEL   = " + alarm_msg["severity"] + "\n"
        if "alarmMetaData" in alarm_msg:
            mensagem += "- MOTIVO  = " + alarm_msg['alarmMetaData'][0]['query'] + "\n\n"
        print("INFO: " + mensagem)
    except (Exception, ValueError) as ex:
        print("ERROR: " + str(ex), flush=True)

    # origem do alarme
    try:
        headers = ctx.Headers()
        message_id = headers["x-oci-ns-messageid"]
    except Exception as ex:
        print('ERROR: Missing Message ID in the header', ex, flush=True)
        raise
    print("INFO: Message ID = ", message_id, flush=True)

    # Transmitindo o aviso
    try:
        webUrl = urlOrds(urlPlantonista, dbuser, dbpwd)
        if webUrl.getcode() == 200:
            data = webUrl.read()
            if enviaMensagem(data, 'plantonista', mensagem, TELEGRAM_TOKEN) == 0:
                webUrl = urlOrds(urlTrabalhando, dbuser, dbpwd)
                if webUrl.getcode() == 200:
                    data = webUrl.read()
                    enviaMensagem(data, 'trabalhando', mensagem, TELEGRAM_TOKEN)
                else:
                    print('Erro de conexão, sem resultados ' + str(webUrl.getcode()))
        else:
            print(' [] Erro de conexão, sem resultados ' + str(webUrl.getcode()))
    except:
        print(f'1 Ocorreu um erro: {sys.exc_info()}')
