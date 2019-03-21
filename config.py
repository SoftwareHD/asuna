###########################################
# Lista de imports
###########################################

import time
import json
import os
from pymongo import MongoClient
import pymongo
import discord

timecache=dict()

###########################################
# Leitura de dados (token, url db, etc)
###########################################

with open('configs/dados.json', encoding='utf-8') as json_dados:
  config = json.load(json_dados)  

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
      return data

def get_guild_find(ids):
  dados = servidor_status.find_one(ids)
  if dados is None:
    return get_guild_insert(ids)
  return dados

###########################################
# Cache
###########################################

server_cache = {}

def server_date(server, dados):
  server_cache[server] = {}
  if dados:
     server_cache[server] = dados

def add(ids):
  server_date(ids, get_guild_find(ids))

def remove(ids):
  del server_cache[ids]

def get_cache(ids):
    if ids in timecache:
      w = json.loads(timecache[ids])
      if time.time() < w:
         return
    timecache[ids] = json.dumps(time.time()+1800)
    if ids in server_cache:
       remove(ids)
       time.sleep(1)
       add(ids)
    else:
      add(ids)

###########################################
# Multi-linguagem settings
###########################################      

translate = {}
for i in os.listdir('./languages'):
  if i.endswith('.json'):
    with open(os.path.join('./languages', i), encoding='utf-8') as file:
      response = json.load(file)
    translate[i.strip('.json')] = response

 
def get_lang(guild, cmd):
  if guild in server_cache:
   language = server_cache[guild]["language"]
   try:
     return translate[language][cmd] 
   except KeyError:
     return translate['english'][cmd]
  else:  
    return translate['english'][cmd]

###########################################
#Multi-prefixo settings
###########################################

def get_prefix(guild):
  if guild in server_cache:
   prefix = server_cache[guild]["prefix"]
   try:
     return prefix
   except KeyError:
     return "a!"
  else:  
    return "a!"

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




