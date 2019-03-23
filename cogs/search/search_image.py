

###########################################
# Lista de imports
###########################################

import discord
from discord.ext import commands
import random
import time
import asyncio
import json
import requests
from bs4 import BeautifulSoup
import bs4
from configs.config import config
from configs.config import get_lang
from configs.config import get_lang_id
from configs.config import get_rank
from configs.paginator import Paginator


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
    @commands.command(aliases=["image","gis"])
    async def google_image(self,ctx, *, args=None):
       if get_rank(ctx.author.id, None, ctx.guild.id, ctx.channel.id) >=1:
        lang = get_lang(ctx.guild.id, "google_image")
        lang_id = get_lang_id(ctx.guild.id)
        if args is None:
           embed = discord.Embed(description=str(lang['search_none']).format(ctx.author.mention), color=0x7BCDE8)
           await ctx.send(embed=embed)
           return          
        try:
          if ctx.channel.is_nsfw() is True:
            safe = "off"
          else:
            safe = "on"
          if lang_id == "portuguese":
             query = f"{args} pt-br"
          else:
            query = f"{args}"             
            params = {"q": query, "safe": safe}
            headers = {"User-Agent": config["user_agent"]}
            r = requests.get(str(config["url_google_image"]).replace("{search}",str(query).replace(" ","%20")), params=params, headers=headers)
            soup = bs4.BeautifulSoup(r.text, "html.parser")
            list = []
            for a in soup.find_all("div",{"class":"rg_meta"}):
                gga = json.loads(a.text)["ou"]
                list.append(gga)
            em = discord.Embed(description=str(lang["find"]).format(args.title()),colour=0x7BCDE8)
            em.set_author(name=str(lang["gis"]), icon_url=ctx.author.avatar_url_as())
            em.set_footer(text=self.client.user.name+" © 2019", icon_url=self.client.user.avatar_url_as())
            paginator = Paginator(ctx, pages=list[:50], page_count=True, embed=em)
            await paginator.run()
        except Exception as error:
                embed = discord.Embed(description=str(lang["not_find"]).format(args.title()),colour=0x7BCDE8)
                await ctx.send(embed = embed) 
       else:
         await ctx.message.add_reaction(config["emoji"]["cadeado"])

###########################################
# Função leitura do cog
###########################################

def setup(client):
    client.add_cog(ping(client))
