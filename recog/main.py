import os
import cv2
import face_recognition
import numpy as np
import pickle
import time

from webcamvideostream import WebcamVideoStream
from fps import FPS

#custom libraries
from mapdata import mdata
from database import dbase


import internetConnection

db=None
mapd=None
mapip = None

if(internetConnection.isConnected()):
    mapd = mdata.Location()
    mapip = mdata.IPLocation()
    db = dbase.DatabaseHelper()
    print("Internet Connected")

ct = 10
factor = 2
names = list()


# imagedir = 'S:\\Projects\\recognize_me\\images'
# encodpath = 'S:\\Projects\\recognize_me\\encodes'


imagedir = f'{os.getcwd()}\\images'
encodpath = f'{os.getcwd()}\\encodes'

#print(imagedir,encodpath)

path = os.listdir(imagedir)
path.remove(".gitkeep")


stop = False
unAurAccess = False


cam = cv2.VideoCapture(0)


def sendMapLoc():
    global db,mapd,mapip
    disconnected = False

    if(internetConnection.isConnected()):
        print("Image uploading....")
        imagelink = db.sendImage()
        db.linkimage(imagelink)
        print("Image uploaded....")
        while(internetConnection.isConnected()):
            # print("\nInternet reconnected")
            print("\nThe data is sending....\n")
            # db.updatelocation(mapd.lat(),mapd.long()) # random loc
            db.updatelocation(mapip.lat(),mapip.long())
            time.sleep(3)
    else:
        print("\nInternet is not connected.\n\nThe data is not sent to the database....\n")
    return
        # if(internetConnection.isConnected()):
        #     if(disconnected):
        #         print("\nInternet reconnected")
        #         print("\nThe data is sending....\n")
        #     #db.updatelocation(mapip.lat(),mapip.long()) # by using ip
        #         if(db):
        #             db.updatelocation(mapd.lat(),mapd.long()) # random loc
        #             time.sleep(3)
        #         else:
        #             db=dbase.DatabaseHelper()
        #             mapd = mdata.Location()
        #             mapip = mdata.IPLocation()
        #         disconnected=False
        # else:
        #     print("\nTrying to reconnect...")
        #     disconnected=True
        #     time.sleep(3)


def sendOnce():
    if(internetConnection.isConnected()):
        #db.updatelocation(mapd.lat(),mapd.long())
        db.updatelocation(mapip.lat(),mapip.long())
    else:
        print("\nInternet is not connected.\n\nThe data is not sent to the database....\n")

    # global db,mapd,mapip
    # dataSent=False
    # while(not dataSent):
    #     if(internetConnection.isConnected()):
    #         if(db):
    #             db.updatelocation(mapd.lat(),mapd.long()) # random loc
    #             dataSent=True 
    #         else:
    #             db=dbase.DatabaseHelper()
    #             mapd = mdata.Location()
    #             mapip = mdata.IPLocation()
    #         #db.updatelocation(mapip.lat(),mapip.long()) # by using ip
    #     elif(not dataSent): 
    #         print("Trying to reconnect...")
    #         time.sleep(3)
    

knownFaceEncodings = pickle.load(open(f'{encodpath}\\encode.pickle','rb'))
names = pickle.load(open(f'{encodpath}\\name.pickle','rb'))
print(names)


def video():
    global ct
    face_is_match = False
    v1=WebcamVideoStream(src=0).start()
    #fps = FPS().start()
    while True:
        #success,frame = cam.read()
        frame = v1.read()
        imgbgr = cv2.resize(frame,(0,0),None,1/factor,1/factor)
        img = cv2.cvtColor(imgbgr,cv2.COLOR_BGR2RGB)

        curtframloc = face_recognition.face_locations(img)
        curtframncods = face_recognition.face_encodings(img,curtframloc)

        for loc,enc in zip(curtframloc,curtframncods):
            matchs = face_recognition.compare_faces(knownFaceEncodings,enc,0.4)
            
            dis = face_recognition.face_distance(knownFaceEncodings,enc)

            matchIndex = np.argmin(dis)
            name = names[matchIndex].upper()           

            y1,x2,y2,x1 = loc[0]*factor,loc[1]*factor,loc[2]*factor,loc[3]*factor
            if matchs[matchIndex]:
                name = names[matchIndex].upper()
                
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(frame,(x1,y2+35),(x2,y2),(0,255,0),-1)
                cv2.putText(frame,name,(x1+10,y2+25),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)
            
            else:
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
                cv2.rectangle(frame,(x1,y2+35),(x2,y2),(0,0,255),-1)
                cv2.putText(frame,"UnAuthorized",(x1+10,y2+25),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)

            if True in matchs:
                first_known_face = matchs.index(True)
                print(f"\nHello {name} !")
                print("Your vechile door is unlocked...\n")
                face_is_match = True
                break
            else:
                if(ct>0):
                    ct-=1
                    print(f"Access denied \nAttempts left - {ct}")
                    cv2.imwrite(f"{os.getcwd()}\\unauthorthorized\\k.jpg",frame)    


        #fps.update()  
        cv2.imshow("showMe",frame)
        
        key = cv2.waitKey(1) & 0xFF

        if face_is_match:
            # sendOnce()
            break
        if(ct < 1):
            global unAurAccess
            unAurAccess = True
            print("\nUnauthorized Access!")
            break

    time.sleep(3)
    cam.release()
    cv2.destroyAllWindows()
    v1.stop()
    #fps.stop()
    # print("[INFO] approx. FPS: {:.2f}\n".format(fps.fps()))
    # print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        
            
#main start

#inpt = input().strip()
#if inpt.lower() == "start":
video()


if unAurAccess:
    
    sendMapLoc()
else:
    sendOnce()