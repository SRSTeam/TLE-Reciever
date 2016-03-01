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
        self.json = jsonData
        self.id = jsonData.get("NORAD_CAT_ID")
        self.name = jsonData.get("OBJECT_NAME")
        self.perigee = float(jsonData.get("PERIGEE"))
        self.apogee = float(jsonData.get("APOGEE"))
        self.object_type = jsonData.get("OBJECT_TYPE")
        self.rcs_size = jsonData.get("RCS_SIZE")
        # self.decay = jsonData.get("DECAY")
    def __str__(self):
        output = "NORAD Catalog ID:\t" + self.id + "\n"
        output += "Satellite Name:\t" + self.name + "\n"
        output += "Object Type:\t" + self.object_type + "\n"
        if self.rcs_size != None:
            output += "RCS Size:\t" + str(self.rcs_size) + "\n"
        output += "Perigee:\t" + str(self.perigee) + " km\n"
        output += "Perigee:\t" + str(self.perigee*0.621371192) + "mi\n"
        output += "Apogee:\t" + str(self.apogee) + " km\n"
        output += "Apogee:\t" + str(self.apogee*0.621371192) + "mi\n"
        # output += "Decay:\t" + self.decay
        return output

data = None
with session() as c:
    c.post('https://www.space-track.org/ajaxauth/login', data=payload)
    # response = c.get('https://www.space-track.org/basicspacedata/query/class/decay/DECAY_EPOCH/%3Enow/orderby/DECAY_EPOCH%20asc/metadata/false') # RCS_SIZE/%3C%3ESMALL/
    # data = json.loads(response.text)
    # decayCatalogIDs = []
    # for line in data:
    #     if(not line.get("OBJECT_NAME").__contains__("DEB")):
    #         decayCatalogIDs.append(line.get("NORAD_CAT_ID"))  
    # catalogQuery = ",".join(decayCatalogIDs)

    response = c.get('https://www.space-track.org/basicspacedata/query/class/satcat/APOGEE/%3C1000/PERIGEE/%3C300/RCS_SIZE/%3C%3ESMALL/OBJECT_TYPE/PAYLOAD/CURRENT/Y/orderby/DECAY%20asc/limit/100/metadata/false')
    # response = c.get('https://www.space-track.org/basicspacedata/query/class/satcat/CURRENT/Y/PERIGEE/%3C200/NORAD_CAT_ID/'+catalogQuery+'/orderby/PERIGEE%20asc/metadata/false')
    data = json.loads(response.text)
    satellites = []
    for sat in data:
        if(sat.get("DECAY") == None):
            satellites.append(Satellite(sat))
            print satellites[-1]
            print
    # print satellites[-1].json
