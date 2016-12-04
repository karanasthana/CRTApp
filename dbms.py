import MySQLdb

db = MySQLdb.connect("localhost","root","password","CRT1")
cursor = db.cursor()

def todbms(tt,date,time,num):
    #if num%1==0 :
    if num%60==0 :
        today = str(date)
        yy=str(today[:4])
        mm=str(today[5:7])
        dd=str(today[8:10])
        stringdate = dd+"/"+mm+"/"+yy
        stringtime = str(time[:5])
        temper=str(tt)
        sql = ("""INSERT INTO TEMPERATURES1 VALUES ('%s','%s','%s');""" %(stringdate,stringtime,temper))
        cursor.execute(sql)
        db.commit()    