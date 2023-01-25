import cv2
import face_recognition
import numpy as np
import pickle
import time

#custom libraries
import mapdata.mdata
import database.dbase

from config import encodepath,namepath

mapd = mapdata.mdata.location()
mapip = mapdata.mdata.iplocation()
db = database.dbase.databs()

ct = 5
factor = 2


stop = False
unAurAccess = False

cam = cv2.VideoCapture(0)

def sendMapLoc():
    while True:
        print("\nThe data is sending....\n")
        #db.updatelocation(mapip.lat(),mapip.long()) # by using ip
        db.updatelocation(mapd.lat(),mapd.long()) # random loc
        time.sleep(20)


def sendOnce():
    db.updatelocation(mapd.lat(),mapd.long())

knownFaceEncodings = pickle.load(open(encodepath,'rb'))
names = pickle.load(open(namepath,'rb'))

print(names)

def video():
    global ct
    face_is_match = False
    while input:

        success,frame = cam.read()
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

            if True in matchs:
                first_known_face = matchs.index(True)
                print(f"Hello {name} your vechile is unlocked...")
                face_is_match = True
                break
            else:
                print(f"Access dennied {ct}")    
                ct-=1

        cv2.imshow("test",frame)
        cv2.waitKey(1)
        if face_is_match:
            sendOnce()
            break
        if(ct < 1):
            global unAurAccess
            unAurAccess = True
            print("Unauthorized Access !")
            break
        
            
        
        
#main start

inpt = input().strip()
if inpt.lower() == "start":
    video()


cam.release()
cv2.destroyAllWindows()



if unAurAccess:
    sendMapLoc()
