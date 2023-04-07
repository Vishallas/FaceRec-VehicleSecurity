import firebase_admin
import os
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import time

path = f"{os.getcwd()}\\recog\\secreteKey\\pyrebaserealtimedb-34825-firebase-adminsdk-lalsz-aba7d939e7.json"
#print(path)

class DatabaseHelper:
    cred_obj = None
    def __init__(self):
        cred_obj = credentials.Certificate(path)
        firebase_admin.initialize_app(cred_obj, {'storageBucket': 'pyrebaserealtimedb-34825.appspot.com'})
        self.db = firestore.client()
        # initialize_app(cred_obj, {'storageBucket': 'pyrebaserealtimedb-34825.appspot.com'})
        # Put your local file path 
        self.fileName = f"{os.getcwd()}\\unauthorthorized\\k.jpg"
        self.bucket = storage.bucket()
        self.imgNo = int(self.db.collection('VechicleData').document("location").get().to_dict()['imgNo'])

    def updatelocation(self,lat,long):
        print(f"Latitude - {lat}.\nLongitude - {long}.\n")
        self.db.collection('VechicleData').document("location").update({'lat':f'{lat}','long':f'{long}',"time":firestore.SERVER_TIMESTAMP})
    
    def sendImage(self):
        self.imgNo += 1
        blob = self.bucket.blob(f"unAurth/UnaurthoPerson{self.imgNo}")
        blob.upload_from_filename(self.fileName)
        blob.make_public()
        time.sleep(2)
        return blob.public_url 

    def linkimage(self,imagelink):
        print("link :",imagelink)
        # self.db.collection('VechicleData').document("imagedata").update({'imgNo':{str(self.imgNo)},'link':f'{imagelink}'})
        self.db.collection('VechicleData').document("location").update({'image_url':f'{imagelink}','imgNo':f'{str(self.imgNo)}'})
    
    def testin(self,imgNo):
        self.imgNo = imgNo
        self.db.collection('VechicleData').document("location").update({'imgNo':f'{str(self.imgNo)}'})

if __name__ == "__main__":
    d = DatabaseHelper()
    d.testin(1)
    print(d.imgNo)