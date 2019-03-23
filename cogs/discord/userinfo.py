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

class userinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

###########################################
# Comando com (cooldown, only guild)
###########################################

    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def userinfo(self, ctx, *, user: discord.Member = None):
       if get_rank(ctx.author.id, list(ctx.author.guild_permissions), ctx.guild.id, ctx.channel.id) >=1:
           lang = get_lang(ctx.guild.id, "userinfo")

           if user is None:
               usuario = ctx.author
               titulo = str(lang['title_one']).format(ctx.author.name)
           else:
              usuario = user
              titulo = str(lang['title_two']).format(ctx.author.name, usuario.name)

           if usuario.display_name == usuario.name:
               apelido = lang['not_defined']
           else:
              apelido = usuario.display_name
           if usuario.avatar_url_as()  == "":
           	  img = lang['img']
           else:
             img = usuario.avatar_url_as()
           try:
             jogo = usuario.activity.name
           except:
               jogo = lang['not_defined']
           if usuario.id in [y.id for y in ctx.guild.members if not y.bot]:
              bot = lang['no']
           else:
             bot = lang['yes']
           entrou_servidor = str(usuario.joined_at.strftime("%H:%M:%S - %d/%m/20%y"))
           conta_criada = str(usuario.created_at.strftime("%H:%M:%S - %d/%m/20%y"))
           cargos = len([r.name for r in usuario.roles if r.name != "@everyone"])
           on = lang['on']
           off = lang['off']
           dnd = lang['dnd']
           afk = lang['afk']
           stat = str(usuario.status).replace("online",on).replace("offline",off).replace("dnd",dnd).replace("idle",afk)
           cargos2 = len([y.id for y in ctx.guild.roles])
           embed = discord.Embed(title=titulo,colour=0x7BCDE8)
           embed.set_author(name=lang['author'], icon_url=ctx.author.avatar_url_as())
           embed.add_field(name=lang['tag'], value = "``"+str(usuario.name)+"#"+str(usuario.discriminator)+"``", inline=True)
           embed.add_field(name=lang['id'], value = "``"+str(usuario.id)+"``", inline=True)
           embed.add_field(name=lang['nick'], value = "``"+str(apelido)+"``", inline=True)
           embed.add_field(name=lang['created'], value = "``"+str(conta_criada)+"``", inline=True)
           embed.add_field(name=lang['join'], value = "``"+str(entrou_servidor)+"``", inline=True)
           embed.add_field(name=lang['top_role'], value = "``"+str(usuario.top_role)+" - ("+str(usuario.top_role.color)+")``", inline=True)
           embed.add_field(name=lang['roles'], value = "``"+str(cargos)+"/"+str(cargos2)+"``", inline=True)
           embed.add_field(name=lang['bot'], value = "``"+str(bot)+"``", inline=True)
           embed.add_field(name=lang['status'], value = "``"+str(stat)+"``", inline=True)
           embed.add_field(name=lang['playing'], value = "``"+str(jogo)+"``", inline=True)
           embed.set_thumbnail(url=img)
           embed.set_footer(text=self.client.user.name+" © 2019", icon_url=self.client.user.avatar_url_as())
           await ctx.send(embed = embed)
       else:
         await ctx.add_reaction(config["emoji"]["cadeado"])

###########################################
# Função leitura do cog
###########################################

def setup(client):
    client.add_cog(userinfo(client))
