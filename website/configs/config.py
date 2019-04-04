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
              "leave_channel":None,
              "leave_type":3,
              "leave_text":None,
              "leave_status":False,
              "autorole_role":None,
              "autorole_status":False,
              "suggestion_channel":None,
              "suggestion_status":False,
              "membercount_channel":None,
              "membercount_status":False,
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

def get_guild_update_leave(ids, leave_channel, leave_type, leave_text, leave_status):
    servidor_status.update_many({"_id":ids},{"$set": {"leave_channel":leave_channel,"leave_type":leave_type, "leave_text":leave_text,"leave_status":leave_status}})

def get_guild_update_two(ids, one_var,one_string, two_var,two_string):
    servidor_status.update_many({"_id":ids},{"$set": {one_var:one_string, two_var:two_string}})

def get_guild_update_func(ids, string, status):
    servidor_status.update_one({"_id":ids},{"$set": {string:status}})

###########################################
# Fim
###########################################
