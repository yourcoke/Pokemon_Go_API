import logic
import api
import time
import pokemon_pb2
import location
import config

def start_private_show(access_token,ltype,loc):
	location.set_location(loc)
	print '[+] Token:',access_token[:40]+'...'
	prot1=logic.gen_first_data(access_token,ltype)
	local_ses=api.get_rpc_server(access_token,prot1)
	new_rcp_point='https://%s/rpc'%(local_ses.rpc_server,)
	while(True):
		work_stop(local_ses,new_rcp_point)
	
def walk_random():
	COORDS_LATITUDE, COORDS_LONGITUDE, COORDS_ALTITUDE=location.get_location_coords()
	COORDS_LATITUDE=location.l2f(COORDS_LATITUDE)
	COORDS_LONGITUDE=location.l2f(COORDS_LONGITUDE)
	COORDS_ALTITUDE=location.l2f(COORDS_ALTITUDE)
	COORDS_LATITUDE=COORDS_LATITUDE+config.steps
	COORDS_LONGITUDE=COORDS_LONGITUDE+config.steps
	location.set_location_coords(COORDS_LATITUDE, COORDS_LONGITUDE, COORDS_ALTITUDE)
	
def work_stop(local_ses,new_rcp_point):
	proto_all=logic.all_stops(local_ses)
	all_stops=api.use_api(new_rcp_point,proto_all)
	maps = pokemon_pb2.maps()
	maps.ParseFromString(all_stops)
	data_list=location.get_near(maps)
	data_list = sorted(data_list, key = lambda x: x[1])
	if len(data_list)>0:
		print '[+] found: %s Pokestops within %s m'%(len(data_list),config.distance,)
		if local_ses is not None and data_list is not None:
			print '[+] starting show'
			for t in data_list:
				print '[!] farming pokestop..'
				work_with_stops(t,local_ses.ses,new_rcp_point)
	else:
		walk_random()
		work_stop(local_ses,new_rcp_point)
		
def work_with_stops(current_stop,ses,new_rcp_point):
	Kinder= logic.gen_stop_data(ses,current_stop)
	tmp_api=api.use_api(new_rcp_point,Kinder)
	try:
		if tmp_api is not None:
			map = pokemon_pb2.map()
			map.ParseFromString(tmp_api)
			st= map.sess[0].status
			if st==4:
				print "[!] +%s"%map.sess[0].amt
			elif st==3:
				print "[!] used"
			elif st==2:
				print "[!] charging"
			elif st==1:
				print "[!] teleport.."
				time.sleep(14)
				work_with_stops(current_stop,ses,new_rcp_point)
			else:
				print "[?]:",st
		else:
			print '[-] tmp_api empty'
	except:
		print '[-] error work_with_stops'