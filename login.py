# -*- coding: utf-8 -*-
import config
import json
import re
from collections import OrderedDict
from gpsoauth import perform_master_login, perform_oauth

AID = '9774d56d682e549c'
SVC= 'audience:server:client_id:848232511240-7so421jotr2609rmqakceuu1luuq0ptb.apps.googleusercontent.com'
APP = 'com.nianticlabs.pokemongo'
CSG = '321187995bc7cdc2b5fc91b11a96e2baa8602c62'

def login_pokemon(user,passw):
	print '[!] doing login for:',user
	try:
		head={'User-Agent':'niantic'}
		r=config.s.get(config.login_url,headers=head)
		jdata=json.loads(r.content)
			
		new_url= r.history[0].headers['Location']
		data = OrderedDict([('lt', jdata['lt']), ('execution',jdata['execution']), ('_eventId', 'submit'), ('username', user), ('password', passw)])
		
		r1=config.s.post(new_url,data=data,headers=head,allow_redirects=False)
		raw_ticket= r1.headers['Location']
		if 'errors' in r1.content:
			print json.loads(r1.content)['errors'][0].replace('&#039;','\'')
			return None
		ticket=re.sub('.*ticket=','',raw_ticket)

		data1 = OrderedDict([('client_id', 'mobile-app_pokemon-go'), ('redirect_uri','https://www.nianticlabs.com/pokemongo/error'), ('client_secret', 'w8ScCUXJQc6kXKw8FiOhd8Fixzht18Dq3PEVkUCP5ZPxtgyWsbTvWHFLm2wNY0JR'), ('grant_type', 'refresh_token'), ('code', ticket)])
		
		r2=config.s.post(config.login_oauth,data=data1)
		access_token=re.sub('.*en=','',r2.content)
		access_token=re.sub('.com.*','.com',access_token)
		return access_token
	except:
		print '[-] pokemon attacking the login server'
		return None
	
def login_google(email,passw):
	print('[!] Google login for: {}'.format(email))

	r1 = perform_master_login(email, passw, AID)
	r2 = perform_oauth(email, r1.get('Token', ''), AID, SVC, APP, CSG)

	return r2