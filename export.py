import MySQLdb
import time
import datetime
import usb

def output_to_file(rrr,ddd,sss,interval):
  
    db = MySQLdb.connect("localhost","root","password") 							#connect the database
    cursor = db.cursor()
  
    sql= """USE CRT1;"""
    cursor.execute(sql)
	
    outfile = open("/home/pi/Desktop/exporting.txt","w") 													#ismei save krenge output || name can preferably be the date!
   	
    rrr=rrr.upper()
    sss=sss.upper()
    ddd=ddd.upper()
    
    if len(rrr)==1:
        rrr=rrr+"   "
    elif len(rrr)==2:
        rrr=rrr+"  "
    elif len(rrr)==3:
        rrr=rrr+" "
    if len(sss)==1:
        sss=sss+"   "
    elif len(rrr)==2:
        sss=sss+"  "
    elif len(rrr)==3:
        sss=sss+" "
    if len(ddd)==1:
        ddd=ddd+"   "
    elif len(ddd)==2:
        ddd=ddd+"  "
    elif len(ddd)==3:
        ddd=ddd+" "
    
    outstring1 = "1 "+rrr+" "+ddd+" "+sss
    outfile.write(outstring1+"\n")
    #time1=str(hh1+":"+mm1)
    #time2=str(hh2+":"+mm2)
    intt=int(interval)
    sql = ("""SELECT * FROM TEMPERATURES1;""")		#Retrieving data from whole dbms
    cursor.execute(sql)
    print ("output_to_file ke andar hai")
    result = cursor.fetchall()
    giveresult(result,intt,outfile)
  

