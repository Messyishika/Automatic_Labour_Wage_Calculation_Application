import cv2
import numpy as np
import face_recognition
import os
import shutil
import glob

src_dir=r'C:\xampp\htdocs\myProject\newImages'
dst_dir=r'C:\xampp\htdocs\myProject\LabourImages'
for jpgfile in glob.iglob(os.path.join(src_dir,"*.jpg")):
    shutil.copy(jpgfile,dst_dir)

images=[]
classnames=[]
path='newImages'
myList=os.listdir(path)

for cls in myList:
    curImg=cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classnames.append(os.path.splitext(cls)[0])

def findencodings(images):
    encodeList=[]
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown=findencodings(images)

#print((encodeListKnown))
with open("encoding.txt", "a") as f:
    for i in encodeListKnown:
         for k in i:
             f.write(str(k)+"\n")

for file in os.listdir(src_dir):
    file_path=os.path.join(src_dir,file)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print("")