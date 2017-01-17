### ### ### ### ### ### THIRD PARTY LIBRARIES ### ### ### ### ### ###

import calendar
import time
import datetime
import re               #Regular Expression
import tkMessageBox     #Error and Info Box
import subprocess       #Keyboard Call
import os               #Keyboard Kill
import hashlib          #Password Security
import sys              #Check fo linux(Jessie)
import glob
import shutil
import binascii
import MySQLdb
# import pyaudio

try:
    import Tkinter as tk
    import tkFont
    import ttk
except ImportError: #py3
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk


### ### ### ### ### ### USER DEFINED LIBRARIES ### ### ### ### ### ###

""" modules defined locally in the interest of the project """

import pcalendar            #Calender Widget
import dialog               #Export Dialog Box
import toaudio              #Export via 3.5mm Jack
import dbms                 #Updating and Querying DB
import usb                  #Export via USB
import temperature          #Fetch Temperature
import export               #Export Functionality
import buzzer               #Control Buzzer
# import Voltagechecker       #Voltage Checking


### ### ### ### ### ### GLOBAL DECLARATION ### ### ### ### ### ###

""" Global Variables used to set various parameters used in the CRTApp """

HOMEDIR = "/home/pi/Downloads/CRTApp" #Home Directory for the Application Folder

TILIST = ["Minutes"]  #Time Interval List
HHLIST = ["00","01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
            "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"] #Hour List
MMLIST = ["00","01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
            "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
            "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
            "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
            "41", "42", "43", "44", "45", "46", "47", "48", "49", "50",
            "51", "52", "53", "54", "55", "56", "57", "58", "59"]  #Minute List

returnToMenu = False  #Boolean Variable for flow of Control(used by frames: Login and TMSConfig)
MINSIZEROW2 = 300   #Minimum Row Height (row 2)
MINSIZEROW3 = 0 #Minimum Row Height (row 3)
MINSIZECOLUMN = 266 #Minimum Column Width (all)
ENTRYFRAMEPADX = 40
ENTRYFRAMEPADY = 40
BUTTONFRAMEPADX = 300
calframe = None #Calendar Frame
PASSWORD = "2282de20b84a7bf6a5c8d95b821be1ff072948435b1dc7cb60205d837b90077dee7dbefbcff55fe15e7b41074f1302d7ea458562a6c86c203473ef24ea64d234"
nn=0
rrr = "RRRR"    #Railway Name
sss = "RRRR"    #Station Name
ddd = "RRRR"    #Division Name
# mmm = "RRRR"
MAXIMUM = 85.0  #Maximum Temperature to set off the alarm
MINIMUM = -5.0  #Minimum Temperature to set off the alarm
maxminsiren1=0
maxminsiren2=0

### ### ### ### ### ### GLOBAL METHODS ### ### ### ### ### ###
    
""" these methods are used independent of the CRTApp class definition """

def errorBox(msg):

    """show custom error box """

    tkMessageBox.showerror("Error", msg)

def infoBox(msg):

    """show custome message box """

    tkMessageBox.showinfo("Done",msg)

def qf():
    print ("done")

def get_calendar(locale, fwday):

    """ instantiate proper calendar class """

    if locale is None:
        return calendar.TextCalendar(fwday)
    else:
        return calendar.LocaleTextCalendar(fwday, locale)

def update_maxmin(temp):

    global secondGap,currentMaxTempValue,currentMinTempValue,prev_date,MAXIMUM,MINIMUM,maxminsiren1,maxminsiren2
    current_time=str(datetime.datetime.now()+datetime.timedelta(seconds=secondGap))
    date=str(prev_date)
    dd1=str(current_time[:2])
    dd2=str(date[:2])
    #print MAXIMUM,MINIMUM
    if dd1 == dd2:
        currentMaxTempValue=float(currentMaxTempValue)
        currentMinTempValue=float(currentMinTempValue)
        #print currentMinTempValue,currentMaxTempValue
        #print "           "
        temp = float(temp)
        #print temp
        MAXIMUM=float(MAXIMUM)
        MINIMUM=float(MINIMUM)
        if temp>currentMaxTempValue:
            print MAXIMUM
            if temp<MAXIMUM:
                if temp!=85.0:
                    currentMaxTempValue=temp
            elif temp>=MAXIMUM:
                if temp!=85.0:
                    currentMaxTempValue=temp
                    #print "ANDAR AA GAYA"
                
                if maxminsiren1==0:
                    if temp!=85.0:
                        buzzer.alarmstart()
                        errorBox("MAXIMUM TEMPERATURE EXCEEDED")
                        buzzer.alarmstop()
                        maxminsiren1=maxminsiren1+1
        elif temp>MAXIMUM:
            if maxminsiren1==0:
                if temp!=85.0:
                    buzzer.alarmstart()
                    errorBox("MAXIMUM TEMPERATURE EXCEEDED")
                    buzzer.alarmstop()
                    maxminsiren1=maxminsiren1+1
                        
                #currentMaxTempValue=aaa
        if temp<currentMinTempValue:
            if temp>=MINIMUM:
                currentMinTempValue=temp
            elif temp<MINIMUM:
                currentMinTempValue=temp
                if maxminsiren2==0:
                    buzzer.alarmstart()
                    errorBox("MINIMUM TEMPERATURE LIMIT")
                    buzzer.alarmstop()
                    maxminsiren2=maxminsiren2+1
        elif temp<MINIMUM:
            if maxminsiren2==0:
                buzzer.alarmstart()
                errorBox("MINIMUM TEMPERATURE LIMIT")
                buzzer.alarmstop()
                maxminsiren2=maxminsiren2+1
    else:
        currentMaxTempValue=temp
        currentMinTempValue=temp
                 
    return (currentMaxTempValue,currentMinTempValue)

