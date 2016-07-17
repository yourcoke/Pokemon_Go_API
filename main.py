import base64
import time
import re
import random
from datetime import datetime
import threading
import argparse
import os
import platform
import sys

import config
import login
import public
try:
	import pokemon_pb2
	import logic
	import dirty
	import stops
	import api
	config.pub=False
except:
	import public_proto_pb2
	config.pub=True

def get_acces_token(usr,pws,type):
	access_token=None
	ltype=None
	if 'goo' in type:
		print '[!] Using google as login..'
		google_data= login.login_google(usr,pws)
		if google_data is not None:
			access_token=google_data['id_token']
			ltype='google'
		else:
			access_token=None
	else:
		print '[!] I am a poketrainer..'
		access_token= login.login_pokemon(usr,pws)
		ltype='ptc'
	return access_token,ltype
	
def main():
	if 'nux' not in platform.system():
		os.system("title Pokemon GO API Python")
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--username", help="Login", required=True)
	parser.add_argument("-p", "--password", help="Password", required=True)
	parser.add_argument("-t", "--type", help="Google/PTC", required=True)
	args = parser.parse_args()
	if 'ptc' in args.type.lower() or 'goo' in args.type.lower():
		access_token,ltype=get_acces_token(args.username,args.password,args.type.lower())
		if access_token is not None:
			print '[!] using:',config.pub
			if config.pub:
				public.start_work(access_token,ltype)
			else:
				dirty.start_private_show(access_token,ltype)
		else:
			print '[-] access_token bad'
	else:
		print '[!] used type "%s" only Google or PTC valid'%(args.type.lower())
	
if __name__ == '__main__':
	main()