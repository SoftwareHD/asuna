###########################################
# Lista de imports
###########################################

import time
import json
import os
from pymongo import MongoClient
import pymongo
import discord


###########################################
# Leitura de dados (token, url db, etc)
###########################################
with open('configs/dados.json', encoding='utf-8') as json_data:
  config = json.load(json_data)

###########################################
# Conexão com database
###########################################
try:
  client = MongoClient(config["database"])
  print("[OK] - Conectado com sucesso ao database.")
except Exception as e:
  print(f"[Exception] - Houve um erro na conexão\n[Erro] - {e}")

###########################################
# Database settings
###########################################

servidor_status = client["raphtalia"]["guild"]

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

###########################################
# Multi-linguagem settings
###########################################      

response_string = {}
for i in os.listdir('./languages'):
  if i.endswith('.json'):
    with open(os.path.join('./languages', i), encoding='utf-8') as file:
      response = json.load(file)
    response_string[i.strip('.json')] = response


def get_lang(guild, cmd, response):
  servidor = servidor_status.find_one({"_id":guild})
  if servidor is None:
      get_guild_insert(guild)
      return response_string[servidor["language"]][cmd][response]  
  try:
    return response_string[servidor["language"]][cmd][response]
  except:
    return response_string['english'][cmd][response]

###########################################
#Multi-prefixo settings
###########################################

def get_prefix(guild):
    servidor = servidor_status.find_one({"_id":guild})
    if servidor is None:
       get_guild_insert(guild)
       return config["prefix_default"]
    try:
      if servidor["prefix"] is None:
       return config["prefix_default"]
      else:
        return servidor["prefix"]
    except KeyError:
      servidor_status.update_one({"_id":guild}, {"$set":{"prefix":"a!"}})
      return servidor["prefix"]
    else:   
      servidor_status.update_one({"_id":guild}, {"$set":{"prefix":"a!"}})
      return servidor["prefix"]

###########################################
# Sistema de permissão
###########################################

def get_rank(user, list_perma, guild, channel):
  servidor = servidor_status.find_one({"_id":guild})
  if servidor is None:
     get_guild_insert(guild)
     return 1  
  if not user in config["staff"]:
   if ('administrator', True) in list_perma: return 6
   elif ('manage_guild', True) in list_perma:return 5
   elif ('ban_members', True) in list_perma: return 4
   elif ('kick_members', True) in list_perma: return 3
   elif ('manage_roles', True) in list_perma: return 2
   elif channel in servidor["channel_lock"]:return -1
   elif servidor["guild_lock"] is True: return -2
   elif user in servidor["user_block"]:return -3
   else:
     return 1 
  else:
    if user in config["staff"]["dev"]:return 7
    elif user in config["staff"]["admin"]:return 6
    elif user in config["staff"]["moderator"]:return 5
    elif user in config["staff"]["ajudante"]:return 4
    elif user in config["staff"]["designer"]:return 3
    elif user in config["staff"]["hunterbug"]:return 2
    else:
      return 1




