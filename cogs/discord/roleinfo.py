###########################################
# Lista de imports
###########################################

import discord
from discord.ext import commands
import random
import time
import asyncio
import json
from configs.config import *



###########################################
# Class reformulada
###########################################

class roleinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

###########################################
# Comando com (cooldown, only guild)
###########################################

    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def roleinfo(self, ctx, *, num=None):
       if get_rank(ctx.author.id, list(ctx.author.guild_permissions), ctx.guild.id, ctx.channel.id) >=1:
          lang = get_lang(ctx.guild.id, "roleinfo")
          if num is None:
             embed = discord.Embed(description=str(lang['none_2']).format(ctx.author.name), color=0x7BCDE8)
             await ctx.send(embed=embed)
             return 
          if str(num).isdigit() == True:
            role = discord.utils.get(ctx.guild.roles, id=int(num))
          else:
            if "<@&" in num:
               num = str(num).replace("<@&","").replace(">","")
               role = discord.utils.get(ctx.guild.roles, id=int(num))
            else:
               role = discord.utils.get(ctx.guild.roles, name=num)

            if role is None:
              embed = discord.Embed(description=lang['none'].format(num), color=0x7BCDE8)
              await ctx.send(embed=embed)
              return  
            perma_audio = []
            perma_geral = []
            lista_audio = ["connect","speak","mute_members","deafen_members","move_members","use_voice_activation"]
            for perm in role.permissions:
              cargo = perm[0]
              if perm[1] == True:
               if cargo in lista_audio:
                  dados = lang[cargo]
                  perma_audio.append(dados)
               else:
                 dados = lang[cargo]
                 perma_geral.append(dados)

            if len(perma_geral) == 0:
              cargos = lang["not_permission"]
              txts = lang["geral"]
              texto = f"{txts}\n```\n{cargos}```"
            else:
              cargos = ", ".join(perma_geral)
              txts = lang["geral"]
              texto = f"{txts}\n```\n{cargos}```"
            if len(perma_audio) == 0:
              cargos2 = lang["not_permission"]
              txt = lang["voz"]
              texto2 = f"{txt}\n```\n{cargos2}```"
            else:
              cargos2 = ", ".join(perma_audio)
              txt = lang["voz"]
              texto2 = f"{txt}\n```\n{cargos2}```"
            textogeral = texto+texto2
            embed = discord.Embed(description=textogeral,colour=0x7BCDE8)
            if role.mentionable:
                a = lang["yes"]
            else:
                a = lang["no"]
            if role.hoist:
                b = lang["yes"]
            else:
                b = lang["no"]
            if role.managed:
              c = lang["yes"]
            else:
              c = lang["no"]
            color = str(role.colour).replace("#","")
            cor = f"https://htmlcolors.com/color-image/{color}.png"
            embed.set_author(name=lang["info"], icon_url=ctx.author.avatar_url_as())
            embed.add_field(name=lang["mentions"], value="``"+str(a)+"``")
            embed.add_field(name=lang["name"], value="``"+str(role.name)+"``")
            embed.add_field(name=lang["ids"], value="``"+str(role.id)+"``")
            criado_em = str(role.created_at.strftime("%H:%M:%S - %d/%m/20%y"))
            embed.add_field(name=lang["created"], value="``"+str(criado_em)+"``")
            embed.add_field(name=lang["pos"], value="``"+str(role.position)+"``")
            embed.add_field(name=lang["cor"], value="``"+str(role.colour)+"``")
            embed.add_field(name=lang["posts"], value="``"+str(b)+"``")
            embed.add_field(name=lang["reg"], value="``"+str(c)+"``")
            embed.set_thumbnail(url=cor)
            member = []
            for x in role.members:
              member.append(x)
            embed.add_field(name=lang["membs"], value="``"+str(len(member))+"``")
            embed.set_footer(text=self.client.user.name+" © 2019", icon_url=self.client.user.avatar_url_as())
            await ctx.send(embed=embed)


       else:
         await ctx.add_reaction(config["emoji"]["cadeado"])

###########################################
# Função leitura do cog
###########################################

def setup(client):
    client.add_cog(roleinfo(client))
