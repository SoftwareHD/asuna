###########################################
# Lista de imports
###########################################

import discord
from discord.ext import commands
import random
import time
import asyncio
import json
from configs.config import config
from configs.config import get_lang
from configs.config import get_rank

###########################################
# Class reformulada
###########################################

class ping(commands.Cog):
    def __init__(self, client):
        self.client = client

###########################################
# Comando com (cooldown, only guild)
###########################################

    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def ping(self,ctx):
       if get_rank(ctx.author.id, list(ctx.author.guild_permissions), ctx.guild.id, ctx.channel.id) >=1:
        print(list(ctx.author.guild_permissions))
        lang = get_lang(ctx.guild.id, "ping")
        timep = time.time()
        embed = discord.Embed(description=str(lang['wait_little']).format(ctx.author.mention), color=0x7BCDE8)
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(2)
        ping = time.time() - timep
        texto_ping = str('{0:.2f}ms'.format(ping*70))
        texto_ping2 = '{0:.2f}ms'.format(self.client.latency * 1000)
        embed1 = discord.Embed(description=str(lang['ping_show']).format(texto_ping, texto_ping2), color=0x7BCDE8)
        await msg.edit(embed=embed1)
       else:
         await ctx.message.add_reaction(config["emoji"]["cadeado"])

###########################################
# Função leitura do cog
###########################################

def setup(client):
    client.add_cog(ping(client))
