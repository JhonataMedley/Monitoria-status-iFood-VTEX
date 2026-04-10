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

url_vtex = "https://status.vtex.com/"
status_normal_vtex = "We’re fully operational"
status_atual_vtex = ""

url_ifood = "https://ifood-merchant-api.statuspage.io/"
status_normal_ifood = "All Systems Operational"
status_atual_ifood = ""

#funcao de enviar mensagem
def enviar_mensagem(site, frase, url):
    webhook_url = os.getenv("google_chat_teste")
    mensagem = {
        "text": f"o status atual {site} é {frase}! \nFonte: {url}"
    }
    headers = {"Content-Type": "application/json; charset=UTF-8"}
    requests.post(webhook_url, data=json.dumps(mensagem), headers=headers)
    print("mensagem enviada com sucesso!")

def verificar_IFOOD():
    try:
        global status_atual_ifood, status_normal_ifood

        pegina_ifood = requests.get(url_ifood, timeout=15)
        dados_pagina_ifood = BeautifulSoup(pegina_ifood.text, 'html.parser')
        site = dados_pagina_ifood.find('title').text.split()[0]
        frase = dados_pagina_ifood.find('h2', class_='status font-large').text.strip()

        status_estava_ruim = status_atual_ifood != status_normal_ifood
        status_agora_normal = frase == status_normal_ifood


        if status_estava_ruim and status_agora_normal:
            enviar_mensagem(f"do {site}", frase, url_ifood)
        

        elif frase != status_normal_ifood and status_atual_ifood != frase:
            enviar_mensagem(f"do {site}", frase, url_ifood)
        
        status_atual_ifood = frase
    except requests.exceptions.RequestException as erro:
        print(f"Erro ao verificar iFood: {erro}")


def verificar_VTEX():
    try:
        global status_atual_vtex, status_normal_vtex

        pegina_vtex = requests.get(url_vtex, timeout=15)
        dados_pagina_vtex = BeautifulSoup(pegina_vtex.text, 'html.parser')
        site = dados_pagina_vtex.find('title').text
        frase = dados_pagina_vtex.find('li').text

        status_estava_ruim = status_atual_vtex != status_normal_vtex
        
        status_agora_normal = frase == status_normal_vtex

        if status_estava_ruim and status_agora_normal:
            enviar_mensagem(f"da {site}", frase, url_vtex)
        
        elif frase != status_normal_vtex and status_atual_vtex != frase:
            enviar_mensagem(f"da {site}", frase, url_vtex)
        
        status_atual_vtex = frase

    except requests.exceptions.RequestException as erro:
        print(f"Erro ao verificar VTEX: {erro}")


while True:
 
    verificar_IFOOD()
    verificar_VTEX() 
    sleep(60)