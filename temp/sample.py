import Tkinter as tk
import xml.etree.ElementTree as ET
import tkMessageBox
import os
# import qualysapi as qa

DEFAULT_FONT = ("Verdana" , 12) 
USERNAME = "x"
PASSWORD = "x"
directory = '\\home\\anupam'
file = 'config.ini'

def xml_Fetch():

	# a = qa.connect(directory+file)
	# call = '/api/2.0/fo/report/'
	# param = {'action' : 'list', 'state' : 'Finished', 'echo_request' : '1'}
	# xml_output = a.request(call, param)
	# tree = ET.fromstring(xml_output)
	# # print qa.xml_output
	# # print type(qa.xml_output)
	# # root = tree.getroot()
	# # print root.tag
	# return tree
	tree = ET.parse('reports.xml')
	root = tree.getroot()
	# print root.tag
	return root

def configuration(user, passw):
	if not os.path.exists(directory):
	    os.makedirs(directory)
	f = open(directory+file,'w')
	s = """[DEFAULT]
max_retries = 3
hostname = qualysapi.qualys.eu

[info]
max_retries = 3
hostname = qualysapi.qualys.eu
username = """+user+"""
password = """+passw
	f.write(s)

def doNothing():
	print "GO fuck yourself!"

def credentialCheck(page, controller):

	
	global USERNAME
	global PASSWORD
	# print USERNAME,PASSWORD
	if USERNAME == 'x' and PASSWORD == 'x':
		controller.show_frame(loginPage)
	else:
		controller.show_frame(page)

def logout():

	global USERNAME
	global PASSWORD
	USERNAME = 'x'
	PASSWORD = 'x'
	os.remove(directory+file)
	# print USERNAME,PASSWORD
	tkMessageBox.showinfo('Information','Successful')

class QualysScanReport(tk.Tk):


	def __init__(self,*args,**kwargs):

		tk.Tk.__init__(self, *args, **kwargs)
		tk.Tk.wm_title(self,"Qualys Report")
		self.wm_geometry("800x600")
		self.wm_resizable( width=False, height=False)
		
		
		container = tk.Frame(self)
		# container.resizable(width=False, height=False)
		container.pack(side="top", fill="both", expand=True)

		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}

		for F in (startPage, loginPage, reports, downloadSpecific):

			frame = F(container, self)

			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		###########################################################################################################

		menuBar = tk.Menu(self)
		self.config(menu=menuBar)
		subMenu = tk.Menu(menuBar)
		menuBar.add_cascade(label = "File", menu=subMenu)
		subMenu.add_command(label = "Start", command=lambda:self.show_frame(startPage))
		subMenu.add_command(label = "Login", command=lambda:self.show_frame(loginPage))
		subMenu.add_command(label = "Logout", command=logout)
		subMenu.add_separator()
		subMenu.add_command(label = "Exit", command=exit)
		editMenu = tk.Menu(menuBar)
		menuBar.add_cascade(label = "Edit", menu=editMenu)
		editMenu.add_command(label = "Reports", command=lambda:credentialCheck(reports,self))
		editMenu.add_command(label = "Download", command=lambda:credentialCheck(downloadSpecific,self))
		editMenu.add_separator()
		editMenu.add_command(label = "Exit", command=exit)

		###########################################################################################################

		self.show_frame(startPage)

	def show_frame(self, cont):

		frame = self.frames[cont]
		frame.tkraise()

class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient="vertical")
        vscrollbar.pack(fill="y", side="right", expand=False)
        ####################################################################
        hscrollbar = tk.Scrollbar(self, orient="horizontal")
        hscrollbar.pack(fill="x", side="bottom", expand=False)
        ####################################################################
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set,xscrollcomman=hscrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        vscrollbar.config(command=self.canvas.yview)
        hscrollbar.config(command=self.canvas.xview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(self.canvas)
        interior_id = self.canvas.create_window(0, 0, window=interior,
                                           anchor="nw")

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                self.canvas.config(width=interior.winfo_reqwidth())
            if interior.winfo_reqheight() != self.canvas.winfo_height():
                # update the canvas's width to fit the inner frame
                self.canvas.config(height=interior.winfo_reqheight())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_reqwidth())
            if interior.winfo_reqheight() != self.canvas.winfo_height():
                # update the inner frame's width to fill the canvas
                self.canvas.itemconfigure(interior_id, height=self.canvas.winfo_reqheight())
        self.canvas.bind('<Configure>', _configure_canvas)
        self.interior.bind('<Enter>', self._bound_to_mousewheel)
        self.interior.bind('<Leave>', self._unbound_to_mousewheel)

    def _bound_to_mousewheel(self, event):
    	self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)
    
    def _unbound_to_mousewheel(self, event):
    	self.canvas.unbind_all('<MouseWheel>')

    def _on_mousewheel(self, event):
    	self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


