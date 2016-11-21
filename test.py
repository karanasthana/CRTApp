import Tkinter as tk
import tkFont
import ttk
import calendar
import pcalender

HHLIST = ["00","01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
            "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]
MMLIST = ["00","01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
            "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
            "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
            "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
            "41", "42", "43", "44", "45", "46", "47", "48", "49", "50",
            "51", "52", "53", "54", "55", "56", "57", "58", "59"]

def qf():
    print "done"

def get_calendar(locale, fwday):
    # instantiate proper calendar class
    if locale is None:
        return calendar.TextCalendar(fwday)
    else:
        return calendar.LocaleTextCalendar(fwday, locale)





class CRTApp(tk.Tk):

    DD = ""
    MM = ""
    YYYY = ""

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self,"CRTApp")
        self.wm_geometry("800x480")
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

        for F in (TNSConfig, DateTimeSetting, MainScreen, Menu, Settings, Export, Login ):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(TNSConfig)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def update(self, calframe,e,d,m,y):

        calframe.grid_forget()

        # YYYY = ttkcal._date.year
        # MM = ttkcal._date.month
        # DD = ttkcal._selection[0]

        YYYY = y
        MM = m
        DD = d

        e.delete(0, "end")
        e.insert(0,str(DD) + '-' + str(MM) + '-' + str(YYYY))

    def call_calendar(self,f,x,y,e):

        calframe= ttk.Frame(self,borderwidth=3,relief=tk.GROOVE)
        ttkcal = pcalender.Calendar(calframe,self.update,e,firstweekday=pcalender.calendar.SUNDAY)
        ttkcal.grid(row=0,column=0)
        # close = ttk.Button(calframe,text='x',width=1,command=lambda:qf())#self.update(calframe,e,ttkcal))
        # close.grid(row=0,column=1,sticky="nw")
        # calframe.grid(row=0,column=1,rowspan=4)
        calframe.grid(pady=y+150,padx=x-10)
        


class TNSConfig(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0,weight=1,minsize = 250)
        self.grid_columnconfigure(1,weight=1,minsize = 250)
        self.grid_columnconfigure(2,weight=1,minsize = 250)
        # self.grid_rowconfigure(0,weight=1,minsize = 80)
        self.grid_rowconfigure(2,weight=3,minsize = 160)
        self.grid_rowconfigure(3,weight=1,minsize = 50)
        
        title = tk.Label(self, text="TNS Configuration", font=controller.headerFont)
        title.grid(row=0,column=0,pady=10,padx=10,columnspan=3, sticky = "w")

        separator = ttk.Separator(self,orient=tk.HORIZONTAL)
        separator.grid(row=1,column=0,columnspan=3,sticky="ew")

        entry = tk.Frame(self)
        entry.grid(row=2, column=0, pady=75,padx=180)

        buttons = tk.Frame(self)#, borderwidth=5, relief=tk.GROOVE)
        buttons.grid(row=3, column=0,padx=0, columnspan=3)

        label1 = tk.Label(entry, text = "Railway Name :",font = controller.defaultFont)
        label2 = tk.Label(entry, text = "Division Name :",font=controller.defaultFont)
        label3 = tk.Label(entry, text = "Station Name :",font=controller.defaultFont)
        label4 = tk.Label(entry, text = "Model Number :", font=controller.defaultFont)        
        
        entry1 = tk.Entry(entry)
        entry2 = tk.Entry(entry)
        entry3 = tk.Entry(entry)
        entry4 = tk.Entry(entry)

        label1.grid(row = 0, column =0,pady=10,sticky="e")
        label2.grid(row = 1, column =0,pady=10,sticky="e")
        label3.grid(row = 2, column =0,pady=10,sticky="e")
        label4.grid(row = 3, column =0,pady=10,sticky="e")

        entry1.grid(row = 0, column =1,padx = 80)
        entry2.grid(row = 1, column =1,padx = 80)
        entry3.grid(row = 2, column =1,padx = 80)
        entry4.grid(row = 3, column =1,padx = 80)

        nextButton = ttk.Button(buttons, text = "Next", command = lambda : controller.show_frame(DateTimeSetting))

        nextButton.grid()
        # print self.grid_size()
        # pcalender.__init__("Anupam")


class DateTimeSetting(tk.Frame):

    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0,weight=1,minsize = 250)
        self.grid_columnconfigure(1,weight=1,minsize = 250)
        self.grid_columnconfigure(2,weight=1,minsize = 250)
        self.grid_rowconfigure(2,weight=3,minsize = 160)
        self.grid_rowconfigure(3,weight=1,minsize = 50)

        title = tk.Label(self, text="Date and Time Settings", font = controller.headerFont)
        title.grid(pady=10,padx=10,columnspan = 3, sticky="w")

        separator = ttk.Separator(self,orient=tk.HORIZONTAL)
        separator.grid(row=1,column=0,columnspan=3,sticky="ew")

        entry = tk.Frame(self)
        entry.grid(row=2, column=0, pady=75,padx=180)

        buttons = tk.Frame(self)#, borderwidth=5, relief=tk.GROOVE)
        buttons.grid(row=3, column=0,pady = 0,padx=0, columnspan=3)

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

        label1.grid(row = 0, column =0,pady=10,sticky="e")
        label2.grid(row = 1, column =0,pady=10,sticky="e")
        label3.grid(row = 2, column =0,pady=10,sticky="e")
        label4.grid(row = 3, column =0,pady=10,sticky="e")

        entry1.grid(row = 0, column =1,padx = 80)
        time1.grid(row = 1, column =1,padx = 80)
        entry3.grid(row = 2, column =1,padx = 80)
        time2.grid(row = 3, column =1,padx = 80)

        nextButton = ttk.Button(buttons, text = "Start", command = lambda : controller.show_frame(MainScreen))
        backButton = ttk.Button(buttons, text = "Back", command = lambda : controller.show_frame(TNSConfig))
        date1 = ttk.Button(entry, text = ".", command = lambda:controller.call_calendar(entry,date1.winfo_x(),date1.winfo_y(),entry1), width=3)
        date2 = ttk.Button(entry, text = ".", command = lambda :controller.call_calendar(entry,date2.winfo_x(),date2.winfo_y(),entry3), width=3)

        backButton.grid(column = 0,padx = 10)
        nextButton.grid(row = 0,column = 1)
        date1.grid(row=0,column=2,sticky="w")
        date2.grid(row=2,column=2,sticky="w")



