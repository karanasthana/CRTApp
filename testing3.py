import calendar
import pcalender
import time
import datetime
import re
import tkMessageBox
import os
import glob
import subprocess
import shutil
import MySQLdb
import pyaudio
import binascii

try:
    import Tkinter as tk
    import tkFont
    import ttk
except ImportError:
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk


def errorBox(msg):

	tkMessageBox.showerror("Error", msg)

def center(x):
    x.update_idletasks()
    w=x.winfo_screenwidth()
    h=x.winfo_screenheight()
    size=tuple(int(_) for _ in x.geometry().split('+')[0].split('x'))
    xx=w/2-size[0]/2
    yy=h/2-size[1]/2
    x.geometry("%dx%d+%d+%d" % (size + (xx,yy)))

def dummyDone(x):
    print "done"
    global app
    x.destroy()
    dbox = tk.Toplevel(app)
    dbox.wm_title("Done")
    dbox.wm_geometry("360x100")
    
    center(dbox)

    defaultFont = tkFont.Font(family = "Helvetica", size = 10, weight = "bold")

    label = tk.Label(dbox,text="Exporting Done",font = defaultFont)
    label.grid(padx=10,pady=10,sticky="w")

    button = tk.Button(dbox,text = "OK", command=dbox.destroy)
    button.grid(row=1,column=1,pady=10,sticky="e",padx=30)

    dbox.mainloop()



"""#def dummyProgress(x):

    global app
    x.destroy()
    pbox = tk.Toplevel(app)
    pbox.wm_geometry("360x100")
    pbox.wm_title("Exporting")
    defaultFont = tkFont.Font(family = "Helvetica", size = 10, weight = "bold")

    label = tk.Label(pbox,text="Exporting",font = defaultFont)
    label.grid(padx=10,pady=10,sticky="w")

    pb = ttk.Progressbar(pbox, orient='horizontal', mode='determinate',length='300')
    pb.grid(row=1,pady=10,padx=30)

    pb.start(1)
    app.after(2000,lambda:dummyDone(pbox))
    pbox.mainloop()"""

    # dummyDone()

TILIST = ["Minutes","Hours"]

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

def sendAudio(t,date,time,r,d,s,num):
    if num%60==0:
        try:
            if(t>=0):
                a="1 RRRR + SSSS + DDDD" + "\n" + "2" + date+" +"+time+" +"+t+" Deg C"
            else:
                a="1 RRRR + SSSS + DDDD" + "\n" + "2" + date+" +"+time+" -"+t+" Deg C"
            b = bin(int(binascii.hexlify(c),16))

            sample_stream=[]
            high_note = (b'\xFF'*100 + b'\0'*100)*50
            low_note = (b'\xFF'*50 + b'\0'*50)*100

            for bit in b[2:] :
                if bit == '1':
                    sample_stream.extend(high_note)
                else:
                    sample_stream.extend(low_note)

            sample_buffer = b''.join(sample_stream)

            p = pyaudio.PyAudio()
            stream = p.open(format = p.get_format_from_width(4),channels=1,rate=44100,output=True)
            #stream.write(sample_buffer)   """ ISKO CHALAANE PE INFINITE LOOP AARA HAI AND KUCH HO NHI RAHA!! """
        except:
            pass


def inputBox():

    global app
    ibox = tk.Toplevel(app)
    ibox.wm_geometry("460x130")
    ibox.wm_title("Time Interval")
    center(ibox)
    defaultFont = tkFont.Font(family = "Helvetica", size = 10, weight = "bold")

    label = tk.Label(ibox,text="Enter Time Interval",font = defaultFont)
    label.grid(padx=10,pady=10,columnspan=2,sticky="w")

    v= tk.StringVar()

    entry = tk.Entry(ibox,width=40,textvariable=v)
    entry.grid(row=1,column=0,padx=10)
    v.set("5")

    ti = tk.StringVar(ibox)
    ti.set(TILIST[0])
    TI = ttk.Combobox(ibox, textvariable = ti, values=TILIST,width=10)
    TI.grid(row=1,column=1)

    button = tk.Button(ibox,text = "Export", command=lambda:dummyDone(ibox))
    button.grid(row=2,column=0,columnspan=2,pady=10)

    entry1 = tk.Entry(entry)
    
    entry1.bind("<FocusIn>",controller.call_keyboard)
    entry1.bind("<FocusOut>",controller.close_keyboard)
       
    ibox.mainloop()


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir='/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-000001db066d')[0]
device_file = device_folder+'/w1_slave'

def read_temp_raw():
    f=open(device_file,'r')
    lines=f.readlines()
    f.close()
    return lines

def read_temp():
    lines=read_temp_raw()
    while lines[0].strip()[-3:]!='YES' :
        lines=read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = ("%.1f" % (float(temp_string)/1000.0))
        return temp_c    