class startPage(tk.Frame):

	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)
		
		title = tk.Label(self, text="Qualys Report", font=DEFAULT_FONT)
		
		license = tk.Frame(self)
		scroll = tk.Scrollbar(license)
		text = tk.Text(license, height = 400, width = 400)
		scroll.pack(side="right",fill="y")
		text.pack(side="left")
		scroll.config(command=text.yview)
		text.config(yscrollcommand = scroll.set)
		lic = """The GNU General Public Licence (GPL) is probably one of the most commonly used licenses for open-source projects. The GPL grants and guarantees a wide range of rights to developers who work on open-source projects. Basically, it allows users to legally copy, distribute and modify software. This means you can:
		The GNU General Public Licence (GPL) is probably one of the most commonly used licenses for open-source projects. The GPL grants and guarantees a wide range of rights to developers who work on open-source projects. Basically, it allows users to legally copy, distribute and modify software. This means you can:
		The GNU General Public Licence (GPL) is probably one of the most commonly used licenses for open-source projects. The GPL grants and guarantees a wide range of rights to developers who work on open-source projects. Basically, it allows users to legally copy, distribute and modify software. This means you can:
		The GNU General Public Licence (GPL) is probably one of the most commonly used licenses for open-source projects. The GPL grants and guarantees a wide range of rights to developers who work on open-source projects. Basically, it allows users to legally copy, distribute and modify software. This means you can:
		The GNU General Public Licence (GPL) is probably one of the most commonly used licenses for open-source projects. The GPL grants and guarantees a wide range of rights to developers who work on open-source projects. Basically, it allows users to legally copy, distribute and modify software. This means you can:
		The GNU General Public Licence (GPL) is probably one of the most commonly used licenses for open-source projects. The GPL grants and guarantees a wide range of rights to developers who work on open-source projects. Basically, it allows users to legally copy, distribute and modify software. This means you can:
		The GNU General Public Licence (GPL) is probably one of the most commonly used licenses for open-source projects. The GPL grants and guarantees a wide range of rights to developers who work on open-source projects. Basically, it allows users to legally copy, distribute and modify software. This means you can:
		The GNU General Public Licence (GPL) is probably one of the most commonly used licenses for open-source projects. The GPL grants and guarantees a wide range of rights to developers who work on open-source projects. Basically, it allows users to legally copy, distribute and modify software. This means you can:
		The GNU General Public Licence (GPL) is probably one of the most commonly used licenses for open-source projects. The GPL grants and guarantees a wide range of rights to developers who work on open-source projects. Basically, it allows users to legally copy, distribute and modify software. This means you can:
		The GNU General Public Licence (GPL) is probably one of the most commonly used licenses for open-source projects. The GPL grants and guarantees a wide range of rights to developers who work on open-source projects. Basically, it allows users to legally copy, distribute and modify software. This means you can:
		The GNU General Public Licence (GPL) is probably one of the most commonly used licenses for open-source projects. The GPL grants and guarantees a wide range of rights to developers who work on open-source projects. Basically, it allows users to legally copy, distribute and modify software. This means you can:
		The GNU General Public Licence (GPL) is probably one of the most commonly used licenses for open-source projects. The GPL grants and guarantees a wide range of rights to developers who work on open-source projects. Basically, it allows users to legally copy, distribute and modify software. This means you can:
		The GNU General Public Licence (GPL) is probably one of the most commonly used licenses for open-source projects. The GPL grants and guarantees a wide range of rights to developers who work on open-source projects. Basically, it allows users to legally copy, distribute and modify software. This means you can:
		The GNU General Public Licence (GPL) is probably one of the most commonly used licenses for open-source projects. The GPL grants and guarantees a wide range of rights to developers who work on open-source projects. Basically, it allows users to legally copy, distribute and modify software. This means you can:"""
		text.insert("end", lic)
		text.config(state="disabled")

		agree = tk.Button(self, text="Agree", command=lambda:controller.show_frame(loginPage))
		
		disagree = tk.Button(self, text="Disagree", command=exit)

		title.place(bordermode="outside", x=20, y=10)
		license.place(bordermode="outside", height=450, width=750, x=20,y=50)
		agree.place(bordermode="outside", x=335,y=520,width=60)
		disagree.place(bordermode="outside", x=405,y=520,width=60)

		# label2.pack(pady=10,padx=10)
		# quit.pack()
		# label1.pack(pady=10,padx=10)
		# login.pack()
		# license.pack()
		# label1.grid(row=0, column=0)
		# license.grid(row=1, column=0)
		# label2.grid(row=3,column=10)
		# login.grid(row=4,column=10)
		# quit.grid(row=4,column=11)

