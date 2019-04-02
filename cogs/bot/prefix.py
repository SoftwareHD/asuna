###########################################
# Lista de imports
###########################################

import discord
from discord.ext import commands
import random
import time
import asyncio
import json
import sys
import inspect
from configs.config import *


###########################################
# Class reformulada
###########################################

class prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

###########################################
# Comando com (cooldown, only guild)
###########################################


    @commands.cooldown(1,1,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def prefix(self,ctx, *,args=None):
       if get_rank(ctx.author.id, list(ctx.author.guild_permissions), ctx.guild.id, ctx.channel.id) >=5:
        lang = get_lang(ctx.guild.id, "prefix")
        if args is None:
           embed = discord.Embed(description=lang['prefix_none'].format(ctx.author.name), color=0x7BCDE8)
           await ctx.send(embed=embed)
           return  
  
        try:
           embed = discord.Embed(description=lang['prefix_set'].format(args), color=0x7BCDE8)
           get_guild_update_func(ctx.guild.id, "prefix", args)
           await ctx.send(embed=embed)
           return  
        except Exception as e:
           embed = discord.Embed(description=lang['prefix_erro'].format(args), color=0x7BCDE8)
           await ctx.send(embed=embed)
           return  
       else:
         await ctx.message.add_reaction(config["emojis"]["cadeado"])

###########################################
# Função leitura do cog
###########################################

def setup(client):
    client.add_cog(prefix(client))
