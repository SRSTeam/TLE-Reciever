from requests import session
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
import json, ConfigParser
from datetime import datetime
import math
##import sgp4lib

config = ConfigParser.ConfigParser()
config.read("config.ini")

payload = {
    'action': 'login',
    'identity': config.get("SpaceTrack","Username"),
    'password': config.get("SpaceTrack","Password")
}
class tleData:
    def __init__(self, jsonData):
        self.norad_cat_id = jsonData.get("NORAD_CAT_ID")
        self.json = jsonData
    def get(self, arg):
        return self.json.get(arg)

def getVp(tle):
    eccent= float(tle.get("ECCENTRICITY"))
    nuprime=float(tle.get("MEAN_MOTION"))*2.0*math.pi/24.0/60.0/60.0
    gravitationalp=3.986e5
    a=float(tle.get("SEMIMAJOR_AXIS"))
    p=a*(1-eccent**2)
    h=math.sqrt(p*gravitationalp)
    rp=float(tle.get("PERIGEE"))+6371
    Vp=h/rp
    return Vp

data = None
with session() as c:
    c.post('https://www.space-track.org/ajaxauth/login', data=payload)

    # Generates TLE database of desired satellites
    tleJson = json.loads(c.get('https://www.space-track.org/basicspacedata/query/class/tle_latest/NORAD_CAT_ID/38744/orderby/ORDINAL asc/limit/1/metadata/false').text)
    tleMap = {}
    for t in tleJson:
        tleMap[t.get("NORAD_CAT_ID")] = tleData(t)

    print getVp(tleMap["38744"])
    
    # Logout
    c.post('https://www.space-track.org/ajaxauth/logout')
