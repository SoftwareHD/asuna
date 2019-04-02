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

lista = ["🇺🇸","🇧🇷"]
###########################################
# Class reformulada
###########################################

class language(commands.Cog):
    def __init__(self, client):
        self.client = client

###########################################
# Comando com (cooldown, only guild)
###########################################


    @commands.cooldown(1,1,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def language(self,ctx):
       if get_rank(ctx.author.id, list(ctx.author.guild_permissions), ctx.guild.id, ctx.channel.id) >= 5:
        lang = get_lang(ctx.guild.id, "language")

        embed = discord.Embed(description=lang['language_choice'].format(ctx.author.name, ctx.author.name), color=0x7BCDE8)
        msg  = await ctx.send(embed=embed)
        for reaction in lista:
          await msg.add_reaction(reaction)
 
        def check(reaction, user):
         return user == ctx.author and str(reaction.emoji)

        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
            if str(reaction.emoji) == "🇺🇸":
               get_guild_update_func(ctx.guild.id, "language", "english")
               embed = discord.Embed(description=lang['language_english'].format(ctx.author.name), color=0x7BCDE8)
               await msg.clear_reactions()
               await msg.edit(embed=embed)
            if str(reaction.emoji) == "🇧🇷":
               get_guild_update_func(ctx.guild.id, "language", "portuguese")
               embed = discord.Embed(description=lang['language_portuguese'].format(ctx.author.name), color=0x7BCDE8)
               await msg.clear_reactions()
               await msg.edit(embed=embed)
 
        except asyncio.TimeoutError:
            await msg.delete()

       else:
         await ctx.message.add_reaction(config["emojis"]["cadeado"])

###########################################
# Função leitura do cog
###########################################

def setup(client):
    client.add_cog(language(client))
