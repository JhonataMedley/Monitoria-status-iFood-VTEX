# estudar melhor esse codigo, criar funcoes para enviar a mensagem pra limpar mais o cofigo, realizar a implementação do uma verificação de se o staus voltou ao normal para enviar uma mensagem de que voltou ao normal.
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



#funcao de enviar mensagem para o space do google chat 
def enviar_mensagem(site, frase, url):
    webhook_url = os.getenv("google_chat_teste")
    mensagem = {
        "text": f"o status atual da {site} é {frase}! \nAguardando 30 minutos antes de verificar novamente. \nFonte: {url}"
    }
    headers = {"contet-Type": "application/json; charset=UTF-8"}
    requests.post(webhook_url, data=json.dumps(mensagem), headers=headers)
    print("mensagem enviada com sucesso!")









def verificar_IFOOD():
    global status_atual_ifood, status_normal_ifood

    pegina_ifood = requests.get(url_ifood, timeout=15)
    dados_pagina_ifood = BeautifulSoup(pegina_ifood.text, 'html.parser')
    site = dados_pagina_ifood.find('title').text
    frase = dados_pagina_ifood.find('h2', class_='status font-large').text.strip()

    # Status atual ESTAVA ruim (diferente do normal)
    status_estava_ruim = status_atual_ifood != status_normal_ifood
    
    # Status AGORA está normal
    status_agora_normal = frase == status_normal_ifood

    # Se estava ruim E agora está normal → voltou ao normal
    if status_estava_ruim and status_agora_normal:
        enviar_mensagem(site, "O status voltou ao normal!", url_ifood)
    
    # Se está diferente do normal E era diferente também → está ainda ruim
    elif frase != status_normal_ifood and status_atual_ifood != frase:
        enviar_mensagem(site, frase, url_ifood)
    
    # Atualiza o status
    status_atual_ifood = frase








def verificar_VTEX():
    global status_atual_vtex
    pegina_vtex = requests.get(url_vtex, timeout=15)
    dados_pagina_vtex = BeautifulSoup(pegina_vtex.text, 'html.parser')
    site = dados_pagina_vtex.find('title').text
    frase = dados_pagina_vtex.find('li').text

    if status_atual_vtex != frase:
        enviar_mensagem(site, frase, url_vtex)
        status_atual_vtex = frase











while True:
 
    verificar_IFOOD()
    verificar_VTEX() 
    sleep(60)