from flask import Flask, render_template
from flask_cors import CORS
import cv2
import numpy as np
import face_recognition
import os
import datetime
import pandas as pd
import mysql.connector
import glob

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

path='LabourImages'
images=[]
classnames=[]
classUniqId=[]  #stores Unique Id
classname=[] #Stores name
myList= os.listdir(path)

for cls in myList:
    curImg=cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classnames.append(os.path.splitext(cls)[0])

for _ in classnames:
    data= _.split(",")
    classUniqId.append(data[1])  #separating id and name from photo name
    classname.append(data[0])

nameList=[]
def markAttendance(name):#marks attendence in database and returns the time
            conn=mysql.connector.connect(host='localhost', user='root',passwd='',database='mysql')
            cursor=conn.cursor()
            nowd = datetime.datetime.now()
            dtStringY = nowd.strftime("%D %H:%M:%S")
            dtString = dtStringY.split(" ")
            sql=("INSERT INTO attendance(Name,Date,Time)"
            "VALUES(%s,%s,%s)")
            d=(name,dtString[0],dtString[1])
            cursor.execute(sql,d)
            cursor.execute("Select * from attendance")
            myresult = cursor.fetchall()
            conn.commit()

            for row in myresult:
                if name in row[0]:
                    print(row)
                    return row

            conn.commit()

def getLabourDetails(name):#fetching details from database
   # namei=(name)
    mydb = mysql.connector.connect(host='localhost', user='root', passwd='', database='mysql')
    mycursor = mydb.cursor()
    mycursor.execute("Select * from information")
    myresult = mycursor.fetchall()
    name=str.title(name)
    for row in myresult:
        if name in row[0]:
            return row

encodeListKnown=[]
with open("encoding.txt", "r") as f:
     #lines=f.readline()
     while True:
      lines = f.readline()
      if(lines==''):
         break
      encode=[]
      encode.append(float(lines))
      for i in range(127):
         lines = f.readline()
         encode.append(float(lines))
      encodeListKnown.append(encode)

@app.route("/")
def hello_world():
    while (True):
        row=0
        img_dir = 'Uploads'
        data_path = os.path.join(img_dir, '*g')
        files = glob.glob(data_path)
        for i in files:
            img=cv2.imread(i)
        imgS =cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        faceCurr = face_recognition.face_locations(imgS)
        encodeCurr = face_recognition.face_encodings(imgS,faceCurr)

        for enf,floc in zip(encodeCurr,faceCurr):
            matches=face_recognition.compare_faces(encodeListKnown,enf)
            faceDis=face_recognition.face_distance(encodeListKnown,enf)
            matchIndex=np.argmin(faceDis)
            min = np.amin(faceDis)
            print(min)

            if matches[matchIndex]:
                name = classname[matchIndex].upper()
                #print(name)
                y1,x2,y2,x1=floc
                y1, x2, y2, x1 =y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(145,60,255),2)

                if (min < 0.5000000000000000):  # Threshold value
                    time=markAttendance(name)
                    row=getLabourDetails(name)
                    hour=abs(int(time[2][0]+time[2][1])-9)
                    wage=int(hour*row[4])



        if(row):
            return render_template("webpage.html", data=row , w=wage, h=hour) #returning the values to the webpage
        else:
            return render_template("Norecord.html")

app.run("localhost",port=5000,debug=True)




