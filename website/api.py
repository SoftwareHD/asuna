import requests
from configs.config import config

base_url = config["url_api"]

def _getheaders(token):
	return {'Authorization': 'Bearer {}'.format(token)}

def exchange_code(code):
	data = {
		'client_id': config["id_bot"],
		'client_secret': config["secret"],
		'grant_type': 'authorization_code',
		'code': code,
		'redirect_uri': config["redirect"],
		'scope': config["scopes"]
	}
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	r = requests.post('{}/oauth2/token'.format(base_url), data, headers)
	r.raise_for_status()
	return r.json()

def get_info(token):
	headers = _getheaders(token)
	r = requests.get('{}/users/@me'.format(base_url), headers=headers)
	r.raise_for_status()
	return r.json()

def get_guilds(token):
	headers = _getheaders(token)
	r = requests.get('{}/users/@me/guilds'.format(base_url), headers=headers)
	r.raise_for_status()
	return r.json()

def get_connections(token):
	headers = _getheaders(token)

	r = requests.get('{}/users/@me/connections'.format(base_url), headers=headers)
	r.raise_for_status()
	return r.json()
