import pokemon_pb2
import base64
import struct
import config
from math import radians, cos, sin, asin, sqrt
from geopy.distance import vincenty
from geopy.geocoders import GoogleV3
	
COORDS_LATITUDE = 0
COORDS_LONGITUDE = 0
COORDS_ALTITUDE = 0
FLOAT_LAT = 0
FLOAT_LONG = 0
	
def get_location_coords():
	return (COORDS_LATITUDE, COORDS_LONGITUDE, COORDS_ALTITUDE)
	
def set_location(location_name):
	geolocator = GoogleV3()
	loc = geolocator.geocode(location_name)

	print('[!] Your given location: {}'.format(loc.address.encode('utf-8')))
	set_location_coords(loc.latitude, loc.longitude, loc.altitude)
	
def set_location_coords(lat, long, alt):
	print('[!] lat/long/alt: {} {} {}'.format(lat, long, alt))
	global COORDS_LATITUDE, COORDS_LONGITUDE, COORDS_ALTITUDE
	global FLOAT_LAT, FLOAT_LONG
	FLOAT_LAT = lat
	FLOAT_LONG = long
	COORDS_LATITUDE = f2i(lat)
	COORDS_LONGITUDE = f2i(long)
	COORDS_ALTITUDE = f2i(alt)
	
def i2f(int):
	return struct.unpack('<Q', struct.pack('<d', int))[0]

def f2h(float):
	return hex(struct.unpack('<Q', struct.pack('<d', float))[0])

def f2i(float):
	return struct.unpack('<Q', struct.pack('<d', float))[0]
	
def l2f(float):
	return struct.unpack('d', struct.pack('Q', int(bin(float), 0)))[0]
 
def h2f(hex):
	return struct.unpack('<d', struct.pack('<Q', int(hex,16)))[0]
	
def get_near(map):
	ms=[]
	for cell in [map]:
		for block in cell.b:
			for obj in block.c:
				for stop in obj.s:
					if is_near(stop.lat,stop.lon,COORDS_LATITUDE,COORDS_LONGITUDE):
						ms.append((stop.name,stop.lat,stop.lon))
	return ms
	
def is_near(locx,locy,myx,myy):
	tmp1 = (l2f(locx), l2f(locy))
	tmp2 = (l2f(myx), l2f(myy))
	res=vincenty(tmp1, tmp2).meters
	return res<config.distance