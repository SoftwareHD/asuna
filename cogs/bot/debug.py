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
from configs.config import config
from configs.config import get_lang
from configs.config import get_rank

###########################################
# Class reformulada
###########################################

class debug(commands.Cog):
    def __init__(self, client):
        self.client = client

###########################################
# Comando com (cooldown, only guild)
###########################################


    @commands.cooldown(1,1,commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def debug(self,ctx, *,args=None):
       if get_rank(ctx.author.id, list(ctx.author.guild_permissions), ctx.guild.id, ctx.channel.id) == 7:
        lang = get_lang(ctx.guild.id, "debug")
        if args is None:
           embed = discord.Embed(description=lang['debug_none'].format(ctx.author.mention), color=0x7BCDE8)
           await ctx.send(embed=embed)
           return  
        
        args = args.strip('` ')
        python = '```py\n{}\n```'
        result = None
        env = {'client': self.client,'ctx': ctx}   
        env.update(globals())
        try:
            result = eval(args, env)
            if inspect.isawaitable(result):
               result = await result
            embed = discord.Embed(colour=0x7BCDE8)
            embed.set_author(name=lang['debug_title'], icon_url=ctx.author.avatar_url_as())
            embed.add_field(name=lang['debug_entry'], value = '```py\n{}```'.format(args), inline=True)
            embed.add_field(name=lang['debug_exit'], value = python.format(result), inline=True)
            embed.set_footer(text=self.client.user.name+" © 2018", icon_url=self.client.user.avatar_url_as())
            await ctx.send(embed=embed) 
        except Exception as e:
            embed = discord.Embed(colour=0x7BCDE8)
            embed.set_author(name=lang['debug_title'], icon_url=ctx.author.avatar_url_as())
            embed.add_field(name=lang['debug_entry'], value = '```py\n{}```'.format(args), inline=True)
            embed.add_field(name=lang['debug_exit'], value = python.format(type(e).__name__ + ': ' + str(e)), inline=True)
            embed.set_footer(text=self.client.user.name+" © 2018", icon_url=self.client.user.avatar_url_as())
            await ctx.send(embed=embed)
            
       else:
         await ctx.message.add_reaction(config["emojis"]["cadeado"])

###########################################
# Função leitura do cog
###########################################

def setup(client):
    client.add_cog(debug(client))