HHLIST = ["00","01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
            "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]
MMLIST = ["00","01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
            "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
            "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
            "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
            "41", "42", "43", "44", "45", "46", "47", "48", "49", "50",
            "51", "52", "53", "54", "55", "56", "57", "58", "59"]

def qf():
    print ("done")

def get_calendar(locale, fwday):
    # instantiate proper calendar class
    if locale is None:
        return calendar.TextCalendar(fwday)
    else:
        return calendar.LocaleTextCalendar(fwday, locale)

def update_maxmin(temp):
    global secondGap,max,min,prev_date
    current_time=str(datetime.datetime.now()+datetime.timedelta(seconds=secondGap))
    date=str(prev_date)
    dd1=str(current_time[:2])
    dd2=str(date[:2])
    if dd1 == dd2:
        max=float(max)
        temp = float(temp)
        if temp>max:
            if float(temp)<85:
                max=temp
                print "HEY!"
            else:
                print "Hil-gaya"
        elif temp<min:
            min=temp
    else:
        max=temp
        min=temp
    return (max,min)

def recorder(num = 1):
    global app
    global t1,t2,t3,date,time,rrr,sss,ddd,rrrr,ssss,div,max,min,prev_date
    if num is 1:
        rrrr.configure(text=rrr.upper())
        ssss.configure(text=sss.upper())
        div.configure(text=ddd.upper())
        max=0
        min=0
        prev_date=""
    if num:
        tt=read_temp()
        global secondGap
        today = str(datetime.datetime.now()+datetime.timedelta(seconds=secondGap))
        todaytime = str(today[11:19])
        today= str(today[:10])
        global max,min
        max,min=update_maxmin(tt)
        prev_date=today
        prev_time=todaytime
        if float(tt)==85.0:
            t1.configure(text = "--")
            errorBox("Check the connection")
        else:
            t1.configure(text = tt)
        t2.configure(text = max)
        t3.configure(text = min)
        date.configure(text = prev_date)
        time.configure(text=prev_time)
        app.after(173, lambda:recorder(num+1))
        app.after(173, lambda:todbms(tt,prev_date,prev_time,num))
        #app.after(173, lambda:sendaudio(tt,date,time,rr,ss,dd,num))

def usbexport():
    source = os.listdir("/home/pi/Downloads/yellow/")
    destination = "/media/pi/TANVI/"
    #CHANGE NAME OF TANVI TO CRT AND THE PENDRIVE BEING CONNECTED SHOULD BE NAMED CRT
    for files in source:
        if files.endswith("put.text"):
            shutil.move(files,destination)



returnToMenu = False

MINSIZEROW2 = 350
MINSIZEROW3 = 0
MINSIZECOLUMN = 266
ENTRYFRAMEPADX = 75
ENTRYFRAMEPADY = 40
BUTTONFRAMEPADX = 310
calframe = None

global rrr,sss,ddd


import MySQLdb
import datetime

def output_on_screen(r,d,s,interval,d1,d2,hh1,hh2,mm1,mm2):

    db = MySQLdb.connect("localhost","root","password") 							#connect the database
    cursor = db.cursor()
    print (str(d1))
  
    sql= """USE CRT1;"""
    cursor.execute(sql)
	
    outfile = open("output.text","w") 													#ismei save krenge output
   	
    outstring1 = "1 "+r+" "+d+" "+s
    outfile.write(outstring1+"\n")
    d1=str(d1)
    d2=str(d2)
    #time1=str(time1)
    #time2=str(time2)
    hh1=str(hh1)
    hh2=str(hh2)
    mm1=str(mm1)
    mm2=str(mm2)

    time1=str(hh1+":"+mm1)
    time2=str(hh2+":"+mm2)
    #sql = ("""SELECT * FROM TEMPERATURES1;""")
    sql = ("""SELECT * FROM TEMPERATURES1 WHERE (DATE = '%s' AND TIME>'%s') OR (DATE > '%s' AND DATE<'%s') OR (DATE = '%s' AND TIME<'%s');""" %(d1,time1,d1,d2,d2,time2))	
    #sql = ("""SELECT * FROM TEMPERATURES1 WHERE (TIME>'%s');""" %(time1))
    cursor.execute(sql)
    result = cursor.fetchall()
    #print result
    print "33"
    #giveresult(result,interval)
    num=0																				#To deal with the timeinterval(in minutes)	
    maxtemp = result[0][2]
    mintemp = result[0][2]
	
    absmaxtemp = result[0][2]
    absmintemp = result[0][2]
	
    x=result[0][0]
    y=result[0][1]
	
    mindate =x																				#min ki date
    maxdate	=x																			
	
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
        outdate = row[0]
	outtime = row[1]
	outtemp = row[2]
	temptemp=outtemp
	if outtemp>=absmaxtemp:															#changing absolute maximum and minimum(which will be per minute)
            absmaxtemp=outtemp
            absmaxdate=outdate
            absmaxtime=outtime
		                
	if absmintemp>=outtemp:
            absmintemp=outtemp
            absmindate=outdate
            absmintime=outtime

	intt = int(interval)		
	#if int(num)%int(interval)==0:  #num%60==0																	for every hour (increasing num at every minute(reading))
        if (int(num)%1)==0:
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





def output_to_file(r,d,s,interval):
  
    db = MySQLdb.connect("localhost","root","password") 							#connect the database
    cursor = db.cursor()
  
    sql= """USE CRT1;"""
    cursor.execute(sql)
	
    outfile = open("testing.text","w") 													#ismei save krenge output || name can preferably be the date!
   	
    outstring1 = "1 "+r+" "+d+" "+s
    outfile.write(outstring1+"\n")  															#Line-1 into the file

    time1=str(hh1+":"+mm1)
    time2=str(hh2+":"+mm2)
    sql = ("""SELECT * FROM TEMPERATURES1;""")		#Retrieving data from whole dbms
    cursor.execute(sql)
    result = cursor.fetchall()
    giveresult(result,interval)
  

def giveresult(result,interval):
  
    num=0																				#To deal with the timeinterval(in minutes)	
    maxtemp = result[0][2]
    mintemp = result[0][2]
	
    absmaxtemp = result[0][2]
    absmintemp = result[0][2]
	
    x=result[0][0]
    y=result[0][1]
	
    mindate =x																				#min ki date
    maxdate	=x																			
	
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
        outdate = row[0]
	outtime = row[1]
	outtemp = row[2]
	temptemp=outtemp
	if outtemp>=absmaxtemp:															#changing absolute maximum and minimum(which will be per minute)
            absmaxtemp=outtemp
            absmaxdate=outdate
            absmaxtime=outtime
		                
	if absmintemp>=outtemp:
            absmintemp=outtemp
            absmindate=outdate
            absmintime=outtime
			
	if num%interval==0:  #num%60==0																	for every hour (increasing num at every minute(reading))
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



class AutoScrollbar(tk.Scrollbar):
    # A scrollbar that hides itself if it's not needed.
    # Only works if you use the grid geometry manager!
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        tk.Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError("cannot use pack with this widget")
    def place(self, **kw):
        raise TclError("cannot use place with this widget")


class CRTApp(tk.Tk):

    DD = ""
    MM = ""
    YYYY = ""

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self,"CRTApp")
        #self.wm_geometry("800x480")
        self.attributes("-zoomed",True)
        self.attributes("-fullscreen",True)
        self.wm_resizable( width=False, height=False)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand="true")
        # container.grid(row=0,column=0)
        # container.grid_rowconfigure(0, weight=1,minsize =480)
        # container.grid_columnconfigure(0, weight=1,minsize=800)

        self.defaultFont = tkFont.Font(family = "Helvetica", size = 10, weight = "bold")
        self.headerFont = tkFont.Font(family = "Helvetica", size = 14, weight = "bold")

        # container.grid_rowconfigure(0, weight=1)
        # container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Login, TMSConfig, DateTimeSetting, MainScreen, Menu, Settings, Output, ViewOutput ):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Login)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def update(self, calframe,e,d,m,y):

        calframe.grid_forget()
        # calframe.destroy()

        # YYYY = ttkcal._date.year
        # MM = ttkcal._date.month
        # DD = ttkcal._selection[0]

        YYYY = y
        MM = m
        DD = d

        e.delete(0, "end")
        e.insert(0,str(DD) + '-' + str(MM) + '-' + str(YYYY))

    def call_calendar(self,container,x,y,e):

        global calframe
        calframe = ttk.Frame(container,borderwidth=3,relief=tk.GROOVE)
        ttkcal = pcalender.Calendar(calframe,self.update,e,firstweekday=pcalender.calendar.SUNDAY)
        ttkcal.grid(row=0,column=0)

        # close = ttk.Button(calframe,text='x',width=1,command=lambda:qf())#self.update(calframe,e,ttkcal))
        # close.grid(row=0,column=1,sticky="nw")
        # calframe.grid(row=0,column=1,rowspan=4)

        calframe.grid(row=0,column=2,rowspan=5)#pady=y+150,padx=x-10)

        # calframe = tk.Toplevel(self)
        # calframe.wm_geometry("800x480")

        # ttkcal = pcalender.Calendar(calframe,self.update,e,firstweekday=pcalender.calendar.SUNDAY)
        # ttkcal.pack(expand=1,fill="both")

    def call_keyboard(self,event):
        subprocess.Popen("matchbox-keyboard")

    def close_keyboard(self,event):
        os.system("killall matchbox-keyboard")
        


