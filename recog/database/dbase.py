import firebase_admin
import os
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

path = f"{os.getcwd()}\\recog\\secreteKey\\pyrebaserealtimedb-34825-firebase-adminsdk-lalsz-aba7d939e7.json"
#print(path)

class databs:
    cred_obj = None
    def __init__(self):
        cred_obj = credentials.Certificate(path)
        firebase_admin.initialize_app(cred_obj)
        self.db = firestore.client()
    def updatelocation(self,lat,long):
        print(f"Latitude - {lat}.\nLongitude - {long}.")
        self.db.collection('VechicleData').document("location").update({'lat':f'{lat}','long':f'{long}',"time":firestore.SERVER_TIMESTAMP})
    
        