class MainScreen(tk.Frame):

    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_columnconfigure(0,weight=1,minsize = 266)
        self.grid_columnconfigure(1,weight=1,minsize = 266)
        self.grid_columnconfigure(2,weight=1,minsize = 266)
        self.grid_rowconfigure(2,weight=3,minsize = 160)
        self.grid_rowconfigure(3,weight=1,minsize = 50)

        title = tk.Label(self, text="Statistics", font=controller.headerFont)
        title.grid(pady=10,padx=10,columnspan = 3, sticky="w")

        separator = ttk.Separator(self,orient=tk.HORIZONTAL)
        separator.grid(row=1,column=0,columnspan=3,sticky="ew")

        display = tk.Frame(self)
        display.grid(row=2, column=0)

        grid1 = tk.Frame(display)
        grid1.pack()

        grid1.grid_columnconfigure(0,weight=1,minsize = 250)
        grid1.grid_columnconfigure(1,weight=1,minsize = 250)
        grid1.grid_columnconfigure(2,weight=1,minsize = 250)

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
        t1 = tk.Label(grid2, text = "XXX",font = controller.defaultFont)
        t2 = tk.Label(grid2, text = "XXX",font = controller.defaultFont)
        t3 = tk.Label(grid2, text = "XXX",font = controller.defaultFont)
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


        buttons = tk.Frame(self)#, borderwidth=5, relief=tk.GROOVE)
        buttons.grid(row=3, column=0,pady = 0,padx=0, columnspan=3)

        menuButton = ttk.Button(buttons, text = "Menu", command = lambda : controller.show_frame(Menu))

        menuButton.grid()


class Menu(tk.Frame):

    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_columnconfigure(0,weight=1,minsize = 266)
        self.grid_columnconfigure(1,weight=1,minsize = 266)
        self.grid_columnconfigure(2,weight=1,minsize = 266)

        title = tk.Label(self, text="Menu", font=controller.headerFont)
        title.grid(pady=10,padx=10,columnspan = 3, sticky="w")

        separator = ttk.Separator(self,orient=tk.HORIZONTAL)
        separator.grid(row=1,column=0,columnspan=3,sticky="ew")

        display = tk.Frame(self)#,borderwidth=3,relief = tk.GROOVE)
        display.grid(row=2, column=0,pady = 70,padx=250)

        button1 = tk.Button(display, text = "TNS Configuration", command = lambda : controller.show_frame(TNSConfig),width=30)
        button2 = tk.Button(display, text = "Settings", command = qf,width=30)
        button3 = tk.Button(display, text = "View Output", command = qf,width=30)
        button4 = tk.Button(display, text = "Export", command = qf,width=30)

        button1.pack(pady=10)
        button2.pack(side = "bottom",pady=10)
        button3.pack(side = "bottom",pady=10)
        button4.pack(side = "bottom",pady=10)

        buttons = tk.Frame(self)#, borderwidth=5, relief=tk.GROOVE)
        buttons.grid(row=3, column=0,pady = 0,padx=0, columnspan=3)

        backButton = ttk.Button(buttons, text = "Back", command = lambda : controller.show_frame(MainScreen))

        backButton.grid()


class Settings(tk.Frame):

    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_columnconfigure(0,weight=1,minsize = 266)
        self.grid_columnconfigure(1,weight=1,minsize = 266)
        self.grid_columnconfigure(2,weight=1,minsize = 266)

        title = tk.Label(self, text="Settings", font=controller.headerFont)
        title.grid(pady=10,padx=10,columnspan = 3, sticky="w")

        separator = ttk.Separator(self,orient=tk.HORIZONTAL)
        separator.grid(row=1,column=0,columnspan=3,sticky="ew")


class Export(tk.Frame):

    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.grid_columnconfigure(0,weight=1,minsize = 266)
        self.grid_columnconfigure(1,weight=1,minsize = 266)
        self.grid_columnconfigure(2,weight=1,minsize = 266)

        title = tk.Label(self, text="Export", font=controller.headerFont)
        title.grid(pady=10,padx=10,columnspan = 3, sticky="w")

        separator = ttk.Separator(self,orient=tk.HORIZONTAL)
        separator.grid(row=1,column=0,columnspan=3,sticky="ew")


class Login(tk.Frame):

    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.grid_columnconfigure(0,weight=1,minsize = 266)
        self.grid_columnconfigure(1,weight=1,minsize = 266)
        self.grid_columnconfigure(2,weight=1,minsize = 266)

        title = tk.Label(self, text="Login", font=controller.headerFont)
        title.grid(pady=10,padx=10,columnspan = 3, sticky="w")

        separator = ttk.Separator(self,orient=tk.HORIZONTAL)
        separator.grid(row=1,column=0,columnspan=3,sticky="ew")




app = CRTApp()
app.mainloop()