def recorder(num = 1):

    """ this is a recursive module which uses "after" to update the mainscreen 
    per second with current date time and max min and current temperature"""

    global app  # CRTApp class instance
    global currentTemp   # Label : Current Temperature
    global currentMaxTemp   # Label : Current maximum temperature
    global currentMinTemp   # Label : Current minimum temperature
    global systemDate   # Date Label on Main Screen
    global systemTime   # Time Label on Main Screen
    global rrrr     # Label : Railway Name
    global ssss     # Label : Station Name
    global dddd     # Label : Division
    global rrr  # Value : Railway Name
    global sss  # Value : Station Name
    global ddd  # Value : Division
    global currentMaxTempValue  # Value : Current Maximum Temperaature
    global currentMinTempValue  # Value : Current Minimum Temperaature
    global prev_date

    if num is 1:
        rrrr.configure(text=rrr)
        ssss.configure(text=sss)
        dddd.configure(text=ddd)
        currentMaxTempValue=-5
        currentMinTempValue=85
        prev_date=""
    if num:
        
        execstart = time.time()*1000
        
        #voltage_val=float(Voltagechecker.checkvol())
        #if voltage_val==2:
            #buzzer.shortalarm(9000)
            #errorBox("LOW BATTERY")
            #buzzer.alarmstop()
        tt,check_connection2=temperature.read_temp()

        global secondGap # difference in system time and current time in seconds
        global maxminsiren1
        global maxminsiren2
        global c
        global d
        global f
        global statusLabel
        global nn

        today = (datetime.datetime.now()+datetime.timedelta(seconds=secondGap))
        today1=str(today)
        todaytime = str(today1[11:19])
        today1= str(today1[:10])
        # global currentMaxTempValue,currentMinTempValue,nn
        prev_date=today1[8:10]+"/"+today1[5:7]+"/"+today1[:4]
        prev_time=todaytime
        if float(tt)<MAXIMUM:
            if maxminsiren1>0:
                maxminsiren1=0
        if float(tt)>MINIMUM:
            if maxminsiren2>0:
                maxminsiren2=0
        if float(tt)==85.0 and check_connection2=="00":
            currentTemp.configure(text = "--")
            buzzer.alarmstart()
            errorBox("Check the connection")
            buzzer.alarmstop()
        elif check_connection2=="00" and float(tt)==00.0:
            currentTemp.configure(text = "--")
            buzzer.alarmstart()
            errorBox("Check the connection")
            buzzer.alarmstop()    
        else:
            currentTemp.configure(text = tt)
            currentMaxTempValue,currentMinTempValue=update_maxmin(tt)
            currentMaxTemp.configure(text = currentMaxTempValue)
            currentMinTemp.configure(text = currentMinTempValue)
        systemDate.configure(text = prev_date)
        systemTime.configure(text=prev_time)
        curr = str(f+" "+c+":"+d+":00")
        starttime=datetime.datetime.strptime(curr,"%d-%m-%Y %H:%M:%S")
        if today>=starttime:
            if nn != 2:
                nn=1
            x=0
            if float(tt)==85.0:
                pass
            elif check_connection2=="00":
                pass
            else:
                x=dbms.todbms(tt,prev_date,prev_time,num)
            if x==2:
            	# pass
                # global rrr,sss,ddd
                toaudio.sendaudio(tt,prev_date,prev_time,rrr,ddd,sss,num)
        if nn==1:
            nn=2
            print "done"
            statusLabel.configure(text="RECORDING")
            statusLabel.configure(fg="red")
            statusLabel.configure(image=app.rec)
            #toaudio(tt,prev_date,prev_time,rrr,ddd,sss,num)

        execend = time.time()*1000
        ii = int(round(1000-(execend-execstart)))
        if ii > 0:
            app.after(ii,lambda:recorder(num+1))
        else:
            app.after(0,lambda:recorder(num+1))


def output_on_screen(r,d,s,interval,dx,d2,hh12,hh2,mm1,mm2):

    db = MySQLdb.connect("localhost","root","password") 							#connect the database
    cursor = db.cursor()
    print (str(dx))
  
    sql= """USE CRT1;"""
    cursor.execute(sql)
	
    outfile = open("/home/pi/Desktop/output.dat","w") 													#ismei save krenge output

    global rrr,sss,ddd
    rrr=rrr.upper()
    sss=sss.upper()
    ddd=ddd.upper()
    outstring1 = "1 "+rrr+" "+ddd+" "+sss
    outfile.write(outstring1+"\n")
    dx=str(dx)
    d2=str(d2)
    print dx
    print d2
    
    
    #time1=str(time1)
    #time2=str(time2)
    hh12=str(hh12)
    #print hh12
    hh2=str(hh2)
    mm1=str(mm1)
    #print mm1
    mm2=str(mm2)

    timex=hh12+":"+mm1+":00"
    #print timex
    time2=hh2+":"+mm2+":00"

    dx=dx+" "+timex
    d2=d2+" "+time2

    #print dx
    #print d2
    startepoch=int(time.mktime(time.strptime(dx,"%d-%m-%Y %H:%M:%S")))
    endepoch=int(time.mktime(time.strptime(d2,"%d-%m-%Y %H:%M:%S")))
    #sql = ("""SELECT * FROM TEMPERATURES1;""")
    #sql = ("""SELECT * FROM TEMPERATURES1 WHERE (DATE = '%s' AND TIME='%s')
    sql = ("""SELECT * FROM TEMPERATURES1 WHERE (DATETIME >= '%s') AND (DATETIME <= '%s');""" %(str(startepoch),str(endepoch)))	
    #sql = ("""SELECT * FROM TEMPERATURES1 WHERE (TIME>'%s');""" %(time1))
    cursor.execute(sql)
    result = cursor.fetchall()
    #print result
    #print "33"
    #giveresult(result,interval)
    num=0																				#To deal with the timeinterval(in minutes)	
    print (len(str(result)))
    if len(str(result))<3:
        print "NO RESULT"
        outfile.write(" NO DATA RECORDED FOR THE GIVEN TIME PERIOD ")
    else:
        maxtemp = result[0][1]
        mintemp = result[0][1]
	
        absmaxtemp = result[0][1]
        absmintemp = result[0][1]

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
    
        outstring3="3 " +str(maxdate)+" "+str(maxtime)+" +" + str(maxtemp)+" Deg C HR MAX"
        outstring4="4 " +str(mindate)+" "+str(mintime)+" +" + str(mintemp)+" Deg C HR MIN"

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
                difference1 = epochcalc2-count
                count=epochcalc2
                if difference1 == 2*apt_diff:
                    kk2=time.strftime("%d/%m/%Y %H:%M:%S",time.localtime(float(result[i-1][0])-60*intt))
                    outdate_2 = kk2[:10]
                    outtime_2 = kk2[11:16]
                    outtemp_2 = result[i-1][1]
                    if outtemp_2>=0:
                        outstring = "2 "+str(outdate_2)+" "+outtime_2+" +" +str(outtemp_2)+" Deg C"
                    else:
                        outstring = "2 "+str(outdate_2)+" "+outtime_2+" -" +str(outtemp_2)+" Deg C"
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
        #return "2"


class AutoScrollbar(tk.Scrollbar):
    """A scrollbar that hides itself if it's not needed.
    Only works if you use the grid geometry manager!"""
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

class MyDialog(dialog.Dialog):

    """ a dialog box that is drawn on Toplevel and grabs focus from "app" 
    until its completed or canceled 
    Dialog class imported from dialog"""

    def body(self, master):

        """body of the dialog box"""

        defaultFont = tkFont.Font(family = "Helvetica", size = 12, weight = "bold")
        buttonFont = tkFont.Font(family = "Helvetica", size = 10, weight = "bold")

        label = tk.Label(master,text="Enter Time Interval",font = defaultFont)
        label.grid(padx=10,pady=10,columnspan=2,sticky="w")

        v= tk.StringVar()

        self.entry = tk.Entry(master,width=30,textvariable=v,font=defaultFont)
        self.entry.grid(row=1,column=0,padx=10)
        self.entry.bind("<Button-1>",lambda x: subprocess.Popen("matchbox-keyboard"))
        self.entry.bind("<FocusIn>",lambda x: subprocess.Popen("matchbox-keyboard"))

        self.ti = tk.StringVar(master)
        self.ti.set(TILIST[0])
        TI = ttk.Combobox(master, textvariable = self.ti, values=TILIST,width=10,font=defaultFont)
        TI.grid(row=1,column=1)
        return self.entry

    def apply(self):

        """over ridden function defines what actions to take 
        when apply is clicked"""

        self.result = int(self.entry.get())
        second = self.ti.get()
        global rrr,sss,ddd
        export.output_to_file(rrr,ddd,sss,self.result)
        usb.usbexport()
        tkMessageBox.showinfo("Done","Exporting Done")

    def validate(self):

        """over ridden function that validates the input from the
        dialog box"""

    	first = self.entry.get()
    	m = re.search("^\d+$",first)
    	if m:
    		return 1
    	self.entry.delete(0,"end")
    	return 0


