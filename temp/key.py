from Tkinter import *

class OSKeyboard(Toplevel):

    def __init__(self, parent, title = None, pos_x = 50, pos_y = 50):
        Toplevel.__init__(self, parent)
        self.transient(parent)

        #--Dialog Popup Position--#
        self.pos_x = pos_x
        self.pos_y = pos_y

        #--Button List--#
        self.btn_list = [
        '1',    '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace',
        'Tab',  'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\',
        'Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', 'Enter',
        'Shift','z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'Shift',
        '<<',   'Space', '>>', 'Clear'
         ]

        self.btn_listM = [
        '!',    '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', 'Backspace',
        'Tab',  'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|',
        'Caps', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"', 'Enter',
        'Shift','Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?', 'Shift',
        '<<',   'Space', '>>', 'Clear'
         ]

        self.btn_listS = [
        '1',    '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace',
        'Tab',  'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '(', ')', '|',
        'Caps', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '_', 'Enter',
        'Shift','Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Shift',
        '<<',   'Space', '>>', 'Clear'
         ]

        self.keystate = 1; # Small size

        #--Dialog title--#
        if title:
            self.title(title)

        self.parent = parent
        self.result = None

        self.display = StringVar()

        mbody = Frame(self)
        self.initial_focus = self.body(mbody, 1)
        mbody.pack()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        #--Start Dialog position--#
        self.geometry("+%d+%d" % (parent.winfo_rootx()+self.pos_x, parent.winfo_rooty()+self.pos_y))

        #--Dialog can't Resize--#
        self.resizable(width=FALSE, height=FALSE)

        self.initial_focus.focus_set()
        self.wait_window(self)

    def body(self, master, mtyp):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        for c in range(14):
            master.columnconfigure(c, weight=0)#pad=1)
        for r in range(5):
            master.columnconfigure(r, weight=0)#pad=1)

        self.label = Label(master, font=('Helvetica', 32), relief='sunken', borderwidth=3, bg='gray40', anchor=SW, fg='green', textvariable=self.display)##, anchor = SE, fg='blue')
        self.label.grid(row = 0, column = 0, columnspan = 14, padx  = 1, pady = 1, sticky='SWEN')

        fn = ('Helvetica', 10)
        fnbold = ('Helvetica', 10, 'bold')
        rel = 'raised'#'groove'

        if mtyp == 1:
            key = self.btn_listS
        elif mtyp == 2:
            key = self.btn_listM

        r = 1
        c = 0
        for b in key:
            cmd = lambda x=b:self.call(x)
            c_span = 1
            r_span = 1
            w = 4

            if (r==1):
                if(c==12): # Back Space
                    c_span = 2
                    cmd = lambda:self.backspace()
                    Button(master, text = b, font = fnbold, width = w, command = cmd, relief = rel).grid(row = r, column = c, rowspan = r_span, columnspan = c_span,  padx = 1, pady=1, sticky='SWEN')
                else:
                    Button(master, text = b, font = fn, width = w, command = cmd, relief = rel).grid(row = r, column = c, rowspan = r_span, columnspan = c_span,  padx = 1, pady=1, sticky='SWEN')
            elif (r==2):
                if(c==0): # Tab (4 space)
                    cmd = lambda:self.call('    ')
                    Button(master, text = b, font = fnbold, width = w, command = cmd, relief = rel).grid(row = r, column = c, rowspan = r_span, columnspan = c_span,  padx = 1, pady=1, sticky='SWEN')
                else:
                    Button(master, text = b, font = fn, width = w, command = cmd, relief = rel).grid(row = r, column = c, rowspan = r_span, columnspan = c_span,  padx = 1, pady=1, sticky='SWEN')
            elif (r==3):
                if(c==0): # Capslock
                    cmd = lambda:self.CapsLock()
                    Button(master, text = b, font = fnbold, width = w, command = cmd, relief = rel).grid(row = r, column = c, rowspan = r_span, columnspan = c_span,  padx = 1, pady=1, sticky='SWEN')
                elif (c==12): # Enter
                    c_span = 2
                    r_span = 2
                    cmd = lambda:self.Enter()
                    Button(master, text = b, font = fnbold, width = w, command = cmd, relief = rel, bg = '#EF7321').grid(row = r, column = c, rowspan = r_span, columnspan = c_span,  padx = 1, pady=1, sticky='SWEN')
                else:
                    Button(master, text = b, font = fn, width = w, command = cmd, relief = rel).grid(row = r, column = c, rowspan = r_span, columnspan = c_span,  padx = 1, pady=1, sticky='SWEN')
            elif (r==4):
                if(c==0): # Shift Left
                    cmd = lambda:self.Shift()
                    Button(master, text = b, font = fnbold, width = w, command = cmd, relief = rel).grid(row = r, column = c, rowspan = r_span, columnspan = c_span,  padx = 1, pady=1, sticky='SWEN')
                elif(c==11): # Shift Right
                    cmd = lambda:self.Shift()
                    Button(master, text = b, font = fnbold, width = w, command = cmd, relief = rel).grid(row = r, column = c, rowspan = r_span, columnspan = c_span,  padx = 1, pady=1, sticky='SWEN')
                else:
                    Button(master, text = b, font = fn, width = w, command = cmd, relief = rel).grid(row = r, column = c, rowspan = r_span, columnspan = c_span,  padx = 1, pady=1, sticky='SWEN')
            elif (r==5):
                if(c==0): # <<
                    Button(master, text = b, font = fnbold, width = w, command = cmd, relief = rel, state=DISABLED).grid(row = r, column = c, rowspan = r_span, columnspan = c_span,  padx = 1, pady=1, sticky='SWEN')
                elif(c==1): # Space
                    c_span = 10
                    cmd = lambda:self.call(' ')
                    Button(master, text = b, font = fnbold, width = w, command = cmd, relief = rel).grid(row = r, column = 1, rowspan = r_span, columnspan = c_span,  padx = 1, pady=1, sticky='SWEN')
                elif(c==2): # >>
                    Button(master, text = b, font = fnbold, width = w, command = cmd, relief = rel, state=DISABLED).grid(row = r, column = 11, rowspan = r_span, columnspan = c_span,  padx = 1, pady=1, sticky='SWEN')
                elif(c==3): # Clear
                    c_span = 2
                    cmd = lambda:self.clear()
                    Button(master, text = b, font = fnbold, width = w, command = cmd, relief = rel).grid(row = r, column = 12, rowspan = r_span, columnspan = c_span,  padx = 1, pady=1, sticky='SWEN')

            c += 1
            if (c == 12):
                if (r==4):
                    r += 1
                    c = 0
            elif (c == 13):
                if (r==1) or (r==3):
                    r += 1
                    c = 0
            elif (c == 14):
                r += 1
                c = 0

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        pass

    #
    # standard button semantics

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):
        return 1 # override

    def apply(self):
        pass # override

     #--Key return function--#
    def call(self, num):
        content = self.display.get() + num
        self.display.set(content)
        if self.keystate == 2:  # Shift press
            self.body(self, 1)
            self.keystate = 1

    def Enter(self):
        content = self.display.get()
        if content == '':
            pass
        else:
            self.result = content
            self.ok()

    def Backspace(self):
        pass

    def Shift(self):
        self.body(self, 2);
        self.keystate = 2

    def Tab(self):
        pass

    def CapsLock(self):
        if self.keystate == 1:
            self.body(self, 2)
            self.keystate = 3
        elif self.keystate == 3 or self.keystate == 2:
            self.body(self, 1)
            self.keystate = 1

    def Space(self):
        pass

    #--Sign--#
    def sign(self):
        content = -(float(self.display.get()))
        self.display.set(content)

    #--Calculated using the eval function--#
    def calculate(self):
        try:
            content = self.display.get()
            result = eval(content)
            self.result = result
            self.display.set(str(result))
            self.ok()
        except:
            self.display.set('Error')
            self.clear()

    #--Empty the contents of the column--#
    def clear(self):
        self.display.set('')

    #--Before you delete a charater--#
    def backspace(self):
        self.display.set(str(self.display.get()[:-1]))

def open_dialog():
   pass

# def main():
root = Tk()
d = OSKeyboard(root, 'On Screen Keyboard', 600, 100)
print d.result
root.mainloop()