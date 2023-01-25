import cv2
import face_recognition
import pickle
import os
from config import namepath,encodepath,imaglist,imagpath


def processImgs():
    imgs = []
    encodings = []
    names = []
    for imgpath in imaglist:
        curbgrimg = cv2.imread(f'{imagpath}/{imgpath}')
        curimg = cv2.cvtColor(curbgrimg,cv2.COLOR_BGR2RGB)
        imgs.append(curimg)
        curname = os.path.splitext(imgpath)[0]
        names.append(curname)
        
    for img,name in zip(imgs,names):
        print(f'Processing image {name} ...')
        curencods = face_recognition.face_encodings(img)[0]
        encodings.append(curencods)
    return encodings,names

with open(namepath,'wb') as f1 , open(encodepath,'wb') as f2:
    en,nam = processImgs()
    pickle.dump(en,f1)
    pickle.dump(nam,f2)