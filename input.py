def dummyDone(x):
    print "done"
    global app
    x.destroy()
    dbox = tk.Toplevel(app)
    dbox.wm_geometry("360x100")
    dbox.wm_title("Done")
    defaultFont = tkFont.Font(family = "Helvetica", size = 10, weight = "bold")

    label = tk.Label(dbox,text="Exporting Done",font = defaultFont)
    label.grid(padx=10,pady=10,sticky="w")

    button = tk.Button(dbox,text = "OK", command=dbox.destroy)
    button.grid(row=1,column=1,pady=10,sticky="e",padx=30)

    dbox.mainloop()




def dummyProgress(x):

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
    pbox.mainloop()

    # dummyDone()

TILIST = ["Seconds","Minutes","Hours","Days"]

def inputBox():

    global app
    ibox = tk.Toplevel(app)
    ibox.wm_geometry("360x100")
    ibox.wm_title("Time Interval")
    defaultFont = tkFont.Font(family = "Helvetica", size = 10, weight = "bold")

    label = tk.Label(ibox,text="Enter Time Interval",font = defaultFont)
    label.grid(padx=10,pady=10,columnspan=2,sticky="w")

    entry = tk.Entry(ibox,width=40)
    entry.grid(row=1,column=0,padx=10)

    ti = tk.StringVar(ibox)
    ti.set(TILIST[1])
    TI = ttk.Combobox(ibox, textvariable = ti, values=TILIST,width=10)
    TI.grid(row=1,column=1)

    button = tk.Button(ibox,text = "Export", command=lambda:dummyProgress(ibox))
    button.grid(row=2,column=0,columnspan=2,pady=10)

    ibox.mainloop()