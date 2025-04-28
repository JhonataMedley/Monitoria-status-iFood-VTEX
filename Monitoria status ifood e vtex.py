import sys
import io
import os
from time import sleep

import requests
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
load_dotenv()

# URL da página de status
url_vtex = "https://status.vtex.com/"
url_ifood = "https://ifood-merchant-api.statuspage.io/"

alertou_vtex = False
alertou_ifood = False


while True:
    try: 


        # Fazendo a requisição
        response_vtex = requests.get(url_vtex, timeout=15)
        response_ifood = requests.get(url_ifood, timeout=15)

        if response_vtex.status_code == 200:
            html = BeautifulSoup(response_vtex.text, 'html.parser')

            status = html.find('li')
            status_vtex = status.get_text()

            if status_vtex != "We’re fully operational": 
                #escreve a mensagem e envia no space
                webhook_url = os.getenv("google_chat_teste")
                message = {
                    "text": f"O status atual da vtex é {status_vtex}! \nAguardando 30 minutos antes de verificar novamente. \nFonte:{url_vtex}"
                }
                headers = {"Content-Type": "application/json; charset=UTF-8"}
                requests.post(webhook_url, data=json.dumps(message), headers=headers)
                alertou_vtex = True
                


        if response_ifood.status_code == 200: 
            html = BeautifulSoup(response_ifood.text, 'html.parser')
            status = html.find('h2')
            status_ifood = status.get_text().strip()
            if status_ifood != "All Systems Opertional": 
                #escreve a mensagem e envia no space
                webhook_url = os.getenv("google_chat_teste")
                message = {
                    "text": f"O status atual do iFood é {status_ifood}! \nAguardando 30 minutos antes de verificar novamente. \nFonte:{url_ifood}"
                }
                headers = {"Content-Type": "application/json; charset=UTF-8"}
                requests.post(webhook_url, data=json.dumps(message), headers=headers)
                alertou_ifood = True

        if alertou_vtex or alertou_ifood:
            sleep(1800)
            alertou_vtex = False
            alertou_ifood = False
        else:
            sleep(10)

        sys.stdout.flush()
        

    except requests.exceptions.RequestException as erro:
        print(f"erro de conexão: {erro}")



