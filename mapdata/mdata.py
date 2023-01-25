import random
import geocoder

class location: 
    def lat(self):
        lat_ = f"{random.randint(-90,90)}.{random.randint(0,10**6)}"
        return lat_
    def long(self):
        long_ = f"{random.randint(-90,90)}.{random.randint(0,10**6)}"
        return long_

class iplocation:
    def __init__(self):
        g = geocoder.ip('me')
        self._lat,self._long  = g.latlng[0],g.latlng[1]
    def lat(self):
        return self.lat
    def long(self):
        return self.long

