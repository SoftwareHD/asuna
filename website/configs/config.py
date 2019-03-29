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
              "welcome_channel":None,
              "welcome_type":3,
              "welcome_text":None,
              "welcome_private":False,
              "welcome_status":False,
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

def get_guild_update_welcome(ids, welcome_channel, welcome_type, welcome_text,welcome_private, welcome_status):
    servidor_status.update_many({"_id":ids},{"$set": {"welcome_channel":welcome_channel,"welcome_type":welcome_type, "welcome_text":welcome_text,"welcome_private":welcome_private,"welcome_status":welcome_status}})

def get_guild_update_func(ids, string, status):
    servidor_status.update_one({"_id":ids},{"$set": {string:status}})

###########################################
# Fim
###########################################
