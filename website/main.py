from flask import Flask, render_template, request, session, redirect, jsonify
from urllib.parse import quote
import requests, api, time
from configs.config import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config["secret_key"]


@app.route('/')
def index():
	url = str(config["url_authentication"]).format(config["id_bot"], quote(config["redirect"]), quote(config["scopes"]))
	token = session.get('token')
	return render_template('index.html', url=url, token=token)

@app.route('/callback')
def response():
	code = request.args.get('code')

	try:
		res = api.exchange_code(code)
	except requests.exceptions.HTTPError:
		return "Token invalido!"

	session['token'] = res['access_token']
	session['scopes'] = str(config["scopes"]).split(" ")
	return redirect("/me")

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
	app.run(debug=True,port=port)
