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
	import api
	config.pub=False
except:
	import public_proto_pb2
	config.pub=True
	
def generate_random_long():
	return long(random.choice(range(0,10000000)))
		
def work_with_stops(current_stop,ses,new_rcp_point):
	Kinder= logic.gen_stop_data(ses,current_stop)
	api.use_api(new_rcp_point,Kinder)
	time.sleep(1)
	
def small_show(t,access_token):
	print '[!] farming pokestop..'
	prot1=logic.gen_first_data(access_token)
	sid= api.get_rpc_server(access_token,prot1)
	if sid is not None and sid.rpc_server is not None:
		new_rcp_point='https://%s/rpc'%(sid.rpc_server,)
		work_with_stops(t,sid.ses,new_rcp_point)
	else:
		small_show(t,access_token)
		
def start_private_show(access_token,ltype):
	print '[+] Token:',access_token[:40]+'...'
	for t in stops.get_static():
		t = threading.Thread(target=small_show, args=(t,access_token,))
		t.start()
		#small_show(t,access_token)
	#prot1=logic.gen_first_data(access_token)
	#sid= api.get_rpc_server(access_token,prot1)
	#new_rcp_point='https://%s/rpc'%(sid.rpc_server,)
	#login_data=api.use_api(new_rcp_point,prot1)
	#if sid is not None:
	#	for t in stops.get_static():
	#		print '[!] farming pokestop..'
	#		work_with_stops(t,sid.ses,new_rcp_point)
			#walking=logic.simulate_walking(ses,t)
			#api.use_api(new_rcp_point,walking)
			#time.sleep(1)
			#Kinder_pre=logic.gen_stop_data_pre(ses,t)
			#api.use_api(new_rcp_point,Kinder_pre)
			#time.sleep(1)

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
			start_private_show(access_token,ltype)
	else:
		print '[-] access_token bad'
	
if __name__ == '__main__':
	main()