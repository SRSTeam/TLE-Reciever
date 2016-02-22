from requests import session
import json, ConfigParser

config = ConfigParser.ConfigParser()
config.read("config.ini")

payload = {
    'action': 'login',
    'identity': config.get("SpaceTrack","Username"),
    'password': config.get("SpaceTrack","Password")
}

class Satellite:
    def __init__(self, jsonData):
        self.id = jsonData.get("NORAD_CAT_ID")
        self.name = jsonData.get("OBJECT_NAME")
        self.perigee = float(jsonData.get("PERIGEE"))
    def __str__(self):
        output = "NORAD Catalog ID:\t" + self.id + "\n"
        output += "Satellite Name:\t" + self.name + "\n"
        output += "Perigee:\t" + str(self.perigee) + " km"
        return output

data = None
with session() as c:
    c.post('https://www.space-track.org/ajaxauth/login', data=payload)
    response = c.get('https://www.space-track.org/basicspacedata/query/class/decay/DECAY_EPOCH/%3E2016-02-13%200:00:00/orderby/DECAY_EPOCH%20asc/limit/20/metadata/false')
    data = json.loads(response.text)
    decayCatalogIDs = []
    for line in data:
        decayCatalogIDs.append(line.get("NORAD_CAT_ID"))
    catalogQuery = ",".join(decayCatalogIDs)

    response = c.get('https://www.space-track.org/basicspacedata/query/class/tle_latest/NORAD_CAT_ID/'+catalogQuery+'/ORDINAL/1/EPOCH/%3Enow-30/MEAN_MOTION/%3E11.25/ECCENTRICITY/%3C0.25/orderby/PERIGEE%20asc/limit/100/metadata/false')
    data = json.loads(response.text)
    satellites = []
    for sat in data:
        satellites.append(Satellite(sat))
        print satellites[-1]
        print
