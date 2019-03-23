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

class serverinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

###########################################
# Comando com (cooldown, only guild)
###########################################

    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def serverinfo(self, ctx):
       if get_rank(ctx.author.id, list(ctx.author.guild_permissions), ctx.guild.id, ctx.channel.id) >=1:
           lang = get_lang(ctx.guild.id, "serverinfo")

           servidor = ctx.guild
           if servidor.icon_url_as(format="png") == "":
              img = "https://i.imgur.com/To9mDVT.png"
           else:
             img  = servidor.icon_url
           online = len([y.id for y in servidor.members if y.status == discord.Status.online])
           afk  = len([y.id for y in servidor.members if y.status == y.status == discord.Status.idle])
           offline = len([y.id for y in servidor.members if y.status == y.status == discord.Status.offline])
           dnd = len([y.id for y in servidor.members if y.status == y.status == discord.Status.dnd])
           geral = len([y.id for y in servidor.members])
           bots= len([y.id for y in servidor.members if y.bot])
           criado_em = str(servidor.created_at.strftime("%H:%M:%S - %d/%m/20%y"))
           usuarios = "<:online:558500234079109146> : ``"+str(online)+"`` <:idle:558500233974120470> : ``"+str(afk)+"`` <:dnd:558500234091560961> : ``"+str(dnd)+"`` <:offline:558500234078978078> : ``"+str(offline)+"`` <:robot:556280025754894336> : ``"+str(bots)+"``"
           texto = "<:hashtag:558397558549118978> : ``"+str(len(servidor.text_channels))+"``<:sound:558500897676853258>  : ``"+str(len(servidor.voice_channels))+"``"
           cargos = len([y.id for y in servidor.roles])
           emojis = len([y.id for y in servidor.emojis])
           embed = discord.Embed(title=str(lang["title"]).format(ctx.author.name, servidor.name),colour=0x7BCDE8)
           embed.set_author(name=lang["about"], icon_url=ctx.author.avatar_url_as())
           embed.add_field(name=lang["onwer"], value = "``"+str(servidor.owner)+"``", inline=True)
           embed.add_field(name=lang["name"], value = "``"+str(servidor.name)+"``", inline=True)
           embed.add_field(name=lang["id"], value = "``"+str(servidor.id)+"``", inline=True)
           embed.add_field(name=lang["created"], value = "``"+str(criado_em)+"``", inline=True)
           embed.add_field(name=lang["roles"], value = "``"+str(cargos)+"``", inline=True)
           embed.add_field(name=lang["emojis"], value = "``"+str(emojis)+"``", inline=True)
           embed.add_field(name=lang["channels"], value = texto, inline=True)
           embed.add_field(name=lang["location"], value = "``"+str(servidor.region).title()+"``", inline=True)
           embed.add_field(name=lang["level"], value = "``"+str(servidor.verification_level).replace("none",lang["none"]).replace("low",lang["low"]).replace("medium",lang["medium"]).replace("high",lang["high"]).replace("extreme",lang["extreme"])+"``", inline=True)
           embed.add_field(name=lang["users"]+" ["+str(geral)+"]", value = usuarios, inline=True)
           embed.set_thumbnail(url=img)
           embed.set_footer(text=self.client.user.name+" © 2019", icon_url=self.client.user.avatar_url_as())
           await ctx.send(embed = embed)       
       else:
         await ctx.message.add_reaction(config["emoji"]["cadeado"])

###########################################
# Função leitura do cog
###########################################

def setup(client):
    client.add_cog(serverinfo(client))
