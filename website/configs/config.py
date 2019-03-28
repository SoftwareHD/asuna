###########################################
# Lista de imports
###########################################

import time
import json
import os
from pymongo import MongoClient
import pymongo
###########################################
# Leitura de dados (token, url db, etc)
###########################################

with open('./json/dados.json', encoding='utf-8') as json_dados:
  config = json.load(json_dados)  


###########################################
# Conexão com database
###########################################

try:
  db = MongoClient(config["database"])
  print("[OK] - Conectado com sucesso ao database.")
except Exception as e:
  print(f"[Exception] - Houve um erro na conexão\n[Erro] - {e}")

###########################################
# Database settings
###########################################

servidor_status = db["raphtalia"]["guild"]

def get_guild_insert(guild):
      data = {"_id":guild,
              "status_welcome":False,
              "tipo_welcome":"1",
              "canal_welcome":None,
              "message_welcome":"Olá (member_mention), seja bem vindo ao (server_name)",
              "private_welcome":False,
              "status_leave":False,
              "tipo_leave":"1",
              "canal_leave":None,
              "message_leave":"O usuário (member_name), saiu do servidor.",
              "level_up_status":False,
              "canal_level_up":None,
              "private_level_up":None,
              "channel_level_up":None,
              "setado_level_up":None,
              "auto_role":None,
              "status_auto_role":False,
              "guild_lock":False,
              "channel_lock":[],
              "user_block":[],
              "prefix":"a!",
              "language":"english"

              }
      servidor_status.insert_one(data).inserted_id
      return data

def get_guild_find(ids):
  dados = servidor_status.find_one(ids)
  if dados is None:
    return get_guild_insert(ids)
  return dados
