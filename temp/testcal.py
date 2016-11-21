import wckCalendar

root = Tkinter.Tk()

def echo():
    print calendar.getselection()

calendar = wckCalendar.Calendar(root, command=echo)
calendar.pack()

mainloop()