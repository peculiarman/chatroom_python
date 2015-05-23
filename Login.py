from Tkinter import *
import sys
from socket import *
from utility import DataOutputStream,DataInputStream,get_lan_ip
from tkMessageBox import *



CRLF = "\r\n"


class logBox(Frame):
    def __init__(self,parent=None,chatclient=None):
        Frame.__init__(self,parent)
        self.varList = {}
        self.soketDict = {}
        self.makeLoginForm()
        self.attachingChatClient = chatclient
    def makeLoginForm(self):       
        lIP = Label(self,text = 'Chat Server IP:')     
        entIP = Entry(self,relief = RIDGE)                        
        varIP = StringVar()
        entIP.config(textvariable = varIP)
        varIP.set('localhost')
        self.varList["serverhost"] = varIP
        lNick = Label(self,text = 'Log in as:')
        entNick = Entry(self,relief = RIDGE)
        varNick = StringVar()
        entNick.config(textvariable = varNick)
        self.entNick = entNick
        self.varList["nickname"]= varNick
        lPW = Label(self,text = 'Password:')
        entPW = Entry(self,show = '*',relief = RIDGE)
        varPW = StringVar()
        entPW.config(textvariable = varPW)
        self.entPW = entPW
        self.varList["password"] = varPW
        loginBt = Button(self,text = "Log in",command = self.onLoginFunc)
        exitBt = Button(self,text = "Exit",command = sys.exit)
        self.pack(expand = YES, fill = BOTH)
        lIP.pack(side = LEFT)
        entIP.pack(side = LEFT,expand = YES,fill=X)
        lNick.pack(side = LEFT)
        entNick.pack(side = LEFT,expand = YES,fill=X)
        lPW.pack(side = LEFT)
        entPW.pack(side = LEFT,expand = YES,fill=X)
        loginBt.pack(side = LEFT,expand = YES,fill=Y)
        exitBt.pack(side = LEFT,expand = YES,fill=Y)    
    def onLoginFunc(self):
        from tkMessageBox import showinfo,showerror
        s_varList = []
        validated = False
        for i in self.varList.keys():
            s_varList.append(self.varList[i].get())
        if ('' in s_varList):
            showinfo('Incomplete login info','Please complete login info')
            self.lift()
            self.entNick.focus()
        else:
            try:
                sockobj = socket(AF_INET,SOCK_STREAM)
                sockobj.connect((self.varList["serverhost"].get(),9082))
                self.dos = DataOutputStream(sockobj)
                self.soketDict["outputstream"] = self.dos
                self.dis = DataInputStream(sockobj)
                self.soketDict["inputstream"] = self.dis
                print 'Sending connection request message....'
                self.sendMsg("10!@~`"+"HELLO!@~`"+get_lan_ip()+"!@~`O"+CRLF)
                reply = self.dis.readUTF()
                if (self.parseReply(reply) != 20):
                    raise IOError
		else:
                    print "reply from server "+self.varList["serverhost"].get()+": "+str(self.parseReply(reply))+" OK"
		    reply = self.dis.readUTF()   
                if (self.parseReply(reply) != 30):
		    raise IOError
		else: 
		    print "reply from server "+self.varList["serverhost"].get()+": "+str(self.parseReply(reply))+" AUTH REQUIRE"
		    self.sendMsg("40!@~`"+self.varList["nickname"].get()+"!@~`"+self.varList["password"].get()+"!@~`O"+CRLF)
                reply = self.dis.readUTF();
                if (self.parseReply(reply) == 50):
		    print "reply from server "+self.varList["serverhost"].get()+": "+str(self.parseReply(reply))+" AUTH SUCCESS"
		    self.sendMsg("90!@~`"+"SYSTEM!@~`ENTER!@~`"+self.varList["nickname"].get() +"!@~`O"+CRLF)
		    validated = True
		elif(self.parseReply(reply) == 60):
		    print "reply from server "+self.varList["serverhost"].get()+": "+str(self.parseReply(reply))+" AUTH FAILED"
		    showwarning("Authorization Fail...","Authorization fail,Please input the correct Usr/Passwd")
		else:
		    raise IOError
		
            except:
                print sys.exc_info()[0]
                print sys.exc_info()[1]
                showerror('connecting failed','connecting server failed... (Are you sure server is up?)')

            
            if (validated):
                self.master.destroy()
                self.attachingChatClient.clientInfo = self.varList
                self.attachingChatClient.socketInfo = self.soketDict
                self.attachingChatClient.logIn = True
                return True
            else:
                self.entNick.delete(0, END)
                self.entPW.delete(0, END)
                return False

    def onExit(self):
        sys.exit()
    def parseReply(self,reply):
        replyArray = reply.split("!@~`")
        return int(replyArray[0])
    def sendMsg(self,msg):
        self.dos.write(msg)

def main():
    root = Tk()
    root.title('login')
    logBox(root)
    root.mainloop()


if __name__ == '__main__':
    main()
    
