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
with open('./json/modlog.json', encoding='utf-8') as json_dados:
  modlog = json.load(json_dados)

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

servidor_status = db["asuna"]["guild"]

def get_guild_insert(guild):
    data= {"_id":guild,
            "welcome":{"channel":None,
                       "type":3,
                       "text":None,
                       "status":False,
                       "private":False
                      },
            "leave":{"channel":None,
                       "type":3,
                       "text":None,
                       "status":False,
                       "private":False
                      },
            "autorole":{"role":None,
                        "status":False                 
                      },
            "suggestion":{"channel":None,
                          "status":False                 
                         },
            "membercount":{"channel":None,
                          "status":False                 
                         },
            "modlog":{"channel":None,
                      "status":False,
                      "user_ban":False,
                      "user_unban":False,
                      "user_kick":False,
                      "user_mute":False,
                      "role_create":False,
                      "role_delete":False,
                      "role_update":False,
                      "channel_create":False,
                      "channel_delete":False,
                      "channel_update":False,
                      "emoji_create":False,
                      "emoji_delete":False,
                      "message_edit":False,
                      "message_delete":False,
                      "message_delete_am":False,
                      "user_name":False,
                      "user_avatar":False,
                      "user_nickname":False
                     },                         
            "config":{"prefix":"a!",
                      "language":"english"                 
                      },
            "block":{"channel":[],
                     "guild":False,
                     "users":[]            
                     }          

          }
    servidor_status.insert_one(data).inserted_id
    return data

def get_guild_find(ids):
  dados = servidor_status.find_one(ids)
  if dados is None:
    return get_guild_insert(ids)
  return dados

def get_guild_update_welcome(ids, channel,type, text, private):
    servidor_status.update_many({"_id":ids},{"$set": {"welcome.channel":channel,"welcome.type":type,"welcome.text":text,"welcome.status":True,"welcome.private":private}})

def get_guild_update_leave(ids, channel,type, text, private):
    servidor_status.update_many({"_id":ids},{"$set": {"leave.channel":channel,"leave.type":type,"leave.text":text,"leave.status":True,"leave.private":private}})

def get_guild_update_autorole(ids, role,status):
    servidor_status.update_many({"_id":ids},{"$set": {"autorole.role":role,"autorole.status":status}})

def get_guild_update_suggestion(ids, channel,status):
    servidor_status.update_many({"_id":ids},{"$set": {"suggestion.channel":channel,"suggestion.status":status}})

def get_guild_update_membercount(ids, channel,status):
    servidor_status.update_many({"_id":ids},{"$set": {"suggestion.channel":channel,"suggestion.status":status}})
def get_guild_update_modlog(ids,channel,user_ban,user_unban,user_kick,user_mute,role_create,role_delete,role_update,channel_create,channel_delete,channel_update,emoji_create,emoji_delete,message_edit,message_delete,message_delete_am,user_name,user_avatar,user_nickname):
    servidor_status.update_many({"_id":ids},{"$set": {'modlog.channel':channel,
                                                            'modlog.user_ban':user_ban,
                                                            'modlog.user_unban':user_unban,
                                                            'modlog.user_kick':user_kick,
                                                            'modlog.user_mute':user_mute,
                                                            'modlog.role_create':role_create,
                                                            'modlog.role_delete':role_delete,
                                                            'modlog.role_update':role_update,
                                                            'modlog.channel_create':channel_create,
                                                            'modlog.channel_delete':channel_delete,
                                                            'modlog.channel_update':channel_update,
                                                            'modlog.emoji_create':emoji_create,
                                                            'modlog.emoji_delete':emoji_delete,
                                                            'modlog.message_edit':message_edit,
                                                            'modlog.message_delete':message_delete,
                                                            'modlog.message_delete_am':message_delete_am,
                                                            'modlog.user_name':user_name,
                                                            'modlog.user_avatar':user_avatar,
                                                            'modlog.user_nickname':user_nickname}})

def get_guild_update_funcao(ids, var, value):
    servidor_status.update_many({"_id":ids},{"$set": {var:value}})



###########################################
# Fim
###########################################
