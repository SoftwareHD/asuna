###########################################
# Lista de imports
###########################################

import discord
from discord.ext.commands import AutoShardedBot, when_mentioned_or
from configs.config import *

###########################################
# Prefixo customizado
###########################################

async def prefix(client, message):
  if message.guild:
    try:
      get_cache(message.guild.id)
      return when_mentioned_or(get_prefix(message.guild.id))(client, message)
    except KeyError:
      return when_mentioned_or(config['prefix_default'])(client, message)
  else:
    return when_mentioned_or(config['prefix_default'])(client, message)

###########################################
# Evento Bot (shard, prefixo, status)
###########################################
client = AutoShardedBot(command_prefix=prefix, case_insensitive=config["case_insensitive"], shard_count=config["shard_count"])

@client.event
async def on_ready():
  print(f"[OK] - {client.user.name} ({client.user.id}) conectada ao discord.")
  await client.change_presence(activity=discord.Streaming(name=config['prefix_default']+"help", url="https://www.twitch.tv/yuka"))

###########################################
# Leitura de modulos & Token
###########################################

if __name__ == '__main__':
  try:
    client.remove_command('help')
    for modulo in config["modulos"]:
      client.load_extension(modulo)
    print(f"[OK] - {len(config['modulos'])} modulos carregados.")
  except Exception as e:
     print(f"[Erro] - O modulo {modulo} não foi carregado.\n[Erro] - {e}")
  
  try:
    client.run(config["token"])
  except Exception as e:
     print(f"[Erro] - O não foi possivel conectar ao discord.\n[Erro] - {e}")


