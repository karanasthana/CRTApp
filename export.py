import MySQLdb
import time
import datetime
import usb

def output_to_file(r,d,s,interval):
  
    db = MySQLdb.connect("localhost","root","password") 							#connect the database
    cursor = db.cursor()
  
    sql= """USE CRT1;"""
    cursor.execute(sql)
	
    outfile = open("testing.text","w") 													#ismei save krenge output || name can preferably be the date!
   	
    outstring1 = "1 "+r+" "+d+" "+s
    outfile.write(outstring1+"\n")  															#Line-1 into the file

    #time1=str(hh1+":"+mm1)
    #time2=str(hh2+":"+mm2)
    intt=int(interval)
    sql = ("""SELECT * FROM TEMPERATURES1;""")		#Retrieving data from whole dbms
    cursor.execute(sql)
<<<<<<< HEAD
=======
    print ("output_to_file ke andar hai")
>>>>>>> af532db9937a5d6a3c02e2562262da1833c1ca11
    result = cursor.fetchall()
    giveresult(result,intt,outfile)
  

def giveresult(result,interval,outfile):
<<<<<<< HEAD
  
    num=0																				#To deal with the timeinterval(in minutes)	
    maxtemp = result[0][2]
    mintemp = result[0][2]
	
    absmaxtemp = result[0][2]
    absmintemp = result[0][2]
	
    x=result[0][0]
    y=result[0][1]
	
    mindate =x																				#min ki date
    maxdate	=x																			
=======
    print "42"
    num=0
    maxtemp = result[0][1]
    mintemp = result[0][1]
	
    absmaxtemp = result[0][1]
    absmintemp = result[0][1]

    epochcalc=int(result[0][0])

    kk=time.strftime("%d/%m/%Y %H:%M:%S",time.localtime(float(result[0][0])))

    print ("give_result ke andar hai")
	
    x=kk[:10]
    y=kk[11:16]
	
    mindate =x																				#min ki date
    maxdate =x																			
>>>>>>> af532db9937a5d6a3c02e2562262da1833c1ca11
	
    absmaxdate =x																		#absolute max ki date
    absmindate =x
	
    mintime=y			
    maxtime=y
	
    absmaxtime=y
    absmintime=y
	
    perdate=x
    
    outstring3="3 " +str(maxdate)+" "+str(maxtime)+" +" + str(maxtemp)+" Deg C HR MAX"
    outstring4="4 " +str(mindate)+" "+str(mintime)+" +" + str(mintemp)+" Deg C HR MIN"
	
    for row in result:
<<<<<<< HEAD
        outdate = row[0]
	outtime = row[1]
	outtemp = row[2]
	temptemp=outtemp
	if outtemp>=absmaxtemp:															#changing absolute maximum and minimum(which will be per minute)
=======
        print "43"
        #number10+=1
        kk=time.strftime("%d/%m/%Y %H:%M:%S",time.localtime(float(row[0])))
        epochcalc2=int(row[0])
        epochdiff1 = int((epochcalc2-epochcalc)/60)
            
        #if epochdiff1>(60*intt):
            #epochcalc2=row[0]
        outdate = kk[:10]
        outtime = kk[11:16]
        outtemp = row[1]
        temptemp=outtemp
        if outtemp>=absmaxtemp:															#changing absolute maximum and minimum(which will be per minute)
>>>>>>> af532db9937a5d6a3c02e2562262da1833c1ca11
            absmaxtemp=outtemp
            absmaxdate=outdate
            absmaxtime=outtime
		                
<<<<<<< HEAD
	if absmintemp>=outtemp:
            absmintemp=outtemp
            absmindate=outdate
            absmintime=outtime

	intt=int(interval)		
	if num==intt:  #num%60==0																	for every hour (increasing num at every minute(reading))
=======
        if absmintemp>=outtemp:
            absmintemp=outtemp
            absmindate=outdate
            absmintime=outtime
            
        intt = int(interval)		
        if epochdiff1%intt==0:  #num%60==0																	for every hour (increasing num at every minute(reading))
        #if (int(num)%1)==0:
>>>>>>> af532db9937a5d6a3c02e2562262da1833c1ca11
            if perdate!=outdate:
                perdate=outdate
                outfile.write(outstring3+"\n")														#Writing the hourly maximum and minimum temperature
                outfile.write(outstring4+"\n")														#Writing Line-3 and Line-4
                mintemp=outtemp
                maxtemp=outtemp
                mindate=outdate
                maxdate=outdate
                mintime=outtime
                maxtime=outtime
<<<<<<< HEAD
                                
=======
                              
>>>>>>> af532db9937a5d6a3c02e2562262da1833c1ca11
            if mintemp>=outtemp:
                mintemp=outtemp
                mindate=outdate
                mintime=outtime
                if(mintemp<0):
                    outstring4 = "4 "+str(mindate)+" "+str(mintime)+" +" + str(mintemp)+" Deg C HR MIN"	
                else:
                    outstring4 = "4 "+str(mindate)+" "+str(mintime)+" +" + str(mintemp)+" Deg C HR MIN"
<<<<<<< HEAD
                
=======
            
>>>>>>> af532db9937a5d6a3c02e2562262da1833c1ca11
            if outtemp>=maxtemp:															
                maxtemp=outtemp
                maxdate=outdate
                maxtime=outtime
                outstring3 = "3 " +str(maxdate)+" "+str(maxtime)+" +" + str(maxtemp)+" Deg C HR MAX"						#hourly max temperature per day
			
            if outtemp>=0 : 																#Line 2 of the output file
                outstring = "2 "+str(outdate)+" "+outtime+" +" +str(outtemp)+" Deg C"
            else :
                outstring = "2 "+str(outdate)+" "+outtime+" -" + str(outtemp)+" Deg C"
            outfile.write(outstring+"\n")
<<<<<<< HEAD
	    num=1
	    
=======
            print "44"
		
>>>>>>> af532db9937a5d6a3c02e2562262da1833c1ca11
        num=num+1
															
    outfile.write(outstring3+"\n")														#Writing the hourly maximum and minimum temperature
    outfile.write(outstring4+"\n")														#Writing Line-3 and Line-4
<<<<<<< HEAD
        
=======
       
>>>>>>> af532db9937a5d6a3c02e2562262da1833c1ca11
    outstring5 = "5 "+str(absmaxdate)+" "+str(absmaxtime)+" +" + str(absmaxtemp)+" Deg C AB MAX"		#Writing Absolute minimum and maximum ONCE
	
    if(absmintemp<0):
        outstring6 = "6 "+str(absmindate)+" "+str(absmintime)+" -" + str(absmintemp)+" Deg C AB MIN"	
    else:
        outstring6 = "6 "+str(absmindate)+" "+str(absmintime)+" +" + str(absmintemp)+" Deg C AB MIN"
	
    outfile.write(outstring5+"\n")	
    outfile.write(outstring6+"\n")
<<<<<<< HEAD
    usb.usbexport()
=======
    #return "2"
    print "45"








>>>>>>> af532db9937a5d6a3c02e2562262da1833c1ca11
