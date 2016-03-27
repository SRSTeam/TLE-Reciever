from requests import session
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
import json, ConfigParser
from datetime import datetime

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

class satcatData:
    def __init__(self, jsonData):
        self.norad_cat_id = jsonData.get("NORAD_CAT_ID")
        self.json = jsonData
    def get(self, arg):
        return self.json.get(arg)

class Satellite:
    def __init__(self, satcatData, tleData):
        self.satcatData = satcatData
        self.tleData = tleData
        self.sgp4Data = twoline2rv(tleData.get("TLE_LINE1"),tleData.get("TLE_LINE2"),wgs72)
        self.id = satcatData.get("NORAD_CAT_ID")
        self.name = satcatData.get("OBJECT_NAME")
        self.perigee = float(tleData.get("PERIGEE"))
        self.apogee = float(tleData.get("APOGEE"))
        self.object_type = satcatData.get("OBJECT_TYPE")
    def __str__(self):
        output = "NORAD Catalog ID:\t" + self.id + "\n"
        output += "Satellite Name:\t" + self.name + "\n"
        output += "Object Type:\t" + self.object_type + "\n"
        output += "Perigee:\t" + str(self.perigee) + " km\n"
        output += "Perigee:\t" + str(self.perigee*0.621371192) + "mi\n"
        output += "Apogee:\t" + str(self.apogee) + " km\n"
        output += "Apogee:\t" + str(self.apogee*0.621371192) + "mi\n"
        output += "Size:\t" + self.satcatData.get("RCS_SIZE")
        return output

    # Returns the location of the satellite in ECI form
    def getLoc(self):
        dt = datetime.now()
        return self.sgp4Data.propagate(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second)[0]

data = None
with session() as c:
    c.post('https://www.space-track.org/ajaxauth/login', data=payload)

    # Generates Satcat database of desired satellites
    satcatJson = json.loads(c.get('https://www.space-track.org/basicspacedata/query/class/satcat/PERIGEE/%3C300/RCS_SIZE/%3C%3ESMALL/OBJECT_TYPE/PAYLOAD/CURRENT/Y/orderby/DECAY%20asc/limit/100/metadata/false').text)
    satcatMap = {}
    for sat in satcatJson:
        if(sat.get("DECAY") == None):
            satcatMap[sat.get('NORAD_CAT_ID')] = satcatData(sat)

    # Generates TLE database of desired satellites
    tleJson = json.loads(c.get('https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/EPOCH/>now-30/MEAN_MOTION/>11.25/ECCENTRICITY/<0.25/OBJECT_TYPE/payload/orderby/NORAD_CAT_ID/format/json').text)
    tleMap = {}
    for t in tleJson:
        tleMap[t.get("NORAD_CAT_ID")] = tleData(t)

    # Combines TLE and Satcat databases into satellite class
    satellites = []
    for sat in satcatMap:
        if sat in tleMap:
            satellites.append(Satellite(satcatMap[sat],tleMap[sat]))

    # Sorts satellites by perigee
    satellites = sorted(satellites, key=lambda x:x.perigee)
    for sat in satellites:
        print sat
        print

    # Logout
    c.post('https://www.space-track.org/ajaxauth/logout')