class loginPage(tk.Frame):

	global USERNAME
	global PASSWORD
	controllerg = 0

	def __init__(self,parent,controller):

		tk.Frame.__init__(self, parent)
		
		title = tk.Label(self, text="Login", font=DEFAULT_FONT)
		
		loginButton = tk.Button(self, text="Login", command=self._login_clicked)
		backButton = tk.Button(self, text="Back", command=lambda:controller.show_frame(startPage))
		
		userLabel = tk.Label(self, text="Username: ")
		passwLabel = tk.Label(self, text="Password: ")

		self.controllerg = controller

		self.userEntry = tk.Entry(self)
		self.passwEntry = tk.Entry(self)
		self.passwEntry.config(show="*")
		self.passwEntry.bind('<Return>', self.__login_clicked)

		userLabel.place(bordermode="outside", x=240, y=200)
		passwLabel.place(bordermode="outside", x=242, y=240)
		self.userEntry.place(bordermode="outside", x=350, y=200, width=150)
		self.passwEntry.place(bordermode="outside", x=350, y=240, width=150)
		title.place(bordermode="outside", x=20, y=10)
		loginButton.place(bordermode="outside", x=335,y=520,width=60)
		backButton.place(bordermode="outside", x=405,y=520,width=60)

	def _login_clicked(self):

		global USERNAME 
		global PASSWORD
		if(self.userEntry.get() and self.passwEntry.get()):
			USERNAME =  self.userEntry.get()
			PASSWORD =  self.passwEntry.get()
			configuration(USERNAME, PASSWORD)
			
			self.controllerg.show_frame(reports)
		else:
			err = tk.Label(self, text="Please Enter Valid Username and Password")
			err.config(fg='red')
			err.place(bordermode="outside", x=270, y=300)

	def __login_clicked(self,event):
		self._login_clicked()

class reports(tk.Frame):

	cb = []
	k = 0

	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)
		
		title = tk.Label(self, text="Reports", font=DEFAULT_FONT)

		reportFrame = VerticalScrolledFrame(self)

		xmlResponse = xml_Fetch()
		
		i=0
		j=0

		maxx = []

		for child in xmlResponse[1][1][0]:
			maxx.append(len(child.tag))
			for att in xmlResponse[1][1].iter(child.tag):
				maxx[i] = max(len(att.text), maxx[i])
			i=i+1

		i=0

		ttext = tk.Label(reportFrame.interior,height=1,width=1,relief="raised")
		ttext.grid(row = 0, column = 0, sticky="nsew")

		for child in xmlResponse[1][1][0]:
			i=0
			ttext = tk.Label(reportFrame.interior,height=1,width=maxx[j]+3,relief="raised",text=child.tag)
			ttext.grid(row = i, column = j+1, sticky="nsew")
			for att in xmlResponse[1][1].iter(child.tag):
				
				i = i+1
				if(j==0):
					self.cb.append(tk.Checkbutton(reportFrame.interior, text=""))
					self.cb[self.k].config(relief="sunken")
					self.cb[self.k].grid(row = i, column = j, sticky="nsew")
					self.k = self.k + 1
				ttext=tk.Text(reportFrame.interior, height=1,width=maxx[j]+3,relief="sunken")
				if ord(att.text[0]) != 10:
					ttext.insert("end",att.text)
				else:
					ttext.insert("end",att[0].text)
				ttext.config(state="disabled")
				ttext.grid(row = i, column = j+1, sticky="nsew")
			# if i<22:
			# 	k=22
			# 	while i<k:
			# 		ttext=tk.Text(reportFrame.interior, height=1,width=maxx[j]+3, relief="sunken")
			# 		ttext.grid(row = i, column = j+1, sticky="nsew")
			# 		ttext.config(state="disabled")
			# 		i=i+1
			j=j+1

		fetchButton = tk.Button(self, text="Fetch", command=self._fetch_clicked)
		backButton = tk.Button(self, text="Back", command=lambda:controller.show_frame(loginPage))

		reportFrame.place(bordermode="outside", x=20, y=50,height=450,width=750)
		title.place(bordermode="outside", x=20, y=10)
		fetchButton.place(bordermode="outside", x=335,y=520,width=60)
		backButton.place(bordermode="outside", x=405,y=520,width=60)

	def _fetch_clicked(self):
		tkMessageBox.showinfo('Information','bhak bhosadike')

class downloadSpecific(tk.Frame):

	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)

		title = tk.Label(self, text="Download", font=DEFAULT_FONT)





app = QualysScanReport()

app.mainloop()
print USERNAME,PASSWORD