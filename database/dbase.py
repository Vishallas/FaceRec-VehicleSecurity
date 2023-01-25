import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

from config import fbase_key

class databs:
    cred_obj = None
    def __init__(self):
        cred_obj = credentials.Certificate(fbase_key)
        firebase_admin.initialize_app(cred_obj)
        self.db = firestore.client()
    def updatelocation(self,lat,long):
        print(f"Latitude - {lat}.\nLongitude - {long}.")
        self.db.collection('VechicleData').document("location").update({'lat':f'{lat}','long':f'{long}'})

