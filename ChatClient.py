from Login import *
from bk_form import *
from Receive import *
import thread 


class ChatClient(Frame):
    def __init__(self,parent=None):
        Frame.__init__(self, parent)
        self.pack(side=RIGHT, expand=YES, fill=BOTH)
        self.clientInfo = {}
        self.socketInfo = {}
        self.makewidget()
        self.logIn = False
        thread.start_new(self.start,())
    def makewidget(self):
        bkInfo = Form(self)
        self.clientList = bkInfo.sClientList
        self.text= bkInfo.sInfoText
        frm = Frame(self)
        frm.pack(side=BOTTOM,expand=YES,fill=X)
        sendEnt = Entry(frm)
        sendBt = Button(frm,text='Send',command=self.onSend)
        msgSendVar = StringVar()
        sendEnt.config(textvariable = msgSendVar)
        msgSendVar.set('message to send')
        self.msgSend = msgSendVar
        sendBt.pack(side=RIGHT)
        sendEnt.pack(side=LEFT,expand=YES,fill=X)
        self.rootWin = root
    def start(self):
        logFlag = self.logIn
        while not logFlag:
            logFlag = self.logIn
        rThread = Receive(attachingChatClient = self, connSocket = self.socketInfo)
        rThread.start()
    def onSend(self):
        content = self.msgSend.get()
        postPeople = self.clientList.listbox.get(ACTIVE)
        if (not postPeople) or (not cmp("",postPeople)) or (not cmp("all online",postPeople)):
            self.text.text.insert('end',"[" + self.clientInfo["nickname"].get() + "]" + " broadcasting:" + content + "\n")
        else:
            self.text.text.insert('end',"[" + self.clientInfo["nickname"].get() + "] " + content + "\n")
        posMsg = "70!@~`"+ self.clientInfo["nickname"].get() + "!@~`" + postPeople + "!@~`" + content+"!@~`O"+CRLF
        self.socketInfo["outputstream"].write(posMsg)
        self.msgSend.set('')
        

def onQuit(chatClientInstance):
    chatClientInstance.socketInfo["outputstream"].write("90!@~`"+"SYSTEM!@~`EXIT!@~`"+chatClientInstance.clientInfo["nickname"].get() +"!@~`O"+CRLF)
    chatClientInstance.master.quit()

def waitLogin(cc,root):
    global waitLoginV
    global title_string
    global ccInstance
    exit = cc.logIn
    while not exit:
        exit = cc.logIn
    title_string = cc.clientInfo["nickname"].get()
    ccInstance = cc
    waitLoginV = True
    print "Exit WaitLogin thread......"
    
    
def decorate(rootWin,string,variable,afterhandle=None): 
    if variable:
        rootWin.title(string)
        rootWin.protocol('WM_DELETE_WINDOW',lambda cc = ccInstance : onQuit(cc))
    else:
        afterhandle = rootWin.after(10,decorate,root,title_string,waitLoginV,afterhandle)


def quitCallback():
    if askyesno('Verify','Do you want to quit program?'):
        sys.exit()
    else:
        pass



if __name__ == '__main__':
    global waitLoginV
    global title_string
    global ccInstance
    title_string = "ChatClient"
    waitLoginV = False
    root = Tk()
    logInWin = Toplevel()
    root.title(title_string)
    cc = ChatClient(root)
    logInWin.lift(root)
    logInWin.title('Log in')
    logBox(logInWin,cc)
    logInWin.focus_set() 
    logInWin.grab_set()
    logInWin.protocol('WM_DELETE_WINDOW',quitCallback)
    thread.start_new(waitLogin,(cc,root))
    decorate(root,title_string,waitLoginV)
    root.mainloop()