class CRTApp(tk.Tk):

    DD = ""
    MM = ""
    YYYY = ""


    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self,"CRTApp")
        # image = Image.open("img/save.png")
        self.save = tk.PhotoImage(file=HOMEDIR+"/img/save.gif")
        # image = Image.open("img/right.png")
        self.next = tk.PhotoImage(file=HOMEDIR+"/img/right.gif")
        # image = Image.open("img/left.png")
        self.back = tk.PhotoImage(file=HOMEDIR+"/img/left.gif")
        # image = Image.open("img/start.png")
        self.start = tk.PhotoImage(file=HOMEDIR+"/img/start.gif")
        # image = Image.open("img/output.png")
        self.output = tk.PhotoImage(file=HOMEDIR+"/img/output.gif")
        # image = Image.open("img/menu.png")
        self.menu = tk.PhotoImage(file=HOMEDIR+"/img/menu.gif")
        # image = Image.open("img/ok.png")
        self.ok = tk.PhotoImage(file=HOMEDIR+"/img/ok.gif")
        # image = Image.open("img/rec.png")
        self.rec = tk.PhotoImage(file=HOMEDIR+"/img/rec.gif")
        # image = Image.open("img/nrec.png")
        self.nrec = tk.PhotoImage(file=HOMEDIR+"/img/nrec.gif")
        self.cal = tk.PhotoImage(file=HOMEDIR+"/img/cal.gif")
        #self.wm_geometry("800x480")
        # self.attributes("-zoomed",True)
        # self.attributes("-fullscreen",True)
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        # self.overrideredirect(1)
        # self.geometry("%dx%d+0+0" % (w, h))
        self.geometry("%dx%d+0+0" % (800, 480))
        self.wm_resizable( width=False, height=False)
        self.it=-1
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand="true")
        # container.grid(row=0,column=0)
        # container.grid_rowconfigure(0, weight=1,minsize =480)
        # container.grid_columnconfigure(0, weight=1,minsize=800)

        self.defaultFont = tkFont.Font(family = "Helvetica", size = 12, weight = "bold")
        self.headerFont = tkFont.Font(family = "Helvetica", size = 16, weight = "bold")
        self.buttonFont = tkFont.Font(family = "Helvetica", size = 10, weight = "bold")

        self.option_add("*TCombobox*Listbox*Font", self.defaultFont)

        # container.grid_rowconfigure(0, weight=1)
        # container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in ( Login, TMSConfig, DateTimeSetting, MainScreen, Menu, Settings,Output, Splash, ViewOutput, PasswordChange):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        time.sleep(2)
        self.logo.place_forget()
        self.show_frame(Login)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def update(self, calframe,e,d,m,y):

        calframe.place_forget()
        # calframe.destroy()

        # YYYY = ttkcal._date.year
        # MM = ttkcal._date.month
        # DD = ttkcal._selection[0]

        YYYY = y
        MM = m
        DD = d

        e.delete(0, "end")
        e.insert(0,"%02d" % int(DD) + '-' + "%02d" % int(MM) + '-' + str(YYYY))

    def call_calendar(self,container,x,y,e):

        global calframe
        calframe = ttk.Frame(self,borderwidth=3,relief=tk.GROOVE)
        if 'win' not in sys.platform:
            style = ttk.Style()
            style.configure('Treeview',rowheight=40)
        ttkcal = pcalendar.Calendar(calframe,self.update,e,firstweekday=pcalendar.calendar.SUNDAY)
        ttkcal.grid(row=0,column=0)

        # close = ttk.Button(calframe,text='x',width=1,command=lambda:qf())#self.update(calframe,e,ttkcal))
        # close.grid(row=0,column=1,sticky="nw")
        # calframe.grid(row=0,column=1,rowspan=4)

        # calframe.grid(row=0,column=2,rowspan=5)#pady=y+150,padx=x-10)
        calframe.place(relx=0.67,rely=0.5, anchor="center")
        # calframe.pack()

        # calframe = tk.Toplevel(self)
        # calframe.wm_geometry("800x480")

        # ttkcal = pcalender.Calendar(calframe,self.update,e,firstweekday=pcalender.calendar.SUNDAY)
        # ttkcal.pack(expand=1,fill="both")

    def call_keyboard(self,event):
    	self.close_keyboard()
        subprocess.Popen("matchbox-keyboard")

    def close_keyboard(self,event=None):
        os.system("killall matchbox-keyboard")

    def checkNextBack(self):

        x = self.read_file(0)
        self.it = self.it + 1
        if x == -1 :
            return 1
        else:
            return 2
        x = self.read_file(1)
        self.it = self.it - 1
        if x == -1 :
            return 3
        else:
            return 4

    def read_file_helper(self):

        self.line_offset = []
        offset = 0
        x = 0
        file = open('/home/pi/Desktop/output.dat','r')
        for line in file:
            if(x == 0):
                self.line_offset.append(offset)
            offset += len(line)
            x = (x+1)%25
        file.close()
        # file.seek(0)

    def read_file(self,direction):
        infile = open('/home/pi/Desktop/output.dat', 'r')
        if direction == 0:
            self.it = self.it - 1
        if direction == 1:
            self.it=self.it +1
        if self.it<0:
            return -1
        if self.it==len(self.line_offset):
            return -1
        infile.seek(self.line_offset[self.it])
        # print self.it
        lines = []
        for line in infile:
            lines.append(line)
            if len(lines) > 25:
                # print lines
                return lines
                # lines = []
        if len(lines) > 0:
            # print lines
            return lines
        
