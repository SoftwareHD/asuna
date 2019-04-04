

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
from configs.config import *
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
    @commands.command(aliases=["link","gs"])
    async def google_link(self,ctx, *, args=None):
       if get_rank(ctx.author.id, None, ctx.guild.id, ctx.channel.id) >=1:
        lang = get_lang(ctx.guild.id, "gs")
        lang_id = date_server_cache(ctx.guild.id)['language']
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
             query = f"{args} pt-br .com"
             lang_params = "pt-br"
          else:
            query = f"{args} .com"      
            lang_params = "en-us" 
          params = {"q": query, "safe": safe, "lang":lang_params}
          headers = {"Accept-Language": lang_params,"User-Agent": config["user_agent"]}
          r = requests.get(str(config["url_google_link"]).replace("{search}",str(query).replace(" ","%20")), params=params, headers=headers)
          soup = bs4.BeautifulSoup(r.text, "html.parser")
          title = []
          url = []
          total = []
          get = 0
          for b in soup.find_all("h3",{"class":"LC20lb"}):
              title.append(b.text)
          for a in soup.find_all("div",{"class":"r"}):
            z = BeautifulSoup(str(a), "html.parser")
            texto = z.find("a").get("href")
            if texto.startswith("http"):
               urls = f"{texto}"
               url.append(urls)
            else:
              urls = f"http://{texto}"
              url.append(urls)
            for a in range(len(url)):
              get += 1
              links = "".join(url[:1])
              titulo = "".join(title[:1])
              txt = f"``{get}°`` - [``{titulo}``]({links})"
              total.append(txt)
              url.pop(0)
              title.pop(0)
          if len(total) == 0:
             embed = discord.Embed(description=str(lang['not_find']).format(args), color=0x7BCDE8)
             await ctx.send(embed=embed)
             return      
          else:
            texto = "\n".join(total)
            embed = discord.Embed(description=str(lang["find"]).format(args, texto),colour=0x7BCDE8)
            embed.set_author(name=str(lang["gs"]), icon_url=ctx.author.avatar_url_as())
            embed.set_footer(text=self.client.user.name+" © 2019", icon_url=self.client.user.avatar_url_as())
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
            embed = discord.Embed(description=str(lang['not_find']).format(args), color=0x7BCDE8)
            await ctx.send(embed=embed)
            return          
       else:
         await ctx.message.add_reaction(config["emoji"]["cadeado"])

###########################################
# Função leitura do cog
###########################################

def setup(client):
    client.add_cog(ping(client))
try:
  pass
except Exception as e:
  raise e