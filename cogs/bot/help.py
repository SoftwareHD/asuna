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
import psutil
import os
from configs.config import *

site = "https://pt-asuna.herokuapp.com"
###########################################
# Class reformulada
###########################################

class help(commands.Cog):
    def __init__(self, client):
        self.client = client

###########################################
# Comando com (cooldown, only guild)
###########################################

    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def help(self,ctx, *, args=None):
       if get_rank(ctx.author.id, list(ctx.author.guild_permissions), ctx.guild.id, ctx.channel.id) >=1:
          lang = get_lang(ctx.guild.id, "help")
          if args is None:
            embed = discord.Embed(description=str(lang['description_embed']).format(ctx.author.name, self.client.user.name, site),colour=0x7BCDE8)
            embed.set_author(name=str(lang["title_embed"]), icon_url=ctx.author.avatar_url_as())
            embed.add_field(name=str(lang["discord"]), value =str(lang["discord_text"]), inline=True)
            embed.add_field(name=str(lang["asuna"]), value =str(lang["asuna_text"]), inline=True)
            embed.add_field(name=str(lang["search"]), value =str(lang["search_text"]), inline=True)
            embed.set_footer(text=self.client.user.name+" © 2019", icon_url=self.client.user.avatar_url_as())
            await ctx.send(embed=embed)
            return
          try:
            var = str(args.lower()).replace("link","google_link").replace("image","google_image")
            lang_2 = get_lang(ctx.guild.id, var)
            embed = discord.Embed(description=str(lang['description_embed_2']).format(ctx.author.name, args),colour=0x7BCDE8)
            embed.set_author(name=str(lang["title_embed"]), icon_url=ctx.author.avatar_url_as())
            embed.add_field(name=str(lang["title_help"]), value =", ".join(lang_2["title"]), inline=True)
            embed.add_field(name=str(lang["rank_help"]), value =lang_2["rank"], inline=True)
            embed.add_field(name=str(lang["aliase_help"]), value =", ".join(lang_2["aliases"]), inline=True)
            embed.add_field(name=str(lang["example_help"]), value =str(", ".join(lang_2["example"])).replace("{prefixo}",get_prefix(ctx.guild.id)), inline=True)
            embed.add_field(name=str(lang["description_help"]), value =lang_2["description"], inline=True)
            embed.set_footer(text=self.client.user.name+" © 2019", icon_url=self.client.user.avatar_url_as())
            await ctx.send(embed=embed)
          except Exception as e:
            embed = discord.Embed(description=lang['erro_help'].format(args), color=0x7BCDE8)
            await ctx.send(embed=embed)
            return  


       else:
         await ctx.message.add_reaction(config["emoji"]["cadeado"])

###########################################
# Função leitura do cog
###########################################

def setup(client):
    client.add_cog(help(client))
