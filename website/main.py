###########################################
# Lista de imports
###########################################

from flask import Flask, session, request, url_for, render_template, redirect,jsonify, flash, abort, Response
from urllib.parse import quote
import requests, api, time, json
from configs.config import *
from configs.get import *

###########################################
# Leitura de dados (config, token)
###########################################
checks = []
app = Flask(__name__)
app.config['SECRET_KEY'] = config["secret_key"]

###########################################
# index primeira pagina do site
###########################################

@app.route('/')
def index():
  if session.get('token') is None:
    url_authentication = str(config["url_app"]).format(config["id_bot"], quote(config["redirect"]), quote(config["scopes"]))
    url_bot = str(config["url_bot"]).format(config["id_bot"], quote(config["redirect_3"]), quote("bot"))
    url = {"url_bot":url_bot, "url_authentication":url_authentication}
    return render_template('index.html', url=url, title="Asuna - Index")
  try:
    user = api.get_info(session.get('token'))
  except requests.exceptions.HTTPError:
    return "Token invalido!"
  url_bot = str(config["url_bot"]).format(config["id_bot"], quote(config["redirect_2"]), quote("bot"))
  url = {"url_bot":url_bot}
  return render_template('index.html', url=url, title="Asuna - Index", user=user)

###########################################
# callback (pegar o token do outh2)
###########################################

@app.route('/callback')
def response():
  code = request.args.get('code')
  try:
    res = api.exchange_code(code)
  except requests.exceptions.HTTPError:
    return "Token invalido!"
  session['token'] = res['access_token']
  session['scopes'] = str(config["scopes"]).split(" ")
  return redirect("/")

###########################################
# pagina de guilds do usuario
###########################################

@app.route('/guilds')
def guilds():
  if session.get('token') is None:
    return redirect('/')  
  try:
    user = api.get_info(session.get('token'))
    servers = api.get_guilds(session.get('token'))
    guilds = list(filter(lambda g: (g['owner'] is True) or bool((int(g['permissions']) >> 5) & 1),servers))
  except requests.exceptions.HTTPError:
       return redirect("/") 
  return render_template('select-server.html', user=user, guilds=guilds, title="Asuna - Servidores")

###########################################
# modulos da guild
###########################################

@app.route('/dashboard/<int:server_id>')
def dashboard(server_id):
    guild = get_guild(server_id)
    if guild is None:
       return redirect(get_invite_link(config["id_bot"], server_id, quote(config["redirect_2"])))  
    servers = api.get_guilds(session.get('token'))
    guilds = list(filter(lambda g: (g['owner'] is True) or bool((int(g['permissions']) >> 5) & 1),servers))
    perm = []
    for gg in guilds:
      if guild["id"] == gg["id"]:
         perm.append(guild["id"])
      else:
        pass
    guild_db = get_guild_find(server_id)
    if guild_db is None:
       return redirect(url_for('guilds'))
    
    if guild["id"] in perm:   
     try:
       user = api.get_info(session.get('token'))
       date = get_date_guild(server_id)
     except requests.exceptions.HTTPError:return redirect("/")
   
     return render_template('dashboard.html', guild=guild,guild_db=guild_db,user=user, date=date, title="Asuna - "+guild["name"])

###########################################
# modulo welcome
###########################################

@app.route('/dashboard/<int:server_id>/welcome')
def dashboard_welcome(server_id):
    guild = get_guild(server_id)
    if guild is None:
       return redirect(get_invite_link(config["id_bot"], server_id, quote(config["redirect_2"])))  
    servers = api.get_guilds(session.get('token'))
    guilds = list(filter(lambda g: (g['owner'] is True) or bool((int(g['permissions']) >> 5) & 1),servers))
    perm = []
    for gg in guilds:
      if guild["id"] == gg["id"]:
         perm.append(guild["id"])
      else:
        pass
    guild_db = get_guild_find(server_id)
    if guild_db is None:
       return redirect(url_for('guilds'))
    if server_id in checks:
       sts = True
       checks.remove(server_id)
    else:
      sts = False  
    
    if guild["id"] in perm:   
     try:
       user = api.get_info(session.get('token'))
       date = get_date_guild(server_id)
       channels = get_guild_channels_type(server_id, 0)

     except requests.exceptions.HTTPError:return redirect("/")
   
     return render_template('dashboard_welcome.html', guild=guild, sts=sts, channels=channels, guild_db=guild_db,user=user, date=date, title="Asuna - "+guild["name"])

###########################################
# get dados do welcome
###########################################