def giveresult(result,interval,outfile):
    maxtemp = float(result[0][1])
    mintemp = float(result[0][1])
	
    absmaxtemp = float(result[0][1])
    absmintemp = float(result[0][1])

    epochcalc=int(result[0][0])
        
    kk=time.strftime("%d/%m/%Y %H:%M:%S",time.localtime(float(result[0][0])))
	
    x=kk[:10]
    y=kk[11:16]

    mindate =x																				#min ki date
    maxdate =x																			
	
    absmaxdate =x																		#absolute max ki date
    absmindate =x

    mintime=y			
    maxtime=y
	
    absmaxtime=y
    absmintime=y
	
    perdate=x



    if 1:
        if maxtemp<0:
            maxdate=maxdate[0:]
            if maxtemp<=-10.0:
                outstring3="3 " +str(maxdate[:6])+str(maxdate[-2:])+" "+str(maxtime)+" " + (tt_final)+" Deg C HR MAX"
            else:
                timetemp = tt_file[1:]
                timetemp = "-0"+timetemp
                outstring3="3 " +str(maxdate[:6])+str(maxdate[-2:])+" "+str(maxtime)+" " + (timetemp)+" Deg C HR MAX"
            
        else:
            if maxtemp<10.0:
                outstring3="3 " +str(maxdate[:6])+str(maxdate[-2:])+" "+str(maxtime)+" +0" +(str(float(maxtemp)))+" Deg C HR MAX"
            else:
                outstring3="3 " +str(maxdate[:6])+str(maxdate[-2:])+" "+str(maxtime)+" +" +(str(float(maxtemp)))+" Deg C HR MAX"
        
        if mintemp<0:
            if mintemp<=-10.0:
                outstring4="4 " +str(mindate[:6])+str(mindate[-2:])+" "+str(mintime)+" " + str("05.1f" % (float(mintemp)))+" Deg C HR MIN"
            else:
                timetemp = tt_file[1:]
                timetemp = "-0"+timetemp
                outstring4="4 " +str(mindate[:6])+str(mindate[-2:])+" "+str(mintime)+" " + (timetemp)+" Deg C HR MIN"

        else:
            if mintemp<10.0:
                outstring4="4 " +str(mindate[:6])+str(mindate[-2:])+" "+str(mintime)+" +0" + (str(float(mintemp)))+" Deg C HR MIN"
            else:
                outstring4="4 " +str(mindate[:6])+str(mindate[-2:])+" "+str(mintime)+" +" +(str(float(mintemp)))+" Deg C HR MIN"
  
                
            #print mintemp
            

	number10 = 0
	count = epochcalc
	intt = int(interval)
	apt_diff = 60*intt
	i=0
	
        for row in result:
            i=i+1
            #number10+=1
            kk=time.strftime("%d/%m/%Y %H:%M:%S",time.localtime(float(row[0])))
            epochcalc2=int(row[0])
            epochdiff1 = int((epochcalc2-epochcalc)/60)
            
            #if epochdiff1>(60*intt):
                #epochcalc2=row[0]
            outdate = kk[:10]
            outtime = kk[11:16]
            outtemp = float(row[1])
            outtemp = float(outtemp)
            tt_file=str(outtemp)
            temptemp=outtemp
            if outtemp>=absmaxtemp:															#changing absolute maximum and minimum(which will be per minute)
                absmaxtemp=outtemp
                absmaxdate=outdate
                absmaxtime=outtime
                abmx=tt_file
		                
            if absmintemp>=outtemp:
                absmintemp=outtemp
                absmindate=outdate
                absmintime=outtime
                abmn=tt_file
            
            if epochdiff1%intt==0:  #num%60==0																	for every hour (increasing num at every minute(reading))
                difference1 = epochcalc2-count
                count=epochcalc2
                if difference1 == 2*apt_diff:
                    kk2=time.strftime("%d/%m/%Y %H:%M:%S",time.localtime(float(result[i-1][0])-60*intt))
                    outdate_2 = kk2[:10]
                    outtime_2 = kk2[11:16]
                    outtemp_2 = float(result[i-1][1])
                    if outtemp_2<0:
                        if outtemp<=-10.0:
                            outstring = "2 "+str(outdate_2[:6])+str(outdate_2[-2:])+" "+outtime_2+" " +tt_file+" Deg C"
                        else:
                            timetemp = tt_file[1:]
                            timetemp = "-0"+timetemp
                            outstring = "2 "+str(outdate_2[:6])+str(outdate_2[-2:])+" "+outtime_2+" " +timetemp+" Deg C"
                    else:
                        if outtemp_2<10.0:
                            outstring = "2 "+str(outdate_2[:6])+str(outdate_2[-2:])+" "+outtime_2+" +0" +tt_file+" Deg C"
                        else:
                            outstring = "2 "+str(outdate_2[:6])+str(outdate_2[-2:])+" "+outtime_2+" +" +tt_file+" Deg C"
                    
                    outfile.write(outstring+"\n")
                    
                                                                                
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
                                
                if mintemp>=outtemp:
                    mintemp=float(outtemp)
                    mindate=outdate
                    mintime=outtime
                    if mintemp>=0:
                        if mintemp<10.0:
                            print mintemp
                            outstring4 = "4 "+str(mindate[:6])+str(mindate[-2:])+" "+str(mintime)+" +" + tt_file+" Deg C HR MIN"
                        else:
                            outstring4 = "4 "+str(mindate[:6])+str(mindate[-2:])+" "+str(mintime)+" +" + tt_file+" Deg C HR MIN"
                    else:
                        if mintemp<=-10.0:
                            outstring4 = "4 "+str(mindate[:6])+str(mindate[-2:])+" "+str(mintime)+" " + tt_file+" Deg C HR MIN"
                        else:
                            timetemp = tt_file[1:]
                            timetemp = "-0"+timetemp
                            outstring4 = "4 "+str(mindate[:6])+str(mindate[-2:])+" "+str(mintime)+" " + timetemp+" Deg C HR MIN"
                        
                if outtemp>=maxtemp:															
                    maxtemp=outtemp
                    maxdate=outdate
                    maxtime=outtime
                    if outtemp>=0:
                        if outtemp<10.0:
                            outstring3 = "3 " +str(maxdate[:6])+str(maxdate[-2:])+" "+str(maxtime)+" +" + tt_file+" Deg C HR MAX"						#hourly max temperature per day
                        else:
                            outstring3 = "3 " +str(maxdate[:6])+str(maxdate[-2:])+" "+str(maxtime)+" +" + tt_file+" Deg C HR MAX"
		    else:
                        if outtemp<=-10.0:
                            outstring3 = "3 " +str(maxdate[:6])+str(maxdate[-2:])+" "+str(maxtime)+" " + tt_file+" Deg C HR MAX"						#hourly max temperature per day
                        else:
                            timetemp = tt_file[1:]
                            timetemp = "-0"+timetemp
                            outstring3 = "3 " +str(maxdate[:6])+str(maxdate[-2:])+" "+str(maxtemp)+" " + timetemp+" Deg C HR MAX"

                            		
                if outtemp>=0 : 																#Line 2 of the output file
                    if outtemp<10.0:
                        outstring = "2 "+str(outdate[:6])+str(outdate[-2:])+" "+outtime+" +0" +tt_file+" Deg C"
                    else:
                        outstring = "2 "+str(outdate[:6])+str(outdate[-2:])+" "+outtime+" +" +tt_file+" Deg C"
                    
                else :
                    if outtemp<=-10.0:
                         outstring = "2 "+str(outdate[:6])+str(outdate[-2:])+" "+outtime+" " + tt_file+" Deg C"
                    else:
                         timetemp = tt_file[1:]
                         timetemp = "-0"+timetemp
                         outstring = "2 "+str(outdate[:6])+str(outdate[-2:])+" "+outtime+" " + timetemp+" Deg C"
       
                outfile.write(outstring+"\n")
		
            #num=num+1
															
        outfile.write(outstring3+"\n")														#Writing the hourly maximum and minimum temperature
        outfile.write(outstring4+"\n")														#Writing Line-3 and Line-4
        if absmaxtemp>0:
            if absmaxtemp<10.0:
                outstring5 = "5 "+str(absmaxdate[:6])+str(absmaxdate[-2:])+" "+str(absmaxtime)+" +" + abmx+" Deg C AB MAX"		#Writing Absolute minimum and maximum ONCE
            else:
                outstring5 = "5 "+str(absmaxdate[:6])+str(absmaxdate[-2:])+" "+str(absmaxtime)+" +" + abmx+" Deg C AB MAX"
	else:
            if absmaxtemp<=-10.0:
                outstring5 = "5 "+str(absmaxdate[:6])+str(absmaxdate[-2:])+" "+str(absmaxtime)+" -" + abmx+" Deg C AB MAX"		#Writing Absolute minimum and maximum ONCE
            else:
                timetemp = abmx[1:]
                timetemp = "-0"+timetemp
                outstring5 = "5 "+str(absmaxdate[:6])+str(absmaxdate[-2:])+" "+str(absmaxtime)+" -" + timetemp+" Deg C AB MAX"		#Writing Absolute minimum and maximum ONCE
              
	
        if(absmintemp<0):
            if absmintemp<=-10.0:
                outstring6 = "6 "+str(absmindate[:6])+str(absmindate[-2:])+" "+str(absmintime)+" " + abmn+" Deg C AB MIN"
            else:
                timetemp = abmn[1:]
                timetemp = "-0"+timetemp
                outstring6 = "6 "+str(absmindate[:6])+str(absmindate[-2:])+" "+str(absmintime)+" " + timetemp+" Deg C AB MIN"
            
        else:
            if absmintemp<10.0:
                outstring6 = "6 "+str(absmindate[:6])+str(absmindate[-2:])+" "+str(absmintime)+" +" +(abmn)+" Deg C AB MIN"
            else:
                outstring6 = "6 "+str(absmindate[:6])+str(absmindate[-2:])+" "+str(absmintime)+" +" + (abmn)+" Deg C AB MIN"
        outfile.write(outstring5+"\n")	
        outfile.write(outstring6+"\n")
        #return "2"

        








































































































 







    print "42"
    """num=0
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
	
    absmaxdate =x																		#absolute max ki date
    absmindate =x
	
    mintime=y			
    maxtime=y
	
    absmaxtime=y
    absmintime=y
	
    perdate=x
    
    outstring3="3 " +str(maxdate)+" "+str(maxtime)+" +" + str(maxtemp)+" Deg C HR MAX"
    outstring4="4 " +str(mindate)+" "+str(mintime)+" +" + str(mintemp)+" Deg C HR MIN"

    number10 = 0
    count = epochcalc
    intt = int(interval)
    apt_diff = 60*intt
    i=0
    
    for row in result:
        i=i+1
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
            absmaxtemp=outtemp
            absmaxdate=outdate
            absmaxtime=outtime
		                
        if absmintemp>=outtemp:
            absmintemp=outtemp
            absmindate=outdate
            absmintime=outtime

        if epochdiff1%intt==0:  #num%60==0																	for every hour (increasing num at every minute(reading))
            difference1=epochcalc2-count
            count=epochcalc2
            if difference1 == 2*apt_diff:
                kk2=time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(float(result[i-1][0])-60*intt))
                outdate_2 = kk2[:10]
                outtime_2 = kk2[11:16]
                outtemp_2 = result[i-1][1]
                if outtemp_2>=0:
                    outstring = "2 "+str(outdate_2)+" "+outtime_2+" +"+str(outtemp_2)+" Deg C"
                else:
                    outstring = "2 "+str(outdate_2)+" "+outtime_2+" -"+str(outtemp_2)+" Deg C"
                outfile.write(outstring+"\n")
        
        #if (int(num)%1)==0:
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
                              
            if mintemp>=outtemp:
                mintemp=outtemp
                mindate=outdate
                mintime=outtime
                if(mintemp<0):
                    outstring4 = "4 "+str(mindate)+" "+str(mintime)+" +" + str(mintemp)+" Deg C HR MIN"	
                else:
                    outstring4 = "4 "+str(mindate)+" "+str(mintime)+" +" + str(mintemp)+" Deg C HR MIN"
            
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
            print "44"
		
        num=num+1
															
    outfile.write(outstring3+"\n")														#Writing the hourly maximum and minimum temperature
    outfile.write(outstring4+"\n")														#Writing Line-3 and Line-4
       
    outstring5 = "5 "+str(absmaxdate)+" "+str(absmaxtime)+" +" + str(absmaxtemp)+" Deg C AB MAX"		#Writing Absolute minimum and maximum ONCE
	
    if(absmintemp<0):
        outstring6 = "6 "+str(absmindate)+" "+str(absmintime)+" -" + str(absmintemp)+" Deg C AB MIN"	
    else:
        outstring6 = "6 "+str(absmindate)+" "+str(absmintime)+" +" + str(absmintemp)+" Deg C AB MIN"
	
    outfile.write(outstring5+"\n")	
    outfile.write(outstring6+"\n")
    #return "2"
    print "45"
"""
