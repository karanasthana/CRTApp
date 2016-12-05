import MySQLdb
import toaudio
import datetime
import time

db = MySQLdb.connect("localhost","root","password","CRT1")
cursor = db.cursor()

def todbms(tt,date,time1,num):
    #if num%1==0 :
    if num%60==1 :
        today = str(date)
        yy=str(today[:4])
        mm=str(today[5:7])
        dd=str(today[8:10])
        stringdatetime = dd+"/"+mm+"/"+yy+" "+str(time1[:5])+":00"
        #stringtime = str(time[:5])
        epochtime = int(time.mktime(time.strptime(stringdatetime,"%d/%m/%Y %H:%M:%S")))        
        epochtime=str(epochtime)
        temper=str(tt)
        sql = ("""INSERT INTO TEMPERATURES1 VALUES ('%s','%s');""" %(epochtime,temper))
        cursor.execute(sql)
        db.commit()
        return "1"
    return "0"
