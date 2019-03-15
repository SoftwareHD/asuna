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

class debug(commands.Cog):
    def __init__(self, client):
        self.client = client

###########################################
# Comando com (cooldown, only guild)
###########################################

    @commands.cooldown(1,10,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def debug(self,ctx, *,args=None):
       if get_rank(ctx.author.id, list(ctx.author.guild_permissions), ctx.guild.id, ctx.channel.id) ==7:
        if args is None:
           embed = discord.Embed(description=get_lang(ctx.guild.id, 'debug','debug_none').format(ctx.author.mention), color=0x7BCDE8)
           await ctx.send(embed=embed)
           return      
        try:
          embed = discord.Embed(colour=0x7BCDE8)
          embed.set_author(name=get_lang(ctx.guild.id, 'debug','debug_title'), icon_url=ctx.author.avatar_url_as())
          embed.add_field(name=get_lang(ctx.guild.id, 'debug','debug_entry'), value = '```py\n{}```'.format(args), inline=True)
          embed.add_field(name=get_lang(ctx.guild.id, 'debug','debug_exit'), value = '```py\n{}```'.format(eval(args)), inline=True)
          embed.set_footer(text=self.client.user.name+" © 2018", icon_url=self.client.user.avatar_url_as())
          await ctx.send(embed=embed)  
        except Exception as e:
            embed = discord.Embed(colour=0x7BCDE8)
            embed.set_author(name=get_lang(ctx.guild.id, 'debug','debug_title'), icon_url=ctx.author.avatar_url_as())
            embed.add_field(name=get_lang(ctx.guild.id, 'debug','debug_entry'), value = '```py\n{}```'.format(args), inline=True)
            embed.add_field(name=get_lang(ctx.guild.id, 'debug','debug_exit'), value = '```py\n{}```'.format(e), inline=True)
            embed.set_footer(text=self.client.user.name+" © 2018", icon_url=self.client.user.avatar_url_as())
            await ctx.send(embed=embed)       
       else:
         await ctx.message.add_reaction(config["emoji"]["cadeado"])

###########################################
# Função leitura do cog
###########################################

def setup(client):
    print("[Bot] : Cmd (debug) ")
    client.add_cog(debug(client))
