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

class channelinfo(commands.Cog):
    def __init__(self, client):
        self.client = client

###########################################
# Comando com (cooldown, only guild)
###########################################

    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def channelinfo(self, ctx, *, num=None):
       if get_rank(ctx.author.id, list(ctx.author.guild_permissions), ctx.guild.id, ctx.channel.id) >=1:
         lang = get_lang(ctx.guild.id, "channelinfo")
         if str(num).isdigit() == True:
           channel = discord.utils.get(ctx.guild.channels, id=int(num))
         else:
           if "<#" in num:
              num = str(num).replace("<#","").replace(">","")
              channel = discord.utils.get(ctx.guild.channels, id=int(num))
           else:
             channel = discord.utils.get(ctx.guild.channels, name=num)

         if channel is None:
           embed = discord.Embed(description=lang['none'].format(num), color=0x7BCDE8)
           await ctx.send(embed=embed)
           return  

         if channel in list(ctx.guild.text_channels):
            channel_type = lang["text"]
         elif channel in list(ctx.guild.voice_channels):
           channel_type = lang["voice"]
         else:
           embed = discord.Embed(description=lang['none'].format(num), color=0x7BCDE8)
           await ctx.send(embed=embed)
           return  
         
         channel_created = str(channel.created_at.strftime("%H:%M:%S - %d/%m/20%y"))
         embed = discord.Embed(description=str(lang['description_embed']).format(ctx.author.name, channel.mention),colour=0x7BCDE8)
         embed.set_author(name=lang['author'], icon_url=ctx.author.avatar_url_as())
         embed.add_field(name=lang['name'], value = "``"+str(channel.name)+"``", inline=True)
         embed.add_field(name=lang['id'], value = "``"+str(channel.id)+"``", inline=True)
         embed.add_field(name=lang['created'], value = "``"+str(channel_created)+"``", inline=True)
         embed.add_field(name=lang['position'], value = "``"+str(channel.position)+"``", inline=True)
         embed.add_field(name=lang['type'], value = "``"+str(channel_type)+"``", inline=True)
         try:
           embed.add_field(name=lang['porn'], value = "``"+str(channel.is_nsfw()).replace("False",lang["no"]).replace("True",lang["yes"])+"``", inline=True)
           if channel.slowmode_delay == 0:
              valor = lang["not_defined"]
           else:
             valor = str(lang["time"]).format(channel.slowmode_delay)
           embed.add_field(name=lang['slow'], value = "``"+str(valor)+"``", inline=True)
           if channel.topic is None:
              topic = lang["not_defined"]
           else:
             topic = channel.topic
           embed.add_field(name=lang['topic'], value = "``"+str(topic[:1024])+"``", inline=True)          
         except:
           pass
         try:
           embed.add_field(name=lang['bitrate'], value = "``"+str(channel.bitrate)+"``", inline=True)
           if channel.user_limit != 0:
             embed.add_field(name=lang['users'], value="``{}/{}``".format(len(channel.members), channel.user_limit))
           else:
             embed.add_field(name=lang['users'], value="``{}``".format(len(channel.members)))          
         except:
           pass         


         embed.set_footer(text=self.client.user.name+" © 2019", icon_url=self.client.user.avatar_url_as())
         await ctx.send(embed = embed)

       else:
         await ctx.add_reaction(config["emoji"]["cadeado"])

###########################################
# Função leitura do cog
###########################################

def setup(client):
    client.add_cog(channelinfo(client))
