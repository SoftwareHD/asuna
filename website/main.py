###########################################
# Lista de imports
###########################################

from flask import Flask, render_template, request, session, redirect, jsonify
from urllib.parse import quote
import requests, api, time, json
from configs.config import *
from configs.get import *

###########################################
# Leitura de dados (config, token)
###########################################

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
# pagina da guild
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
	 
     return render_template('dashboard.html', guild=guild,user=user, date=date, title="Asuna - "+guild["name"])



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
