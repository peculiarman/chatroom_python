from Tkinter import * 


class ScrolledList(Frame):
    def __init__(self, options=[], parent=None):
        Frame.__init__(self, parent)
        self.pack(side=RIGHT, expand=YES, fill=BOTH)
        self.makeWidgets(options)
    def handleList(self, event):
        index = self.listbox.curselection()
        label = self.listbox.get(index)
        self.runCommand(label)
    def makeWidgets(self, options):
        sbar = Scrollbar(self)
        list = Listbox(self, relief=SUNKEN)
        sbar.config(command=list.yview)
        list.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        list.pack(side=LEFT, expand=YES, fill=BOTH)
        pos = 0
        for label in options:
            list.insert(pos, label)
            pos = pos + 1
        list.bind('<Double-1>', self.handleList)
        self.listbox = list
    def runCommand(self, selection):
        print 'You selected:', selection


class ScrolledText(Frame):
    def __init__(self, parent=None, text='', file=None):
        Frame.__init__(self, parent)
        self.pack(side = LEFT, expand=YES, fill=BOTH) 
        self.makewidgets()
        self.settext(text, file)
    def makewidgets(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN)
        sbar.config(command=text.yview)
        text.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        text.pack(side=LEFT, expand=YES, fill=BOTH)
        self.text = text
    def settext(self, text='', file=None):
        if file: 
            text = open(file, 'r').read()
        self.text.delete('1.0', END)
        self.text.insert('1.0', text)
        self.text.mark_set(INSERT, '1.0')
    def gettext(self):
        return self.text.get('1.0', END+'-1c')

class Form(Frame):
    def __init__(self,parent=None):
        Frame.__init__(self,parent)
        self.pack(expand=YES,fill=BOTH)
        self.makewidgets()
    def makewidgets(self):
        sClientList = ScrolledList(parent=self)
        sInfoText = ScrolledText(parent=self)
        self.sInfoText = sInfoText
        self.sClientList = sClientList
        

if __name__== '__main__':
    root=Tk()
    root.title("experiment")
    frm = Form(root)
    root.mainloop()
        
        