@app.route('/dashboard/<int:server_id>/welcome/update', methods=['POST'])
def update_welcome(server_id):
    guild_db = get_guild_find(server_id)
    if request.form["btn"] == "atualizar":
        welcome_text = request.form.get('welcome_message')
        private = request.form.get('private')
        if private == "on":
           welcome_private = True
        else:
           welcome_private = False
        welcome_channel = request.form.get('channel')
        welcome_type = request.form.get('type')
        if not server_id in checks:
           checks.append(server_id)
        else:
          pass        
        get_guild_update_welcome(server_id, welcome_channel, welcome_type, welcome_text,welcome_private, True)
        return redirect(url_for('dashboard_welcome', server_id=server_id))
    if request.form["btn"] == "resetar":
       get_guild_update_welcome(server_id, None, None, None,None, True)
       return redirect(url_for('dashboard_welcome', server_id=server_id))
    if request.form["btn"] == "desligar":
       get_guild_update_func(server_id, "welcome_status", False)       
       return redirect(url_for('dashboard_welcome', server_id=server_id))
    if request.form["btn"] == "ligar":
       get_guild_update_func(server_id, "welcome_status", True)       
       return redirect(url_for('dashboard_welcome', server_id=server_id))
###########################################
# modulo leave
###########################################

@app.route('/dashboard/<int:server_id>/leave')
def dashboard_leave(server_id):
    guild = get_guild(server_id)
    if guild is None:
       return redirect(get_invite_link(config["id_bot"], server_id, quote(config["redirect_2"])))  
    servers = api.get_guilds(session.get('token'))
    guilds = list(filter(lambda g: (g['owner'] is True) or bool((int(g['permissions']) >> 5) & 1),servers))
    perm = []
    for gg in guilds:
      if guild["id"] == gg["id"]:
         perm.append(guild["id"])
      else:
        pass
    guild_db = get_guild_find(server_id)
    if guild_db is None:
       return redirect(url_for('guilds'))
    if server_id in checks:
       sts = True
       checks.remove(server_id)
    else:
      sts = False  
    if guild["id"] in perm:   
     try:
       user = api.get_info(session.get('token'))
       date = get_date_guild(server_id)
       channels = get_guild_channels_type(server_id, 0)

     except requests.exceptions.HTTPError:return redirect("/")
   
     return render_template('dashboard_leave.html', guild=guild, sts=sts,channels=channels, guild_db=guild_db,user=user, date=date, title="Asuna - "+guild["name"])

###########################################
# get dados do leave
###########################################

@app.route('/dashboard/<int:server_id>/leave/update', methods=['POST'])
def update_leave(server_id):
    guild_db = get_guild_find(server_id)
    if request.form["btn"] == "atualizar":
        leave_text = request.form.get('leave_message')
        leave_channel = request.form.get('channel')
        leave_type = request.form.get('type')
        if not server_id in checks:
           checks.append(server_id)
        else:
          pass         
        get_guild_update_leave(server_id, leave_channel, leave_type, leave_text, True)
        return redirect(url_for('dashboard_leave', server_id=server_id))
    if request.form["btn"] == "resetar":
       get_guild_update_leave(server_id, None, None, None, True)
       return redirect(url_for('dashboard_leave', server_id=server_id))
    if request.form["btn"] == "desligar":
       get_guild_update_func(server_id, "leave_status", False)       
       return redirect(url_for('dashboard_leave', server_id=server_id))
    if request.form["btn"] == "ligar":
       get_guild_update_func(server_id, "leave_status", True)       
       return redirect(url_for('dashboard_leave', server_id=server_id))

###########################################
# modulo autorole
###########################################

@app.route('/dashboard/<int:server_id>/autorole')
def dashboard_autorole(server_id):
    guild = get_guild(server_id)
    if guild is None:
       return redirect(get_invite_link(config["id_bot"], server_id, quote(config["redirect_2"])))  
    servers = api.get_guilds(session.get('token'))
    guilds = list(filter(lambda g: (g['owner'] is True) or bool((int(g['permissions']) >> 5) & 1),servers))
    perm = []
    for gg in guilds:
      if guild["id"] == gg["id"]:
         perm.append(guild["id"])
      else:
        pass
    guild_db = get_guild_find(server_id)
    if guild_db is None:
       return redirect(url_for('guilds'))
    if server_id in checks:
       sts = True
       checks.remove(server_id)
    else:
      sts = False  
    if guild["id"] in perm:   
     try:
       user = api.get_info(session.get('token'))
       date = get_date_guild(server_id)
       roles = get_guild_roles(server_id)

     except requests.exceptions.HTTPError:return redirect("/")
   
     return render_template('dashboard_autorole.html', guild=guild, sts=sts,roles=roles, guild_db=guild_db,user=user, date=date, title="Asuna - "+guild["name"])

###########################################
# get dados do auto role
###########################################

@app.route('/dashboard/<int:server_id>/autorole/update', methods=['POST'])
def update_autorole(server_id):
    guild_db = get_guild_find(server_id)
    if request.form["btn"] == "atualizar":
        autorole_id = request.form.get('role_id')
        if not server_id in checks:
           checks.append(server_id)
        else:
          pass         
        get_guild_update_func(server_id, "autorole_role", autorole_id)       
        return redirect(url_for('dashboard_autorole', server_id=server_id))
    if request.form["btn"] == "resetar":
       get_guild_update_two(ids, "autorole_role",None, "autorole_status",autorole_id)
       return redirect(url_for('dashboard_autorole', server_id=server_id))
    if request.form["btn"] == "desligar":
       get_guild_update_func(server_id, "autorole_status", False)       
       return redirect(url_for('dashboard_autorole', server_id=server_id))
    if request.form["btn"] == "ligar":
       get_guild_update_func(server_id, "autorole_status", True)       
       return redirect(url_for('dashboard_autorole', server_id=server_id))

