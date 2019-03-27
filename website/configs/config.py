###########################################
# Lista de imports
###########################################

import time
import json
import os

###########################################
# Leitura de dados (token, url db, etc)
###########################################

with open('./json/dados.json', encoding='utf-8') as json_dados:
  config = json.load(json_dados)  


