import base64
import time
import re
import random
from datetime import datetime
import threading

import config
import login
import public
import logins
try:
	import pokemon_pb2
	import logic
	import stops
	import dirty
	import api
	config.pub=False
except:
	import public_proto_pb2
	config.pub=True

def get_acces_token():
	if config.google:
		print '[!] Using google as login..'
		google_data= login.login_google(logins.google_mail,logins.google_password)
		if google_data is not None:
			access_token=google_data['id_token']
			ltype='google'
		else:
			access_token=None
	else:
		print '[!] I am a poketrainer..'
		access_token= login.login_pokemon(logins.pokemon_username,logins.pokemon_password)
		ltype='ptc'
	return access_token,ltype
	
def main():
	access_token,ltype=get_acces_token()
	if access_token is not None:
		print '[!] using:',config.pub
		if config.pub:
			public.start_work(access_token,ltype)
		else:
			dirty.start_private_show(access_token,ltype)
	else:
		print '[-] access_token bad'
	
if __name__ == '__main__':
	main()