###########################################
# modulo sugestão
###########################################

@app.route('/dashboard/<int:server_id>/suggestion')
def dashboard_suggestion(server_id):
    guild = get_guild(server_id)
    if guild is None:
       return redirect(get_invite_link(config["id_bot"], server_id, quote(config["redirect_2"])))  
    servers = api.get_guilds(session.get('token'))
    guilds = list(filter(lambda g: (g['owner'] is True) or bool((int(g['permissions']) >> 5) & 1),servers))
    perm = []
    for gg in guilds:
      if guild["id"] == gg["id"]:
         perm.append(guild["id"])
      else:
        pass
    guild_db = get_guild_find(server_id)
    if guild_db is None:
       return redirect(url_for('guilds'))
    if server_id in checks:
       sts = True
       checks.remove(server_id)
    else:
      sts = False  
    if guild["id"] in perm:   
     try:
       user = api.get_info(session.get('token'))
       date = get_date_guild(server_id)
       channels = get_guild_channels_type(server_id, 0)

     except requests.exceptions.HTTPError:return redirect("/")
   
     return render_template('dashboard_suggestion.html', guild=guild, sts=sts,channels=channels, guild_db=guild_db,user=user, date=date, title="Asuna - "+guild["name"])

###########################################
# get dados do auto role
###########################################

@app.route('/dashboard/<int:server_id>/suggestion/update', methods=['POST'])
def update_suggestion(server_id):
    guild_db = get_guild_find(server_id)
    if request.form["btn"] == "atualizar":
        suggestion_id = request.form.get('channel_id')
        if not server_id in checks:
           checks.append(server_id)
        else:
          pass         
        get_guild_update_func(server_id, "suggestion_channel", suggestion_id)       
        return redirect(url_for('dashboard_suggestion', server_id=server_id))
    if request.form["btn"] == "resetar":
       get_guild_update_two(ids, "suggestion_channel",None, "suggestion_status",suggestion_id)
       return redirect(url_for('dashboard_suggestion', server_id=server_id))
    if request.form["btn"] == "desligar":
       get_guild_update_func(server_id, "suggestion_status", False)       
       return redirect(url_for('dashboard_suggestion', server_id=server_id))
    if request.form["btn"] == "ligar":
       get_guild_update_func(server_id, "suggestion_status", True)       
       return redirect(url_for('dashboard_suggestion', server_id=server_id))

###########################################
# modulo sugestão 
###########################################

@app.route('/dashboard/<int:server_id>/membercount')
def dashboard_membercount(server_id):
    guild = get_guild(server_id)
    if guild is None:
       return redirect(get_invite_link(config["id_bot"], server_id, quote(config["redirect_2"])))  
    servers = api.get_guilds(session.get('token'))
    guilds = list(filter(lambda g: (g['owner'] is True) or bool((int(g['permissions']) >> 5) & 1),servers))
    perm = []
    for gg in guilds:
      if guild["id"] == gg["id"]:
         perm.append(guild["id"])
      else:
        pass
    guild_db = get_guild_find(server_id)
    if guild_db is None:
       return redirect(url_for('guilds'))
    if server_id in checks:
       sts = True
       checks.remove(server_id)
    else:
      sts = False  
    if guild["id"] in perm:   
     try:
       user = api.get_info(session.get('token'))
       date = get_date_guild(server_id)
       channels = get_guild_channels_type(server_id, 0)

     except requests.exceptions.HTTPError:return redirect("/")
   
     return render_template('dashboard_membercount.html', guild=guild, sts=sts,channels=channels, guild_db=guild_db,user=user, date=date, title="Asuna - "+guild["name"])

###########################################
# get dados do auto role
###########################################

@app.route('/dashboard/<int:server_id>/membercount/update', methods=['POST'])
def update_membercount(server_id):
    guild_db = get_guild_find(server_id)
    if request.form["btn"] == "atualizar":
        membercount_id = request.form.get('channel_id')
        if not server_id in checks:
           checks.append(server_id)
        else:
          pass         
        get_guild_update_func(server_id, "membercount_channel", membercount_id)       
        return redirect(url_for('dashboard_membercount', server_id=server_id))
    if request.form["btn"] == "resetar":
       get_guild_update_membercount(server_id, None, None, None, True)
       return redirect(url_for('dashboard_membercount', server_id=server_id))
    if request.form["btn"] == "desligar":
       get_guild_update_func(server_id, "membercount_status", False)       
       return redirect(url_for('dashboard_membercount', server_id=server_id))
    if request.form["btn"] == "ligar":
       get_guild_update_func(server_id, "membercount_status", True)       
       return redirect(url_for('dashboard_membercount', server_id=server_id))

###########################################
# deslogar a conta do site
###########################################

@app.route('/logout')
def logout():
  del session['token']
  return redirect('/')

###########################################
# main e porta
##########################################

if __name__ == '__main__':
  app.run(debug=True,port=8000)
