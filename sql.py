import pandas as pd
import mysql.connector
mydb=mysql.connector.connect(host='localhost', user='root', passwd ='', database='mysql')
mycursor=mydb.cursor()
mycursor.execute("Select * from information")
myresult=mycursor.fetchall()

for row in myresult:
    print(row)