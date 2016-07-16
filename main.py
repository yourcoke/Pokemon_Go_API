import base64
import time
import re
from random import randint
import random


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
	
#https://github.com/tejado
def start_work(access_token,ltype):
	print '[+] Token:',access_token[:40]+'...'
	api_endpoint =public.get_api_endpoint(access_token,ltype)
	if api_endpoint is not None:
		print('[+] Received API endpoint: {}'.format(api_endpoint))
		profile = public.get_profile(api_endpoint, access_token)
		if profile is not None:
			print('[+] Login successful')

			profile = profile.payload[0].profile
			print('[+] Username: {}'.format(profile.username))

			creation_time = datetime.fromtimestamp(int(profile.creation_time)/1000)
			print('[+] You are playing Pokemon Go since: {}'.format(
				creation_time.strftime('%Y-%m-%d %H:%M:%S'),
			))
			print('[+] Poke Storage: {}'.format(profile.poke_storage))
			print('[+] Item Storage: {}'.format(profile.item_storage))
			for curr in profile.currency:
				print('[+] {}: {}'.format(curr.type, curr.amount))
		else:
			print('[-] Ooops...')
	else:
		print('[-] RPC server offline')
		exit()
		
def start_private_show(access_token,ltype):
	print '[+] Token:',access_token[:40]+'...'
	prot1=logic.gen_first_data(access_token)
	new_api= api.get_rpc_server(access_token,prot1)
	login_data=api.use_api(new_api,prot1)
	cis= api.get_session(login_data)
	#for t in stops.get_static():
		#print '[!] farming pokestop..'
		#walking=logic.simulate_walking(cis,t)
		#use_api(new_api,walking)
		#time.sleep(1)
		#Kinder_pre=logic.gen_stop_data_pre(cis,t)
		#use_api(new_api,Kinder_pre)
		#Kinder= logic.gen_stop_data(cis,t)
		#api.use_api(new_api,Kinder)
		#time.sleep(3)
	
def main():
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
	if access_token is not None:
		if config.pub:
			start_work(access_token,ltype)
		else:
			start_private_show(access_token,ltype)
	else:
		print '[-] access_token bad'
	
if __name__ == '__main__':
	main()