class Splash(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        photo = tk.PhotoImage(file=HOMEDIR+"/img/logo.gif")
        controller.logo = tk.Label(parent,image=photo)
        controller.logo.image = photo # keep a reference!
        controller.logo.place(relx=0.5, rely=0.4, anchor="center")
        apptitle = tk.Label(parent,text="CONTINUOUS RAIL THERMOMETER",font=controller.headerFont)
        apptitle.place(relx=0.5, rely=0.75, anchor="center")
        appversion = tk.Label(parent,text="Version 4.0",font=controller.defaultFont)
        appversion.place(relx=0.5, rely=0.8, anchor="center")


class TMSConfig(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        f = tk.Frame(self)

        f.grid_columnconfigure(0,weight=1,minsize = MINSIZECOLUMN)
        f.grid_columnconfigure(1,weight=1,minsize = MINSIZECOLUMN)
        f.grid_columnconfigure(2,weight=1,minsize = MINSIZECOLUMN)
        # self.grid_rowconfigure(0,weight=1,minsize = 80)
        f.grid_rowconfigure(2,weight=3,minsize = MINSIZEROW2)
        f.grid_rowconfigure(3,weight=1,minsize = MINSIZEROW3)
        # self.config(borderwidth=3,relief=tk.GROOVE)
        
        self.title = tk.Label(f, text="TMS Configuration", font=controller.headerFont)
        self.title.grid(row=0,column=0,pady=10,padx=10,columnspan=3, sticky = "w")

        self.separator = ttk.Separator(f,orient=tk.HORIZONTAL)
        self.separator.grid(row=1,column=0,columnspan=3,sticky="ew")

        self.entry = tk.Frame(f)
        self.entry.grid(row=2, column=0, pady=ENTRYFRAMEPADY,padx=ENTRYFRAMEPADX)

        self.buttons = tk.Frame(f)#, borderwidth=5, relief=tk.GROOVE)
        self.buttons.grid(row=3, column=0,padx=BUTTONFRAMEPADX-40, columnspan=3,sticky="w")

        label1 = tk.Label(self.entry, text = "Railway Name :",font = controller.defaultFont)
        label2 = tk.Label(self.entry, text = "Division Name :",font=controller.defaultFont)
        label3 = tk.Label(self.entry, text = "Station Name :",font=controller.defaultFont)
        # label4 = tk.Label(self.entry, text = "Model Number :", font=controller.defaultFont)        
        
        self.w = tk.StringVar()
        self.x = tk.StringVar()
        self.y = tk.StringVar()
        # self.z = tk.StringVar()
        entry1 = tk.Entry(self.entry,textvariable=self.w,font=controller.defaultFont)
        entry2 = tk.Entry(self.entry,textvariable=self.x,font=controller.defaultFont)
        entry3 = tk.Entry(self.entry,textvariable=self.y,font=controller.defaultFont)
        # entry4 = tk.Entry(self.entry,textvariable=self.z,font=controller.defaultFont)

        self.w.trace("w", lambda x,y,z:self.autocapitalize(self.w))
        self.x.trace("w", lambda x,y,z:self.autocapitalize(self.x))
        self.y.trace("w", lambda x,y,z:self.autocapitalize(self.y))

        entry1.bind("<Button-1>",self.adjust)
        entry2.bind("<Button-1>",self.adjust)
        entry3.bind("<Button-1>",self.adjust)
        # entry4.bind("<Button-1>",self.adjust)

        f.bind("<Button-1>", self.readjust)

        label1.grid(row = 0, column =0,pady=10,sticky="e")
        label2.grid(row = 1, column =0,pady=10,sticky="e")
        label3.grid(row = 2, column =0,pady=10,sticky="e")
        # label4.grid(row = 3, column =0,pady=7,sticky="e")

        entry1.grid(row = 0, column =1,padx = 80)
        entry2.grid(row = 1, column =1,padx = 80)
        entry3.grid(row = 2, column =1,padx = 80)
        # entry4.grid(row = 3, column =1,padx = 80)

        
        nextButton = tk.Button(self.buttons, text = "Save", command = lambda : self.local_show_frame(controller,entry1,entry2,entry3,self.buttons)
            ,image=controller.save,compound="left",font=controller.buttonFont)

        nextButton.grid(row=0,column=0)
        f.grid()
        

    def local_show_frame(self,controller,rr,dd,ss,buttons):

        global sss,rrr,ddd#,mmm

        flag = 0

        controller.close_keyboard()

    	self.entry.grid_forget()
    	self.buttons.grid_forget()
    	self.title.grid(row=0,column=0,pady=10,padx=10,columnspan=3, sticky = "w")
    	self.separator.grid(row=1,column=0,columnspan=3,sticky="ew")
    	self.entry.grid(row=2, column=0, pady=ENTRYFRAMEPADY,padx=ENTRYFRAMEPADX)
    	self.buttons.grid(row=3, column=0,padx=BUTTONFRAMEPADX-40, columnspan=3,sticky="w")

        # w=mn.get()
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
        else:
            global returnToMenu
            # print returnToMenu
            infoBox("Done")
            # mmm = z
            if returnToMenu==True:
                controller.show_frame(Menu)
            else:
            	# buttons.config(padx=BUTTONFRAMEPADX)
            	backButton = tk.Button(self.buttons, text = "Back", command = lambda : self.backPressed(controller),image=controller.back,compound="left",font=controller.buttonFont)
            	nextButton = tk.Button(self.buttons, text = "Save", command = lambda : self.local_show_frame(controller,rr,dd,ss,self.buttons),image=controller.save,compound="left",font=controller.buttonFont)
            	backButton.grid(row=0,column=0)
            	nextButton.grid(row=0,column=1,padx=10)
            	controller.show_frame(DateTimeSetting)

    def backPressed(self,controller):

    	global sss,rrr,ddd#,mmm

    	controller.close_keyboard()
    	self.entry.grid_forget()
    	self.buttons.grid_forget()
    	self.title.grid(row=0,column=0,pady=10,padx=10,columnspan=3, sticky = "w")
    	self.separator.grid(row=1,column=0,columnspan=3,sticky="ew")
    	self.entry.grid(row=2, column=0, pady=ENTRYFRAMEPADY,padx=ENTRYFRAMEPADX)
    	self.buttons.grid(row=3, column=0,padx=BUTTONFRAMEPADX-40, columnspan=3,sticky="w")

    	self.w.set(rrr)
    	self.x.set(ddd)
    	self.y.set(sss)
    	# self.z.set(mmm)

    	controller.show_frame(Menu)

    def autocapitalize(self,var):

        var.set(var.get().upper())

    def adjust(self,event):

    	os.system("killall matchbox-keyboard") #controller.close_keyboard()
    	subprocess.Popen("matchbox-keyboard")
    	self.title.grid_forget()
        self.separator.grid_forget()
        self.entry.grid_forget()
        self.buttons.grid_forget()
        self.entry.grid(row=0, column=0, pady=0,padx=ENTRYFRAMEPADX)
        self.buttons.grid(row=1, column=0,padx=BUTTONFRAMEPADX-40, columnspan=3,sticky="w",pady=ENTRYFRAMEPADY-30)

    def readjust(self, event):

    	os.system("killall matchbox-keyboard") # controller.close_keyboard()
    	self.entry.grid_forget()
    	self.buttons.grid_forget()
    	self.title.grid(row=0,column=0,pady=10,padx=10,columnspan=3, sticky = "w")
    	self.separator.grid(row=1,column=0,columnspan=3,sticky="ew")
    	self.entry.grid(row=2, column=0, pady=ENTRYFRAMEPADY,padx=ENTRYFRAMEPADX)
    	self.buttons.grid(row=3, column=0,padx=BUTTONFRAMEPADX-40, columnspan=3,sticky="w")


class DateTimeSetting(tk.Frame):

    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(1,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(2,weight=1,minsize = MINSIZECOLUMN)
        self.grid_rowconfigure(2,weight=3,minsize = MINSIZEROW2)
        self.grid_rowconfigure(3,weight=1,minsize = MINSIZEROW3)
        self.x=True

        title = tk.Label(self, text="Date and Time Settings", font = controller.headerFont)
        title.grid(pady=10,padx=10,columnspan = 3, sticky="w")

        separator = ttk.Separator(self,orient=tk.HORIZONTAL)
        separator.grid(row=1,column=0,columnspan=3,sticky="ew")

        entry = tk.Frame(self)
        entry.grid(row=2, column=0, pady=ENTRYFRAMEPADY,padx=ENTRYFRAMEPADX)
        entry.grid_columnconfigure(2,minsize=220)
        # entry.grid_rowconfigure(4,minsize=50)

        buttons = tk.Frame(self)#, borderwidth=5, relief=tk.GROOVE)
        buttons.grid(row=3, column=0,pady = 0,padx=BUTTONFRAMEPADX-40, columnspan=3,sticky="w")

        label1 = tk.Label(entry, text = "DATE :",font = controller.defaultFont)
        label2 = tk.Label(entry, text = "TIME :",font=controller.defaultFont)
        label3 = tk.Label(entry, text = "START DATE :",font=controller.defaultFont)
        label4 = tk.Label(entry, text = "START TIME :",font=controller.defaultFont)

        self.currentDate = tk.StringVar(entry)
        # currentDate.set("1-1-2017")
        entry1 = tk.Entry(entry,font=controller.defaultFont,textvariable = self.currentDate)

        time1 = tk.Frame(entry)

        self.currentHour = tk.StringVar(time1)
        self.currentHour.set(HHLIST[0])
        HH1 = tk.Entry(time1, textvariable = self.currentHour,width=9,font=controller.defaultFont)
        HH1.grid(row=0,column=0,padx=3)
        
        self.currentMinute = tk.StringVar(time1)
        self.currentMinute.set(MMLIST[0])
        MM1 = tk.Entry(time1, textvariable = self.currentMinute,width=9,font=controller.defaultFont)
        MM1.grid(row=0,column = 1,padx=3)
                
        time2 = tk.Frame(entry)
        
        hh2 = tk.StringVar(time2)
        hh2.set(HHLIST[0])
        HH2 = ttk.Combobox(time2, textvariable = hh2, values=HHLIST,width=8,font=controller.defaultFont)
        HH2.grid(row=0,column=0,padx=3)
        
        mm2 = tk.StringVar(time2)
        mm2.set(MMLIST[0])
        MM2 = ttk.Combobox(time2, textvariable = mm2, values=MMLIST,width=8,font=controller.defaultFont)
        MM2.grid(row=0,column = 1,padx=3)
        
        entry3 = tk.Entry(entry,font=controller.defaultFont)

        label1.grid(row = 0, column =0,pady=14,sticky="e")
        label2.grid(row = 1, column =0,pady=14,sticky="e")
        label3.grid(row = 2, column =0,pady=14,sticky="e")
        label4.grid(row = 3, column =0,pady=14,sticky="e")

        entry1.grid(row = 0, column =1,padx = 20)
        time1.grid(row = 1, column =1,padx = 20)
        entry3.grid(row = 2, column =1,padx = 20)
        time2.grid(row = 3, column =1,padx = 20)

        nextButton = tk.Button(buttons, text = "Start", command = lambda : self.start_recording(controller,HH1,MM1,HH2,MM2,entry1,entry3),image=controller.start,compound="right",font=controller.buttonFont)
        backButton = tk.Button(buttons, text = "Back", command = lambda : self.local_show_frame(controller,TMSConfig),image=controller.back,compound="left",font=controller.buttonFont)
        # date1 = tk.Button(entry, image=controller.cal, command = lambda:controller.call_calendar(entry,date1.winfo_x(),date1.winfo_y(),entry1), width=30,height=30)
        date2 = tk.Button(entry, image=controller.cal, command = lambda:controller.call_calendar(entry,date2.winfo_x(),date2.winfo_y(),entry3), width=30,height=30)

        backButton.grid(column = 0,padx = 10)
        nextButton.grid(row = 0,column = 1)
        # date1.grid(row=0,column=2,sticky="w")
        date2.grid(row=2,column=2,sticky="w")
        self.upDate()


    def local_show_frame(self,controller,f):

		global calframe

		controller.close_keyboard()
		
		if calframe :
			calframe.place_forget()
		controller.show_frame(f)

    def upDate(self):

        if self.x :
            # global app
            a=str(datetime.datetime.now())
            self.currentDate.set(a[8:10]+"-"+a[5:7]+"-"+a[:4])
            self.currentHour.set(a[11:13])
            self.currentMinute.set(a[14:16])
            self.after(1000,self.upDate)
        else :
            pass

    def start_recording(self,controller,hh1,mm1,hh2,mm2,cdate,sdate):

        global c,d,f

        controller.close_keyboard()

        global calframe

        if calframe :
            calframe.place_forget()

        self.x = False

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
    			hh1.delete(0,"end")
                        mm1.delete(0,"end")
                        hh2.delete(0,"end")
                        mm2.delete(0,"end")
                        sdate.delete(0,"end")
                        cdate.delete(0,"end")
                        controller.show_frame(MainScreen)
                        recorder()



class MainScreen(tk.Frame):

    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_columnconfigure(0,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(1,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(2,weight=1,minsize = MINSIZECOLUMN)
        self.grid_rowconfigure(2,weight=1,minsize = MINSIZEROW2)
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

        global systemDate,systemTime,rrrr,ssss,dddd,currentTemp,currentMaxTemp,currentMinTemp

        systemDate = tk.Label(grid1, text = "DD/MM/YYYY",font = controller.defaultFont)
        systemTime = tk.Label(grid1, text = "HH:MM:SS",font = controller.defaultFont)
        rrrr = tk.Label(grid1, text = "RRRR",font = controller.defaultFont)
        dddd = tk.Label(grid1, text = "DIV",font = controller.defaultFont)
        ssss = tk.Label(grid1, text = "SSSS",font = controller.defaultFont)

        systemDate.grid(row=0, column = 0,pady=10)
        systemTime.grid(row=0,column = 2,pady=10)
        rrrr.grid(row=1, column = 0,pady=10)
        dddd.grid(row=1, column = 1,pady=10)
        ssss.grid(row=1, column = 2,pady=10)

        global statusLabel
        recording = tk.Frame(display)
        # photo = tk.PhotoImage(file = "/home/anupam/WorkSpace/CRTApp/img/rec.gif")
        statusLabel = tk.Label(recording,text="NOT RECORDING",font = controller.defaultFont,fg="blue",image=controller.nrec,compound="left")
        statusLabel.pack()
        recording.pack()

        grid2 = tk.Frame(display)
        grid2.pack(pady=20)

        temp = tk.Label(grid2, text = "TEMPERATURE :",font = controller.headerFont)
        mxtemp = tk.Label(grid2, text = "MAX TEMPERATURE :",font = controller.headerFont)
        mntemp = tk.Label(grid2, text = "MIN TEMPERATURE :",font = controller.headerFont)

        currentTemp = tk.Label(grid2, text = 0,font = controller.headerFont)
        currentMaxTemp = tk.Label(grid2, text = 0,font = controller.headerFont)
        currentMinTemp = tk.Label(grid2, text = 0,font = controller.headerFont)
        degree1 = tk.Label(grid2, text = "*C",font = controller.headerFont)
        degree2 = tk.Label(grid2, text = "*C",font = controller.headerFont)
        degree3 = tk.Label(grid2, text = "*C",font = controller.headerFont)

        temp.grid(row=0,column=0,sticky="e",pady=10)
        mxtemp.grid(row=1,column=0,sticky="e",pady=10)
        mntemp.grid(row=2,column=0,sticky="e",pady=10)
        currentTemp.grid(row=0,column=1)
        currentMaxTemp.grid(row=1,column=1)
        currentMinTemp.grid(row=2,column=1)
        degree1.grid(row=0,column=2)
        degree2.grid(row=1,column=2)
        degree3.grid(row=2,column=2)



        menuButton = tk.Button(buttons, text = "Menu", command = lambda :self.local_show_frame(controller),image=controller.menu,compound="left",font=controller.buttonFont)

        menuButton.grid()

    def local_show_frame(self,controller):

        global returnToMenu

        controller.close_keyboard()

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

        button1 = tk.Button(display, text = "TMS Configuration", command = lambda : self.local_show_frame(controller),width=30,font=controller.buttonFont)
        button2 = tk.Button(display, text = "Export", command = self.exportBox,width=30,font=controller.buttonFont)
        button3 = tk.Button(display, text = "View Output", command = lambda : controller.show_frame(Output),width=30,font=controller.buttonFont)
        button4 = tk.Button(display, text = "Settings", command = lambda : controller.show_frame(Settings),width=30,font=controller.buttonFont)
        button5 = tk.Button(display, text = "Change Password", command = lambda : controller.show_frame(PasswordChange),width=30,font=controller.buttonFont)

        button1.pack(pady=10)
        button2.pack(side = "bottom",pady=10)
        button3.pack(side = "bottom",pady=10)
        button4.pack(side = "bottom",pady=10)
        button5.pack(side = "bottom",pady=10)


        backButton = tk.Button(buttons, text = "Back", command = lambda : controller.show_frame(MainScreen),image=controller.back,compound="left",font=controller.buttonFont)

        backButton.grid()

    def local_show_frame(self, controller):

        controller.close_keyboard()

        controller.show_frame(TMSConfig)

    def exportBox(self):

    	d = MyDialog(self)
    	# print d.result


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
        entry.grid(row=2, column=0, pady=ENTRYFRAMEPADY,padx=ENTRYFRAMEPADX,sticky="n")

        buttons = tk.Frame(self)#, borderwidth=5, relief=tk.GROOVE)
        buttons.grid(row=3, column=0,padx=BUTTONFRAMEPADX-40, columnspan=3,sticky="w")

        label1 = tk.Label(entry, text = "Max Temperature :",font = controller.defaultFont)
        label2 = tk.Label(entry, text = "Min Temperature :",font=controller.defaultFont)      
        
        x = tk.StringVar()
        y = tk.StringVar()
        entry1 = tk.Entry(entry,textvariable=x,font=controller.defaultFont)
        entry2 = tk.Entry(entry,textvariable=y,font=controller.defaultFont)
        x.set(MAXIMUM)
        y.set(MINIMUM)

        entry1.bind("<Button-1>",controller.call_keyboard)
        entry2.bind("<Button-1>",controller.call_keyboard)

        self.bind("<Button-1>",controller.close_keyboard)
        # entry1.bind("<Leave>",controller.close_keyboard)
        # entry2.bind("<Leave>",controller.close_keyboard)

        label1.grid(row = 0, column =0,pady=10,sticky="e")
        label2.grid(row = 1, column =0,pady=10,sticky="e")

        entry1.grid(row = 0, column =1,padx = 80)
        entry2.grid(row = 1, column =1,padx = 80)

        nextButton = tk.Button(buttons, text = "Save", command = lambda : self.local_show_frame(controller,entry1,entry2),image=controller.save,compound="left",font=controller.buttonFont)
        backButton = tk.Button(buttons, text = "Back", command = lambda : self.backPressed(controller,x,y),image=controller.back,compound="left",font=controller.buttonFont)

        backButton.grid(row=0,column=0,padx=10)
        nextButton.grid(row=0,column=1)

    def local_show_frame(self,controller,Entry1,Entry2):

        global MAXIMUM,MINIMUM
        
        controller.close_keyboard()

        xx=Entry1.get()
        yy=Entry2.get()
        checkmx = re.search("(^[\-]{0,1}[0-9]+[\.][0-9]$)|(^[\-]{0,1}[0-9]+$)",xx)
        checkmn = re.search("(^[\-]{0,1}[0-9]+[\.][0-9]$)|(^[\-]{0,1}[0-9]+$)",yy)
        fl = 0
        if checkmx:
            if checkmn:
                fl = 1
            else:
                errorBox("Invalid Minimum Temperature")
        else:
            errorBox("Invalid Maximum Temperature")
        if fl == 1:
        	MAXIMUM = xx
        	MINIMUM = yy
        	infoBox("Done")
        	controller.show_frame(Menu)

    def backPressed(self,controller,Entry1,Entry2):

    	global MAXIMUM,MINIMUM
    	
    	controller.close_keyboard()

    	Entry1.set(MAXIMUM)
    	Entry2.set(MINIMUM)
    	x = Entry1.get()
    	controller.show_frame(Menu)



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
        buttons.grid(row=3, column=0,pady = 0,padx=BUTTONFRAMEPADX-40, columnspan=3,sticky="w")

        label1 = tk.Label(entry, text = "START DATE :",font = controller.defaultFont)
        label2 = tk.Label(entry, text = "START TIME :",font=controller.defaultFont)
        label3 = tk.Label(entry, text = "END DATE :",font=controller.defaultFont)
        label4 = tk.Label(entry, text = "END TIME :",font=controller.defaultFont)
        label5 = tk.Label(entry, text = "TIME INTERVAL :",font=controller.defaultFont)

        entry1 = tk.Entry(entry,font=controller.defaultFont)

        time1 = tk.Frame(entry)

        hh1 = tk.StringVar(time1)
        hh1.set(HHLIST[0])
        HH1 = ttk.Combobox(time1, textvariable = hh1, values=HHLIST,width=8,font=controller.defaultFont)
        HH1.grid(row=0,column=0,padx=3)
        
        mm1 = tk.StringVar(time1)
        mm1.set(MMLIST[0])
        MM1 = ttk.Combobox(time1, textvariable = mm1, values=MMLIST,width=8,font=controller.defaultFont)
        MM1.grid(row=0,column = 1,padx=3)
                
        entry3 = tk.Entry(entry,font=controller.defaultFont)

        time2 = tk.Frame(entry)
        
        hh2 = tk.StringVar(time2)
        hh2.set(HHLIST[0])
        HH2 = ttk.Combobox(time2, textvariable = hh2, values=HHLIST,width=8,font=controller.defaultFont)
        HH2.grid(row=0,column=0,padx=3)
        
        mm2 = tk.StringVar(time2)
        mm2.set(MMLIST[0])
        MM2 = ttk.Combobox(time2, textvariable = mm2, values=MMLIST,width=8,font=controller.defaultFont)
        MM2.grid(row=0,column = 1,padx=3)

        entry5 = tk.Entry(entry,font=controller.defaultFont)
        
        label5.grid(row = 0, column =0,pady=10,sticky="e")
        label1.grid(row = 1, column =0,pady=10,sticky="e")
        label2.grid(row = 2, column =0,pady=10,sticky="e")
        label3.grid(row = 3, column =0,pady=10,sticky="e")
        label4.grid(row = 4, column =0,pady=10,sticky="e")

        entry5.grid(row = 0, column =1,padx = 20)
        entry1.grid(row = 1, column =1,padx = 20)
        time1.grid(row = 2, column =1,padx = 20)
        entry3.grid(row = 3, column =1,padx = 20)
        time2.grid(row = 4, column =1,padx = 20)

        entry5.bind("<Button-1>",controller.call_keyboard)

        self.bind("<Button-1>",controller.close_keyboard)

        # entry5.bind("<Leave>",controller.close_keyboard)

        nextButton = tk.Button(buttons, text = "Output", command = lambda : self.validate(controller,HH1,MM1,HH2,MM2,entry1,entry3,entry5),image=controller.output,compound="left",font=controller.buttonFont)
        backButton = tk.Button(buttons, text = "Back", command = lambda : self.backPressed(controller,HH1,MM1,HH2,MM2,entry1,entry3,entry5),image=controller.back,compound="left",font=controller.buttonFont)
        date1 = tk.Button(entry, image=controller.cal, command = lambda:controller.call_calendar(entry,date1.winfo_x(),date1.winfo_y(),entry1), width=30,height=30)
        date2 = tk.Button(entry, image=controller.cal, command = lambda :controller.call_calendar(entry,date2.winfo_x(),date2.winfo_y(),entry3), width=30, height=30)

        backButton.grid(column = 0,padx = 10)
        nextButton.grid(row = 0,column = 1)
        date1.grid(row=1,column=2,sticky="w")
        date2.grid(row=3,column=2,sticky="w")

    def backPressed(self,controller,hh1,mm1,hh2,mm2,sdate,edate,intr):

        controller.close_keyboard()
        sdate.delete(0,"end")
    	edate.delete(0,"end")
    	intr.delete(0,"end")
    	hh1.delete(0,"end")
    	hh2.delete(0,"end")
    	mm1.delete(0,"end")
    	mm2.delete(0,"end")
        global calframe
        if calframe:
            calframe.place_forget()
        controller.show_frame(Menu)
    
    # def backPressed(self,controller,hh1,mm1,hh2,mm2,sdate,edate,intr):

    	

    def validate(self,controller,hh1,mm1,hh2,mm2,sdate,edate,intr):

        controller.close_keyboard()
        global calframe
        if calframe:
            calframe.place_forget()
        axx = hh1.get()
        b = mm1.get()
        c = hh2.get()
        d = mm2.get()
        e = sdate.get()
        f = edate.get()
        g = intr.get()
        h = re.search("^[0-9]+$",g)
        # print h.group(0)

        if not (axx and b and c and d and e and f and h):
            if e:
                if axx:
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
            start_date = e + " " + axx +":" + b + ":00"
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
                    calframe.place_forget()
                global rrr,sss,ddd, outfile,out
                output_on_screen(rrr,ddd,sss,g,e,f,axx,c,b,d)
                # num_lines = sum(1 for line in open('/home/pi/Desktop/output.dat'))
                # out.config(height=num_lines+100)
                # file = open('/home/pi/Desktop/output.dat','r')
                # file.close()
                controller.read_file_helper()
                controller.it = -1
                fi = controller.read_file(1)
                out.config(state="normal")
                out.delete('1.0',"end")
                for x in fi:
                    out.insert(tk.INSERT,x)
                out.config(state="disabled")
                hh1.delete(0,"end")
                mm1.delete(0,"end")
                hh2.delete(0,"end")
                mm2.delete(0,"end")
                sdate.delete(0,"end")
                edate.delete(0,"end")
                intr.delete(0,"end")
                              
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
        buttons.grid(row=3, column=0,padx=BUTTONFRAMEPADX-50,columnspan=3,sticky="w")

        outputFrame = tk.Frame(self)
        vscrollbar = AutoScrollbar(outputFrame)
        vscrollbar.grid(row=0, column=1, sticky="ns")
        hscrollbar = AutoScrollbar(outputFrame, orient="horizontal")
        hscrollbar.grid(row=1, column=0, sticky="ew")
        canvas = tk.Canvas(outputFrame, yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set,width=650)
        canvas.grid(row=0, column=0, sticky="nsew")
        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)
        outputFrame.grid_rowconfigure(0, weight=1)
        outputFrame.grid_columnconfigure(0, weight=1)
        frame = tk.Frame(canvas)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(1, weight=1)
        
        # num_lines = sum(1 for line in open('/home/pi/Desktop/output.dat'))
        # print num_lines
        global out
        out = tk.Text(frame, state="normal",width = 90,height = 25)
        out.pack()
        # text = tk.Label(frame,text=file.read(),justify = "left")
        # for i in range(1, rows):
        #   for j in range(1, 10):
        #       button = tk.Button(frame, text="%d, %d" % (i,j))
        #       button.grid(row=i, column=j, sticky='news')
        # frame.rowconfigure(1, weight=1)
        # frame.columnconfigure(1, weight=1)
        # text.pack()
        canvas.create_window(0, 0, anchor="nw", window=frame)
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        outputFrame.grid(row=2,column=0,pady=ENTRYFRAMEPADY,padx=35)


        backButton = tk.Button(buttons, text = "Menu", command = lambda : controller.show_frame(Menu),image=controller.menu,compound="left",font=controller.buttonFont)
        bButton = tk.Button(buttons,  command = lambda : self.backPage(controller,out,bButton,nButton),width = 3,state="disabled",image=controller.back,compound="left",font=controller.buttonFont)
        nButton = tk.Button(buttons, command = lambda : self.nextPage(controller,out,bButton,nButton), width = 3,image=controller.next,compound="right",font=controller.buttonFont)
        # self.checkNextBack(controller,bButton,nButton)

        bButton.grid(padx = 5,row=0,column=0)
        nButton.grid(padx=5,row=0,column=2)
        backButton.grid(row=0,column=1)




    def nextPage(self,controller,out,bButton,nButton):

        a = controller.read_file(1)
        if a!=-1:
            bButton.config(state = "normal")
            nButton.config(state = "normal")
            ret = controller.checkNextBack()
            if(ret == 1):
                bButton.config(state = "disabled")
            if(ret == 3):
                nButton.config(state = "disabled")
            out.config(state="normal")
            out.delete('1.0',"end")
            for x in a:
                out.insert(tk.INSERT,x)
            out.config(state="disabled")
        else:
            nButton.config(state="disabled")

    def backPage(self,controller,out,bButton,nButton):

        a = controller.read_file(0)
        if a != -1:
            bButton.config(state = "normal")
            nButton.config(state = "normal")
            ret = controller.checkNextBack()
            if(ret == 1):
                bButton.config(state = "disabled")
            if(ret == 3):
                nButton.config(state = "disabled")
            out.config(state="normal")
            out.delete('1.0',"end")
            for x in a:
                out.insert(tk.INSERT,x)
            out.config(state="disabled")
        else:
            bButton.config(state="disabled")



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
        buttons.grid(row=3, column=0,padx=BUTTONFRAMEPADX-40,pady=20, columnspan=3,sticky="w")

        #label1 = tk.Label(entry, text = "Username :",font = controller.defaultFont)
        label2 = tk.Label(entry, text = "Password :",font=controller.defaultFont)       
        
        #entry1 = tk.Entry(entry)
        self.passw = tk.StringVar()
        entry2 = tk.Entry(entry,show="*",textvariable=self.passw,font=controller.defaultFont)

        #label1.grid(row = 0, column =0,pady=10,sticky="e")
        label2.grid(row = 1, column =0,pady=10,sticky="e")

        #entry1.grid(row = 0, column =1,padx = 80)
        entry2.grid(row = 1, column =1,padx = 80)

        #entry1.bind("<FocusIn>",controller.call_keyboard)
        entry2.bind("<Button-1>",controller.call_keyboard)

        self.bind("<Button-1>",controller.close_keyboard)

        #entry1.bind("<FocusOut>",controller.close_keyboard)
        # entry2.bind("<Leave>",controller.close_keyboard)

        # backButton = ttk.Button(buttons, text = "Back", command = lambda : self.backPressed(controller))
        nextButton = tk.Button(buttons, text = "Next", command = lambda : self.local_show_frame(controller,buttons),image=controller.next,compound="right",font=controller.buttonFont)

        # backButton.grid(row=0 ,column=0,padx=10)
        nextButton.grid(row=0 ,column=1)
        
    def local_show_frame(self,controller,buttons):

        global sss,rrr,ddd

        controller.close_keyboard()

        flag = 0

        #u=user.get()
        p=self.passw.get()

        #user.delete(0,"end")
        self.passw.set("")
        
        #if """u == "anupam" and""" p == "singh":
        global PASSWORD
        UPASSWORD = None
        try:
            p9=open(HOMEDIR+"/data/securp.dat","r")
            for line in p9:
                UPASSWORD=line
        except:
            pass

        hashObject = hashlib.sha512(p)
        p = hashObject.hexdigest()
        if p == UPASSWORD or p == PASSWORD:
            flag = 1

        
        if flag == 1:
        	global returnToMenu
        	if returnToMenu:
        		controller.show_frame(Menu)
        	else:
        		backButton = tk.Button(buttons, text = "Back", command = lambda : self.backPressed(controller),image=controller.back,compound="left",font=controller.buttonFont)
        		nextButton = tk.Button(buttons, text = "Next", command = lambda : self.local_show_frame(controller,buttons),image=controller.next,compound="right",font=controller.buttonFont)
        		backButton.grid(row=0 ,column=0,padx=10)
        		nextButton.grid(row=0 ,column=1)
	    		controller.show_frame(TMSConfig)
        else:
            errorBox("Invalid Password")

    def backPressed(self,controller):

    	controller.close_keyboard()
    	self.passw.set("")
    	controller.show_frame(MainScreen)


class PasswordChange(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(1,weight=1,minsize = MINSIZECOLUMN)
        self.grid_columnconfigure(2,weight=1,minsize = MINSIZECOLUMN)
        # self.grid_rowconfigure(0,weight=1,minsize = 80)
        self.grid_rowconfigure(2,weight=3,minsize = MINSIZEROW2)
        self.grid_rowconfigure(3,weight=1,minsize = MINSIZEROW3)
        
        title = tk.Label(self, text="Change Password", font=controller.headerFont)
        title.grid(row=0,column=0,pady=10,padx=10,columnspan=3, sticky = "w")

        separator = ttk.Separator(self,orient=tk.HORIZONTAL)
        separator.grid(row=1,column=0,columnspan=3,sticky="ew")

        entry = tk.Frame(self)
        entry.grid(row=2, column=0, pady=ENTRYFRAMEPADY,padx=ENTRYFRAMEPADX,sticky="n")

        self.buttons = tk.Frame(self)#, borderwidth=5, relief=tk.GROOVE)
        self.buttons.grid(row=3, column=0,padx=BUTTONFRAMEPADX-40,pady=20, columnspan=3,sticky="w")

        label1 = tk.Label(entry, text = "New Password :",font = controller.defaultFont)
        label2 = tk.Label(entry, text = "Confirm Password :",font=controller.defaultFont)       
        
        self.passw1 = tk.StringVar()
        self.passw2 = tk.StringVar()
        entry1 = tk.Entry(entry,show="*",textvariable=self.passw1,font=controller.defaultFont)
        entry2 = tk.Entry(entry,show="*",textvariable=self.passw2,font=controller.defaultFont)

        label1.grid(row = 0, column =0,pady=10,sticky="e")
        label2.grid(row = 1, column =0,pady=10,sticky="e")

        entry1.grid(row = 0, column =1,padx = 80)
        entry2.grid(row = 1, column =1,padx = 80)

        entry1.bind("<Button-1>",controller.call_keyboard)
        entry2.bind("<Button-1>",controller.call_keyboard)

        self.bind("<Button-1>",controller.close_keyboard)

        # entry1.bind("<Leave>",controller.close_keyboard)
        # entry2.bind("<Leave>",controller.close_keyboard)

        backButton = tk.Button(self.buttons, text = "Back", command = lambda : self.backPressed(controller),image=controller.back,compound="left",font=controller.buttonFont)
        nextButton = tk.Button(self.buttons, text = "Save", command = lambda : self.local_show_frame(controller),image=controller.save,compound="left",font=controller.buttonFont)

        backButton.grid(row=0,column=0,padx=10)
        nextButton.grid(row=0,column=1)
        
    #def local_show_frame(self,controller,"""user,"""passw):
    def local_show_frame(self,controller):

        global sss,rrr,ddd

        controller.close_keyboard()

        flag = 0

        p1=self.passw1.get()
        p2=self.passw2.get()

        self.passw1.set("")
        self.passw2.set("")
        
        #if """u == "anupam" and""" p == "singh":
        if p1 and p2:
        	if p1 == p2:
        		flag = 1
        		global PASSWORD
        		#PASSWORD = p1
        		outfile1 = open(HOMEDIR+"/data/securp.dat","w")
                hashObject = hashlib.sha512(p1)
                p1 = hashObject.hexdigest()
                outfile1.write(p1)
                infoBox("Done")
        	if flag==1:
        		controller.show_frame(Menu)
        	else:
        		errorBox("Password doesn't Match")
        else:
        	errorBox("Invalid Input")

    def backPressed(self,controller):

    	controller.close_keyboard()
    	
    	self.passw1.set("")
        self.passw2.set("")
    	controller.show_frame(Menu)


global app
app = CRTApp()

app.mainloop()


