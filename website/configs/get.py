###########################################
# Lista de imports
###########################################

import time
import json
import os
import requests
from configs.config import *

###########################################
# Lista de gets
###########################################

def get_guild(server_id):
    headers = {'Authorization': config["token_bot"]}
    r = requests.get(config["url_api"]+"/guilds/{}".format(server_id),headers=headers)
    if r.status_code == 200:
        return r.json()
    return None

def get_guild_members(server_id):
    headers = {'Authorization': config["token_bot"]}
    members = []
    MAX_MEMBERS = 5000
    while True:
        params = {'limit': 1000}
        if len(members):
            params['after'] = members[-1]['user']['id']

        r = requests.get(config["url_api"]+'/guilds/{}/members'.format(server_id),params=params,headers=headers)

        if r.status_code == 200:
            chunk = r.json()
            members += chunk
            if chunk == [] or len(members) >= MAX_MEMBERS:
              break
        else:
            break

    return members

def get_guild_channels(server_id):
        channels = []
        headers = {'Authorization': config["token_bot"]}
        r = requests.get(config["url_api"]+'/guilds/{}/channels'.format(server_id), headers=headers)
        if r.status_code == 200:
           texto = list(filter(lambda c: c['guild_id'], r.json()))
           for chan in texto:
               channels.append(chan['id'])
    
        return channels

def get_guild_channels_type(server_id, text):
        members = []
        headers = {'Authorization': config["token_bot"]}
        r = requests.get(config["url_api"]+'/guilds/{}/channels'.format(server_id), headers=headers)
        if r.status_code == 200:
            channels = r.json()
            channels = list(filter(lambda c: c['type'] == text,channels))
            return channels
        return None
def get_guild_roles(server_id):
        headers = {'Authorization': config["token_bot"]}
        r = requests.get(config["url_api"]+'/guilds/{}/roles'.format(server_id), headers=headers)
        if r.status_code == 200:
           roles = r.json()
        return roles       

def get_invite_link(bot, guild, redirect):
    convite = str(config["url_invite"]).format(bot, guild, redirect)
    return convite

def get_date_guild(server_id):
   members = get_guild_members(server_id)    
   channels = get_guild_channels(server_id)    
   roles = get_guild_channels(server_id)  
   lista = {"members":len(members),"channels":len(channels), "roles":len(roles)}
   return lista  

###########################################
# Fim
###########################################
  