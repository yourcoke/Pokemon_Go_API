import base64
import time
import re
import config
import login
try:
	import pokemon_pb2
	import pokemon
except:
	print 'missing files.. ask Mila432..'
	exit()
try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

def get_api(access_token):
	try:
		r=config.s.post(config.api_url,data=base64.b64decode(pokemon.generate_login(access_token)),verify=False)
		pok = pokemon_pb2.Login()
		pok.ParseFromString(r.content)
		return 'https://'+pok.api_point+'/rpc'
	except:
		print '[-] server offline'
		time.sleep(3)
		get_api(access_token)
		
def use_api(target_api,access_token):
	if config.debug:
		print '[!] using api:',target_api
	r=config.s.post(target_api,data=base64.b64decode(pokemon.generate_login(access_token)),verify=False)
	return r.content
	
def main():
	if config.google:
		print '[!] Using google as login..'
		google_data= login.login_google('mygoogle@gmail.com','superstrongpassword')
		access_token=google_data['id_token']
	else:
		print '[!] I am a poketrainer..'
		access_token= login.login_pokemon('login_pokemon','superstrongpassword')
	if access_token is not None:
		print '[+] Token:',access_token[:40]+'...'
		new_api= get_api(access_token)
		if 'Milaly432' in use_api(new_api,access_token):
			print '[+] logged in'
		else:
			print '[-] protobuf sux..'
	
if __name__ == '__main__':
	main()