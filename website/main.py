from flask import Flask, render_template, request, session, redirect, jsonify
from urllib.parse import quote
import requests, api, time, json
from configs.config import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config["secret_key"]


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

@app.route('/me')
def me():
	if session.get('token') is None:
		return redirect("/")

	try:
		user = api.get_info(session.get('token'))
	except requests.exceptions.HTTPError:
		return "Token invalido!"

	return jsonify(user)

@app.route('/guilds')
def guilds():
	if session.get('token') is None:
		return redirect('/')	

	try:
		servers = api.get_guilds(session.get('token'))
	except requests.exceptions.HTTPError:
		return "Token invalido!"
	
	return jsonify(servers)



@app.route('/logout')
def logout():

	del session['token']
	return redirect('/')

if __name__ == '__main__':
	app.run(debug=True,port=8000)
