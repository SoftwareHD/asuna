###########################################
# Lista de imports
###########################################

import discord
from discord.ext import commands
import random
import time
import asyncio
import json
from config import config
from config import get_lang
from config import get_rank

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
           if user is None:
               usuario = ctx.author
               titulo = get_lang(ctx.guild.id, 'userinfo','title_one').format(ctx.author.name)
           else:
              usuario = user
              titulo = get_lang(ctx.guild.id, 'userinfo','title_two').format(ctx.author.name, usuario.name)

           if usuario.display_name == usuario.name:
               apelido = get_lang(ctx.guild.id, 'userinfo','not_defined')
           else:
              apelido = usuario.display_name
           if usuario.avatar_url_as()  == "":
           	  img = get_lang(ctx.guild.id, 'userinfo','img')
           else:
             img = usuario.avatar_url_as()
           try:
             jogo = ctx.author.activity.name
           except:
               jogo = get_lang(ctx.guild.id, 'userinfo','not_defined')
           if usuario.id in [y.id for y in ctx.message.guild.members if not y.bot]:
              bot = get_lang(ctx.guild.id, 'userinfo','no')
           else:
             bot = get_lang(ctx.guild.id, 'userinfo','yes')
           entrou_servidor = str(usuario.joined_at.strftime("%H:%M:%S - %d/%m/20%y"))
           conta_criada = str(usuario.created_at.strftime("%H:%M:%S - %d/%m/20%y"))
           cargos = len([r.name for r in usuario.roles if r.name != "@everyone"])
           on = get_lang(ctx.guild.id, 'userinfo','on')
           off = get_lang(ctx.guild.id, 'userinfo','off')
           dnd = get_lang(ctx.guild.id, 'userinfo','dnd')
           afk = get_lang(ctx.guild.id, 'userinfo','afk')
           stat = str(usuario.status).replace("online",on).replace("offline",off).replace("dnd",dnd).replace("idle",afk)
           cargos2 = len([y.id for y in ctx.message.guild.roles])
           embed = discord.Embed(title=titulo,colour=0x7BCDE8)
           embed.set_author(name=get_lang(ctx.guild.id, 'userinfo','author'), icon_url=ctx.author.avatar_url_as())
           embed.add_field(name=get_lang(ctx.guild.id, 'userinfo','tag'), value = "``"+str(usuario.name)+"#"+str(usuario.discriminator)+"``", inline=True)
           embed.add_field(name=get_lang(ctx.guild.id, 'userinfo','id'), value = "``"+str(usuario.id)+"``", inline=True)
           embed.add_field(name=get_lang(ctx.guild.id, 'userinfo','nick'), value = "``"+str(apelido)+"``", inline=True)
           embed.add_field(name=get_lang(ctx.guild.id, 'userinfo','created'), value = "``"+str(conta_criada)+"``", inline=True)
           embed.add_field(name=get_lang(ctx.guild.id, 'userinfo','join'), value = "``"+str(entrou_servidor)+"``", inline=True)
           embed.add_field(name=get_lang(ctx.guild.id, 'userinfo','top_role'), value = "``"+str(usuario.top_role)+" - ("+str(usuario.top_role.color)+")``", inline=True)
           embed.add_field(name=get_lang(ctx.guild.id, 'userinfo','roles'), value = "``"+str(cargos)+"/"+str(cargos2)+"``", inline=True)
           embed.add_field(name=get_lang(ctx.guild.id, 'userinfo','bot'), value = "``"+str(bot)+"``", inline=True)
           embed.add_field(name=get_lang(ctx.guild.id, 'userinfo','status'), value = "``"+str(stat)+"``", inline=True)
           embed.add_field(name=get_lang(ctx.guild.id, 'userinfo','playing'), value = "``"+str(jogo)+"``", inline=True)
           embed.set_thumbnail(url=img)
           embed.set_footer(text=self.client.user.name+" © 2018", icon_url=self.client.user.avatar_url_as())
           await ctx.send(embed = embed)
       else:
         await ctx.message.add_reaction(config["emoji"]["cadeado"])

###########################################
# Função leitura do cog
###########################################

def setup(client):
    print("[Bot] : Cmd (userinfo) ")
    client.add_cog(userinfo(client))
