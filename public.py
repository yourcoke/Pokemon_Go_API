import public_proto_pb2
import config

def api_req(api_endpoint, access_token, req,ltype):
	try:
		p_req = public_proto_pb2.RequestEnvelop()
		p_req.unknown1 = 2
		p_req.rpc_id = 8145806132888207460

		p_req.requests.MergeFrom(req)

		p_req.latitude=0
		p_req.longitude=0
		p_req.altitude = 0

		p_req.unknown12 = 989
		p_req.auth.provider = ltype
		p_req.auth.token.contents = access_token
		p_req.auth.token.unknown13 = 59
		protobuf = p_req.SerializeToString()

		r = config.SESSION.post(api_endpoint, data=protobuf, verify=False,timeout=3)

		p_ret = public_proto_pb2.ResponseEnvelop()
		p_ret.ParseFromString(r.content)
		return p_ret
	except:
		print '[-] error in api_req'
		return None
	#except Exception,e:
	#	if config.DEBUG:
	#		print(e)
	#	return None


def get_api_endpoint(access_token,ltype):
	try:
		req = public_proto_pb2.RequestEnvelop()
		req1 = req.requests.add()
		req1.type = 2
		req2 = req.requests.add()
		req2.type = 126
		req3 = req.requests.add()
		req3.type = 4
		req4 = req.requests.add()
		req4.type = 129
		req5 = req.requests.add()
		req5.type = 5
		req5.message.unknown4 = "4a2e9bc330dae60e7b74fc85b98868ab4700802e"
		p_ret = api_req(config.API_URL, access_token, req.requests,ltype)
		return ('https://%s/rpc' % p_ret.api_url)
	except:
		print '[-] error in get_api_endpoint'
		return None
		
def get_profile(api_endpoint, access_token):
	try:
		req = pokemon_pb2.RequestEnvelop()
		req1 = req.requests.add()
		req1.type = 2
		return api_req(api_endpoint, access_token, req.requests)
	except:
		print '[-] error in get_profile'
		return None