class TMSConfig(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(1,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(2,weight=1,minsize = MINSIZECOLUMN)
        # self.grid_rowconfigure(0,weight=1,minsize = 80)
        self.grid_rowconfigure(2,weight=3,minsize = MINSIZEROW2)
        self.grid_rowconfigure(3,weight=1,minsize = MINSIZEROW3)
        
        title = tk.Label(self, text="TMS Configuration", font=controller.headerFont)
        title.grid(row=0,column=0,pady=10,padx=10,columnspan=3, sticky = "w")

        separator = ttk.Separator(self,orient=tk.HORIZONTAL)
        separator.grid(row=1,column=0,columnspan=3,sticky="ew")

        entry = tk.Frame(self)
        entry.grid(row=2, column=0, pady=ENTRYFRAMEPADY,padx=ENTRYFRAMEPADX)

        buttons = tk.Frame(self)#, borderwidth=5, relief=tk.GROOVE)
        buttons.grid(row=3, column=0,padx=BUTTONFRAMEPADX, columnspan=3,sticky="w")

        label1 = tk.Label(entry, text = "Railway Name :",font = controller.defaultFont)
        label2 = tk.Label(entry, text = "Division Name :",font=controller.defaultFont)
        label3 = tk.Label(entry, text = "Station Name :",font=controller.defaultFont)
        label4 = tk.Label(entry, text = "Model Number :", font=controller.defaultFont)        
        
        entry1 = tk.Entry(entry)
        entry2 = tk.Entry(entry)
        entry3 = tk.Entry(entry)
        entry4 = tk.Entry(entry)

        entry1.bind("<FocusIn>",controller.call_keyboard)
        entry2.bind("<FocusIn>",controller.call_keyboard)
        entry3.bind("<FocusIn>",controller.call_keyboard)
        entry4.bind("<FocusIn>",controller.call_keyboard)

        entry1.bind("<FocusOut>",controller.close_keyboard)
        entry2.bind("<FocusOut>",controller.close_keyboard)
        entry3.bind("<FocusOut>",controller.close_keyboard)
        entry4.bind("<FocusOut>",controller.close_keyboard)

        label1.grid(row = 0, column =0,pady=10,sticky="e")
        label2.grid(row = 1, column =0,pady=10,sticky="e")
        label3.grid(row = 2, column =0,pady=10,sticky="e")
        label4.grid(row = 3, column =0,pady=10,sticky="e")

        entry1.grid(row = 0, column =1,padx = 80)
        entry2.grid(row = 1, column =1,padx = 80)
        entry3.grid(row = 2, column =1,padx = 80)
        entry4.grid(row = 3, column =1,padx = 80)

        nextButton = ttk.Button(buttons, text = "Save", command = lambda : self.local_show_frame(controller,entry1,entry2,entry3,entry4))

        nextButton.grid()
        # print self.grid_size()
        # pcalender.__init__("Anupam")
        # subprocess.Popen("killall matchbox-keyboard")

    def local_show_frame(self,controller,rr,dd,ss,mn):

        global sss,rrr,ddd

        flag = 0

        w=mn.get()
        x=rr.get()
        y=dd.get()
        z=ss.get()
        m = re.search("^[a-zA-Z]{1,4}$",x)
        n = re.search("^[a-zA-Z]{1,4}$",y)
        o = re.search("^[a-zA-Z]{1,4}$",z)
        if m:
        	rrr = x
        	if n:
        		ddd = y
        		if o:
        			sss = z
        		else:
        			flag = 3
        	else:
        		flag = 2
        else:
        	flag = 1

        if flag == 1:
        	errorBox("Invalid Railway Name")
        elif flag == 2:
        	errorBox("Invalid Division Name")
        elif flag == 3:
        	errorBox("Invalid Station Name")
        elif not w:
        	errorBox("Please Enter Model Number")
        else:
            global returnToMenu
            # print returnToMenu
            if returnToMenu==True:
                controller.show_frame(Menu)
            else:
                controller.show_frame(DateTimeSetting)


class DateTimeSetting(tk.Frame):

    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(1,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(2,weight=1,minsize = MINSIZECOLUMN)
        self.grid_rowconfigure(2,weight=3,minsize = MINSIZEROW2)
        self.grid_rowconfigure(3,weight=1,minsize = MINSIZEROW3)

        title = tk.Label(self, text="Date and Time Settings", font = controller.headerFont)
        title.grid(pady=10,padx=10,columnspan = 3, sticky="w")

        separator = ttk.Separator(self,orient=tk.HORIZONTAL)
        separator.grid(row=1,column=0,columnspan=3,sticky="ew")

        entry = tk.Frame(self)
        entry.grid(row=2, column=0, pady=ENTRYFRAMEPADY,padx=ENTRYFRAMEPADX)
        entry.grid_columnconfigure(2,minsize=220)

        buttons = tk.Frame(self)#, borderwidth=5, relief=tk.GROOVE)
        buttons.grid(row=3, column=0,pady = 0,padx=BUTTONFRAMEPADX-40, columnspan=3,sticky="w")

        label1 = tk.Label(entry, text = "DATE :",font = controller.defaultFont)
        label2 = tk.Label(entry, text = "TIME :",font=controller.defaultFont)
        label3 = tk.Label(entry, text = "START DATE :",font=controller.defaultFont)
        label4 = tk.Label(entry, text = "START TIME :",font=controller.defaultFont)

        entry1 = tk.Entry(entry)

        time1 = tk.Frame(entry)

        hh1 = tk.StringVar(time1)
        hh1.set(HHLIST[0])
        HH1 = ttk.Combobox(time1, textvariable = hh1, values=HHLIST,width=7)
        HH1.grid(row=0,column=0,padx=3)
        
        mm1 = tk.StringVar(time1)
        mm1.set(MMLIST[0])
        MM1 = ttk.Combobox(time1, textvariable = mm1, values=MMLIST,width=7)
        MM1.grid(row=0,column = 1,padx=3)
                
        time2 = tk.Frame(entry)
        
        hh2 = tk.StringVar(time2)
        hh2.set(HHLIST[0])
        HH2 = ttk.Combobox(time2, textvariable = hh2, values=HHLIST,width=7)
        HH2.grid(row=0,column=0,padx=3)
        
        mm2 = tk.StringVar(time2)
        mm2.set(MMLIST[0])
        MM2 = ttk.Combobox(time2, textvariable = mm2, values=MMLIST,width=7)
        MM2.grid(row=0,column = 1,padx=3)
        
        entry3 = tk.Entry(entry)

        label1.grid(row = 0, column =0,pady=14,sticky="e")
        label2.grid(row = 1, column =0,pady=14,sticky="e")
        label3.grid(row = 2, column =0,pady=14,sticky="e")
        label4.grid(row = 3, column =0,pady=14,sticky="e")

        entry1.grid(row = 0, column =1,padx = 80)
        time1.grid(row = 1, column =1,padx = 80)
        entry3.grid(row = 2, column =1,padx = 80)
        time2.grid(row = 3, column =1,padx = 80)

        nextButton = ttk.Button(buttons, text = "Start", command = lambda : self.start_recording(controller,HH1,MM1,HH2,MM2,entry1,entry3))
        backButton = ttk.Button(buttons, text = "Back", command = lambda : self.local_show_frame(controller,TMSConfig))
        date1 = ttk.Button(entry, text = ".", command = lambda:controller.call_calendar(entry,date1.winfo_x(),date1.winfo_y(),entry1), width=3)
        date2 = ttk.Button(entry, text = ".", command = lambda :controller.call_calendar(entry,date2.winfo_x(),date2.winfo_y(),entry3), width=3)

        backButton.grid(column = 0,padx = 10)
        nextButton.grid(row = 0,column = 1)
        date1.grid(row=0,column=2,sticky="w")
        date2.grid(row=2,column=2,sticky="w")

    def local_show_frame(self,controller,f):

		global calframe
		if calframe :
			calframe.grid_forget()
		controller.show_frame(f)

    def start_recording(self,controller,hh1,mm1,hh2,mm2,cdate,sdate):

    	a = hh1.get()
    	b = mm1.get()
    	c = hh2.get()
    	d = mm2.get()
    	e = cdate.get()
    	f = sdate.get()

    	if not (a and b and c and d and e and f):
    		if e:
    			if a:
    				if b:
    					if f:
    						if c:
    							if d:
    								pass
    							else:
    								errorBox("Please Enter Starting Minutes")
    						else:
    							errorBox("Please Enter Starting Hour")
    					else:
    						errorBox("Please Enter Starting Date")
    				else:
    					errorBox("Please Enter Current Minutes")
    			else:
    				errorBox("Please Enter Current Hours")
    		else:
    			errorBox("Please Enter Current Date")
    	else:
    		current_date = e + " " + a +":" + b + ":00"
    		start_date = f + " " + c +":" + d + ":00"
    		# print current_date,start_date
    		a=str(datetime.datetime.now())
    		current=str(a[:10])+" "+str(a[11:19])
    		actualtime=datetime.datetime.strptime(current,"%Y-%m-%d %H:%M:%S")
    		current_date=datetime.datetime.strptime(current_date, "%d-%m-%Y %H:%M:%S")
    		start_date=datetime.datetime.strptime(start_date, "%d-%m-%Y %H:%M:%S")
    		if current_date > start_date:
    			errorBox("Starting Date-Time should be greater")
    		else:
    			delta=current_date-actualtime
    			global secondGap
    			secondGap= delta.seconds + delta.days*86400
    			controller.show_frame(MainScreen)
    			recorder()



class MainScreen(tk.Frame):

    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_columnconfigure(0,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(1,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(2,weight=1,minsize = MINSIZECOLUMN)
        self.grid_rowconfigure(2,weight=3,minsize = MINSIZEROW2)
        self.grid_rowconfigure(3,weight=1,minsize = MINSIZEROW3)

        title = tk.Label(self, text="Statistics", font=controller.headerFont)
        title.grid(pady=10,padx=10,columnspan = 3, sticky="w")

        separator = ttk.Separator(self,orient=tk.HORIZONTAL)
        separator.grid(row=1,column=0,columnspan=3,sticky="ew")

        display = tk.Frame(self)
        display.grid(row=2, column=0)

        buttons = tk.Frame(self)#, borderwidth=5, relief=tk.GROOVE)
        buttons.grid(row=3, column=0,pady = 0,padx=BUTTONFRAMEPADX, columnspan=3,sticky="w")

        grid1 = tk.Frame(display)
        grid1.pack()

        grid1.grid_columnconfigure(0,weight=1,minsize = 250)
        grid1.grid_columnconfigure(1,weight=1,minsize = 250)
        grid1.grid_columnconfigure(2,weight=1,minsize = 250)

        global date,time,rrrr,ssss,div,t1,t2,t3

        date = tk.Label(grid1, text = "DD/MM/YYYY",font = controller.defaultFont)
        time = tk.Label(grid1, text = "HH/MM",font = controller.defaultFont)
        rrrr = tk.Label(grid1, text = "RRRR",font = controller.defaultFont)
        div = tk.Label(grid1, text = "DIV",font = controller.defaultFont)
        ssss = tk.Label(grid1, text = "SSSS",font = controller.defaultFont)

        date.grid(row=0, column = 0,pady=20)
        time.grid(row=0,column = 2,pady=20)
        rrrr.grid(row=1, column = 0,pady=20)
        div.grid(row=1, column = 1,pady=20)
        ssss.grid(row=1, column = 2,pady=20)

        grid2 = tk.Frame(display)
        grid2.pack(pady=40)

        temp = tk.Label(grid2, text = "TEMPERATURE :",font = controller.defaultFont)
        mxtemp = tk.Label(grid2, text = "MAX TEMPERATURE :",font = controller.defaultFont)
        mntemp = tk.Label(grid2, text = "MIN TEMPERATURE :",font = controller.defaultFont)

        t1 = tk.Label(grid2, text = 0,font = controller.defaultFont)
        t2 = tk.Label(grid2, text = 0,font = controller.defaultFont)
        t3 = tk.Label(grid2, text = 0,font = controller.defaultFont)
        degree1 = tk.Label(grid2, text = "*C",font = controller.defaultFont)
        degree2 = tk.Label(grid2, text = "*C",font = controller.defaultFont)
        degree3 = tk.Label(grid2, text = "*C",font = controller.defaultFont)

        temp.grid(row=0,column=0,sticky="e",pady=10)
        mxtemp.grid(row=1,column=0,sticky="e",pady=10)
        mntemp.grid(row=2,column=0,sticky="e",pady=10)
        t1.grid(row=0,column=1)
        t2.grid(row=1,column=1)
        t3.grid(row=2,column=1)
        degree1.grid(row=0,column=2)
        degree2.grid(row=1,column=2)
        degree3.grid(row=2,column=2)



        menuButton = ttk.Button(buttons, text = "Menu", command = lambda :self.local_show_frame(controller))

        menuButton.grid()

    def local_show_frame(self,controller):

        global returnToMenu
        returnToMenu = True

        controller.show_frame(Login)




class Menu(tk.Frame):

    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_columnconfigure(0,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(1,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(2,weight=1,minsize = MINSIZECOLUMN)
        self.grid_rowconfigure(2,weight=3,minsize = MINSIZEROW2)
        self.grid_rowconfigure(3,weight=1,minsize = MINSIZEROW3)

        title = tk.Label(self, text="Menu", font=controller.headerFont)
        title.grid(pady=10,padx=10,columnspan = 3, sticky="w")

        separator = ttk.Separator(self,orient=tk.HORIZONTAL)
        separator.grid(row=1,column=0,columnspan=3,sticky="ew")

        display = tk.Frame(self)#,borderwidth=3,relief = tk.GROOVE)
        display.grid(row=2, column=0,pady = ENTRYFRAMEPADY,padx=200)

        buttons = tk.Frame(self)#, borderwidth=5, relief=tk.GROOVE)
        buttons.grid(row=3, column=0,pady = 0,padx=BUTTONFRAMEPADX, columnspan=3,sticky="w")
        # returnToMenu = True
        # print returnToMenu

        button1 = tk.Button(display, text = "TMS Configuration", command = lambda : self.local_show_frame(controller),width=30)
        button2 = tk.Button(display, text = "Export", command = lambda:inputBox(),width=30)
        button3 = tk.Button(display, text = "View Output", command = lambda : controller.show_frame(Output),width=30)
        button4 = tk.Button(display, text = "Settings", command = lambda : controller.show_frame(Settings),width=30)

        button1.pack(pady=10)
        button2.pack(side = "bottom",pady=10)
        button3.pack(side = "bottom",pady=10)
        button4.pack(side = "bottom",pady=10)


        backButton = ttk.Button(buttons, text = "Back", command = lambda : controller.show_frame(MainScreen))

        backButton.grid()

    def local_show_frame(self, controller):

        controller.show_frame(TMSConfig)


class Settings(tk.Frame):

    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_columnconfigure(0,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(1,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(2,weight=1,minsize = MINSIZECOLUMN)
        self.grid_rowconfigure(2,weight=3,minsize = MINSIZEROW2)
        self.grid_rowconfigure(3,weight=1,minsize = MINSIZEROW3)

        title = tk.Label(self, text="Settings", font=controller.headerFont)
        title.grid(pady=10,padx=10,columnspan = 3, sticky="w")

        separator = ttk.Separator(self,orient=tk.HORIZONTAL)
        separator.grid(row=1,column=0,columnspan=3,sticky="ew")

        entry = tk.Frame(self)
        entry.grid(row=2, column=0, pady=ENTRYFRAMEPADY,padx=ENTRYFRAMEPADX)

        buttons = tk.Frame(self)#, borderwidth=5, relief=tk.GROOVE)
        buttons.grid(row=3, column=0,padx=BUTTONFRAMEPADX, columnspan=3,sticky="w")

        label1 = tk.Label(entry, text = "Max Temperature :",font = controller.defaultFont)
        label2 = tk.Label(entry, text = "Min Temperature :",font=controller.defaultFont)      
        
        entry1 = tk.Entry(entry)
        entry2 = tk.Entry(entry)

        entry1.bind("<FocusIn>",controller.call_keyboard)
        entry2.bind("<FocusIn>",controller.call_keyboard)

        entry1.bind("<FocusOut>",controller.close_keyboard)
        entry2.bind("<FocusOut>",controller.close_keyboard)

        label1.grid(row = 0, column =0,pady=10,sticky="e")
        label2.grid(row = 1, column =0,pady=10,sticky="e")

        entry1.grid(row = 0, column =1,padx = 80)
        entry2.grid(row = 1, column =1,padx = 80)

        nextButton = ttk.Button(buttons, text = "Save", command = lambda : controller.show_frame(Menu))

        nextButton.grid()




class Output(tk.Frame):

    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.grid_columnconfigure(0,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(1,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(2,weight=1,minsize = MINSIZECOLUMN)
        self.grid_rowconfigure(2,weight=3,minsize = MINSIZEROW2)
        self.grid_rowconfigure(3,weight=1,minsize = MINSIZEROW3)

        title = tk.Label(self, text="Output", font=controller.headerFont)
        title.grid(pady=10,padx=10,columnspan = 3, sticky="w")

        separator = ttk.Separator(self,orient=tk.HORIZONTAL)
        separator.grid(row=1,column=0,columnspan=3,sticky="ew")

        entry = tk.Frame(self)
        entry.grid(row=2, column=0, pady=ENTRYFRAMEPADY,padx=ENTRYFRAMEPADX)
        entry.grid_columnconfigure(2,minsize=220)

        buttons = tk.Frame(self)#, borderwidth=5, relief=tk.GROOVE)
        buttons.grid(row=3, column=0,pady = 0,padx=BUTTONFRAMEPADX, columnspan=3,sticky="w")

        label1 = tk.Label(entry, text = "START DATE :",font = controller.defaultFont)
        label2 = tk.Label(entry, text = "START TIME :",font=controller.defaultFont)
        label3 = tk.Label(entry, text = "END DATE :",font=controller.defaultFont)
        label4 = tk.Label(entry, text = "END TIME :",font=controller.defaultFont)
        label5 = tk.Label(entry, text = "TIME INTERVAL :",font=controller.defaultFont)

        entry1 = tk.Entry(entry)

        time1 = tk.Frame(entry)

        hh1 = tk.StringVar(time1)
        hh1.set(HHLIST[0])
        HH1 = ttk.Combobox(time1, textvariable = hh1, values=HHLIST,width=7)
        HH1.grid(row=0,column=0,padx=3)
        
        mm1 = tk.StringVar(time1)
        mm1.set(MMLIST[0])
        MM1 = ttk.Combobox(time1, textvariable = mm1, values=MMLIST,width=7)
        MM1.grid(row=0,column = 1,padx=3)
                
        entry3 = tk.Entry(entry)

        time2 = tk.Frame(entry)
        
        hh2 = tk.StringVar(time2)
        hh2.set(HHLIST[0])
        HH2 = ttk.Combobox(time2, textvariable = hh2, values=HHLIST,width=7)
        HH2.grid(row=0,column=0,padx=3)
        
        mm2 = tk.StringVar(time2)
        mm2.set(MMLIST[0])
        MM2 = ttk.Combobox(time2, textvariable = mm2, values=MMLIST,width=7)
        MM2.grid(row=0,column = 1,padx=3)

        entry5 = tk.Entry(entry)
        
        label1.grid(row = 0, column =0,pady=10,sticky="e")
        label2.grid(row = 1, column =0,pady=10,sticky="e")
        label3.grid(row = 2, column =0,pady=10,sticky="e")
        label4.grid(row = 3, column =0,pady=10,sticky="e")
        label5.grid(row = 4, column =0,pady=10,sticky="e")

        entry1.grid(row = 0, column =1,padx = 80)
        time1.grid(row = 1, column =1,padx = 80)
        entry3.grid(row = 2, column =1,padx = 80)
        time2.grid(row = 3, column =1,padx = 80)
        entry5.grid(row = 4, column =1,padx = 80)

        entry5.bind("<FocusIn>",controller.call_keyboard)

        entry5.bind("<FocusOut>",controller.close_keyboard)

        nextButton = ttk.Button(buttons, text = "Output", command = lambda : self.validate(controller,HH1,MM1,HH2,MM2,entry1,entry3,entry5))
        backButton = ttk.Button(buttons, text = "Back", command = lambda : self.local_show_frame(controller,Menu))
        date1 = ttk.Button(entry, text = ".", command = lambda:controller.call_calendar(entry,date1.winfo_x(),date1.winfo_y(),entry1), width=3)
        date2 = ttk.Button(entry, text = ".", command = lambda :controller.call_calendar(entry,date2.winfo_x(),date2.winfo_y(),entry3), width=3)

        backButton.grid(column = 0,padx = 10)
        nextButton.grid(row = 0,column = 1)
        date1.grid(row=0,column=2,sticky="w")
        date2.grid(row=2,column=2,sticky="w")

    def local_show_frame(self,controller,f):

        global calframe
        if calframe:
            calframe.grid_forget()
        controller.show_frame(f)

    def validate(self,controller,hh1,mm1,hh2,mm2,sdate,edate,intr):

        a = hh1.get()
        b = mm1.get()
        c = hh2.get()
        d = mm2.get()
        e = sdate.get()
        f = edate.get()
        g = intr.get()
        h = re.search("^[0-9]+$",g)
        # print h.group(0)

        if not (a and b and c and d and e and f and h):
            if e:
                if a:
                    if b:
                        if f:
                            if c:
                                if d:
                                    if h != None:
                                        pass
                                    else:
                                        errorBox("Enter Valid Time Interval in Minutes")
                                else:
                                    errorBox("Please Enter Ending Minutes")
                            else:
                                errorBox("Please Enter Ending Hour")
                        else:
                            errorBox("Please Enter Ending Date")
                    else:
                        errorBox("Please Enter Starting Minutes")
                else:
                    errorBox("Please Enter Starting Hours")
            else:
                errorBox("Please Enter Starting Date")
        else:
            start_date = e + " " + a +":" + b + ":00"
            end_date = f + " " + c +":" + d + ":00"
            # print current_date,start_date
            a=str(datetime.datetime.now())
            current=str(a[:10])+" "+str(a[11:19])
            actualtime=datetime.datetime.strptime(current,"%Y-%m-%d %H:%M:%S")
            start_date=datetime.datetime.strptime(start_date, "%d-%m-%Y %H:%M:%S")
            end_date=datetime.datetime.strptime(end_date, "%d-%m-%Y %H:%M:%S")
            if start_date > end_date:
                errorBox("Ending Date-Time should be greater")
            else:
                delta=start_date-actualtime
                # global secondGap
                # secondGap= delta.seconds + delta.days*86400
                global calframe
                if calframe:
                    calframe.grid_forget()
                output_on_screen("r","d","s",g,e,f,a,c,b,d)              
                controller.show_frame(ViewOutput)
                # recorder()


class ViewOutput(tk.Frame):

    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.grid_columnconfigure(0,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(1,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(2,weight=1,minsize = MINSIZECOLUMN)
        self.grid_rowconfigure(2,weight=3,minsize = MINSIZEROW2)
        self.grid_rowconfigure(3,weight=1,minsize = MINSIZEROW3)

        title = tk.Label(self, text="Output", font=controller.headerFont)
        title.grid(pady=10,padx=10,columnspan = 3, sticky="w")

        separator = ttk.Separator(self,orient=tk.HORIZONTAL)
        separator.grid(row=1,column=0,columnspan=3,sticky="ew")

        buttons = tk.Frame(self)#, borderwidth=5, relief=tk.GROOVE)
        buttons.grid(row=3, column=0,padx=BUTTONFRAMEPADX, columnspan=3,sticky="w")

        outputFrame = tk.Frame(self)
        outputFrame.grid(row=0,column=0,sticky="nsew")
        # outputFrame.grid_rowconfigure(0, weight=1)
        # outputFrame.grid_columnconfigure(0, weight=1)
        vscrollbar = AutoScrollbar(outputFrame)
        vscrollbar.grid(row=0, column=1, sticky="ns")
        # hscrollbar = AutoScrollbar(outputFrame, orient="horizontal")
        # hscrollbar.grid(row=1, column=0, sticky="ew")
        canvas = tk.Canvas(outputFrame, yscrollcommand=vscrollbar.set)#, xscrollcommand=hscrollbar.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        vscrollbar.config(command=canvas.yview)
        # hscrollbar.config(command=canvas.xview)
        outputFrame.grid_rowconfigure(0, weight=1)
        outputFrame.grid_columnconfigure(0, weight=1)
        frame = tk.Text(canvas, state="normal",width=100)
        file = open('output.text','r')
        frame.insert(tk.INSERT,file.read())
        frame.config(state="disabled")

        canvas.create_window(0, 0, anchor="nw", window=frame)
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        outputFrame.grid(row=2,column=0,pady=ENTRYFRAMEPADY,padx=35,columnspan=3)


        backButton = ttk.Button(buttons, text = "Back", command = lambda : controller.show_frame(Menu))

        backButton.grid()

class Login(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(1,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(2,weight=1,minsize = MINSIZECOLUMN)
        # self.grid_rowconfigure(0,weight=1,minsize = 80)
        self.grid_rowconfigure(2,weight=3,minsize = MINSIZEROW2)
        self.grid_rowconfigure(3,weight=1,minsize = MINSIZEROW3)
        
        title = tk.Label(self, text="Login", font=controller.headerFont)
        title.grid(row=0,column=0,pady=10,padx=10,columnspan=3, sticky = "w")

        separator = ttk.Separator(self,orient=tk.HORIZONTAL)
        separator.grid(row=1,column=0,columnspan=3,sticky="ew")

        entry = tk.Frame(self)
        entry.grid(row=2, column=0, pady=ENTRYFRAMEPADY,padx=ENTRYFRAMEPADX)

        buttons = tk.Frame(self)#, borderwidth=5, relief=tk.GROOVE)
        buttons.grid(row=3, column=0,padx=BUTTONFRAMEPADX,pady=20, columnspan=3,sticky="w")

        #label1 = tk.Label(entry, text = "Username :",font = controller.defaultFont)
        label2 = tk.Label(entry, text = "Password :",font=controller.defaultFont)       
        
        #entry1 = tk.Entry(entry)
        entry2 = tk.Entry(entry,show="*")

        #label1.grid(row = 0, column =0,pady=10,sticky="e")
        label2.grid(row = 1, column =0,pady=10,sticky="e")

        #entry1.grid(row = 0, column =1,padx = 80)
        entry2.grid(row = 1, column =1,padx = 80)

        #entry1.bind("<FocusIn>",controller.call_keyboard)
        entry2.bind("<FocusIn>",controller.call_keyboard)

        #entry1.bind("<FocusOut>",controller.close_keyboard)
        entry2.bind("<FocusOut>",controller.close_keyboard)

        #nextButton = ttk.Button(buttons, text = "Save", command = lambda : self.local_show_frame(controller,"""entry1,"""entry2))
        nextButton = ttk.Button(buttons, text = "Save", command = lambda : self.local_show_frame(controller,entry2))

        nextButton.grid()
        
    #def local_show_frame(self,controller,"""user,"""passw):
    def local_show_frame(self,controller,passw):

        global sss,rrr,ddd

        flag = 0

        #u=user.get()
        p=passw.get()

        #user.delete(0,"end")
        passw.delete(0,"end")
        
        #if """u == "anupam" and""" p == "singh":
        if p == "crt":
            flag = 1

        
        if flag == 1:
            global returnToMenu
            # print returnToMenu
            if returnToMenu == True:
                controller.show_frame(Menu)
            else:
                controller.show_frame(TMSConfig)
        else:
            errorBox("Invalid Username Password")



global app
app = CRTApp()

app.mainloop()


