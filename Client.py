
import threading,time
from utility import *

CRLF = "\r\n"

class Client(threading.Thread):
    def __init__(self,attachingChatServer=None,connSocket=None,lock=None):
        self.attachServer = attachingChatServer
        self.lock = lock
        try :
            self.connSocket = connSocket
            self.dis = DataInputStream(self.connSocket)
            self.dos = DataOutputStream(self.connSocket)	    
            self.isStart = True
        except IOError:
            import sys
            print sys.exc_info()[0],sys.exc_info()[1]
        threading.Thread.__init__(self)
    def run(self):
        try :
            while(self.isStart):
                msg = self.dis.readUTF()
                tmpMsg = msg.split("!@~`")
                if self.parseReply(msg) == 10:
                    self.dos.write("20!@~`"+get_lan_ip()+"!@~`HELLO!@~`"+tmpMsg[2]+"!@~`O"+CRLF)
                    self.dos.write("30!@~`"+"AUTH!@~`"+tmpMsg[2]+"!@~`O"+CRLF)
                elif(self.parseReply(msg) == 40):
                    user,password = tmpMsg[1],tmpMsg[2]
                    logFile = open('loginfo.txt','r')
                    found = False
                    while logFile:
                        line = logFile.readline()
                        if not line:
                            break
                        authen = line.split("##")
                        usr_a = authen[0]
                        pw_str = authen[1]
                        if (cmp(user,usr_a) == 0) and (cmp(password,pw_str) == 0):
                            found = True
                            break
                    if found and (not self.attachServer.clientDict.has_key(user)):
                        self.dos.write("50!@~`"+"AUTH-SUCCESS!@~`"+user+"!@~`O"+CRLF)
                    else:
                        self.dos.write("60!@~`"+"AUTH-FAILED!@~`"+user+"!@~`O"+CRLF)
                elif(self.parseReply(msg) == 70):
                    nickname = tmpMsg[1]
                    content = tmpMsg[3]
                    if (not tmpMsg[2]) or (tmpMsg[2] == None) or (tmpMsg[2] == "all online"):
                        self.lock.acquire()
                        for key in self.attachServer.clientDict.keys():
                            clientInstance = self.attachServer.clientDict[key]
                            if(self.dos != clientInstance.dos):
                                self.send(clientInstance.dos,msg)
                        self.lock.release()
                        self.attachServer.bkInfo.sInfoText.text.insert('end',"["+ nickname +"]" + " broadcasting: " + content + "\n")
                    else:
                        self.lock.acquire()
                        clientInstance = self.attachServer.clientDict[tmpMsg[2]]
                        self.send(clientInstance.dos,msg)
                        self.attachServer.bkInfo.sInfoText.text.insert('end',"["+ nickname +"] to " + "[" + tmpMsg[2] + "]" + ":" + content + "\n")
                        self.lock.release()
                elif(self.parseReply(msg) == 90):
                    sysMsg = msg.split("!@~`")
                    monitorMsg = "100!@~`"
                    if not cmp(sysMsg[1],"SYSTEM"):
                        if not cmp(sysMsg[2],"ENTER"):
                            onlinePeoples = ""
                            self.nickname = sysMsg[3]
                            self.lock.acquire()
                            self.attachServer.clientDict[user]= self
                            self.attachServer.bkInfo.sClientList.listbox.insert('end',user)
                            self.lock.release()
                            onlinePeoples = "100!@~`" + "all online"
                            self.lock.acquire()
                            for i in self.attachServer.bkInfo.sClientList.listbox.get(0,'end'):
                                onlinePeoples += "!#~`" + i
                            for key in self.attachServer.clientDict:
                                clientInstance = self.attachServer.clientDict[key]
                                self.send(clientInstance.dos,onlinePeoples)
                            self.lock.release()
                            monitorMsg += "[" + self.nickname +"]" + " entering "
                        elif not cmp(sysMsg[2],"EXIT"): 
                            onlinePeoples = ""
                            self.nickname = sysMsg[3]
                            self.lock.acquire()
                            pos = 0
                            for label in self.attachServer.bkInfo.sClientList.listbox.get(0,'end'):
                                if not cmp(sysMsg[3],label):
                                    break
                                else:
                                    pos += 1
                            self.attachServer.bkInfo.sClientList.listbox.delete(pos)
                            onlinePeoples = "100!@~`" + "all online"
                            for label in self.attachServer.bkInfo.sClientList.listbox.get(0,'end'):
                                onlinePeoples += "!#~`" + label
                            for key in self.attachServer.clientDict:
                                clientInstance = self.attachServer.clientDict[key]
                                self.send(clientInstance.dos,onlinePeoples)
                            self.lock.release()
                            monitorMsg += "[" + self.nickname +"]" + " exiting "
                    monitorMsg += " chatroom "
                    actMsg = monitorMsg.split("!@~`");
                    time.sleep(1)
                    self.lock.acquire()
                    self.attachServer.bkInfo.sInfoText.text.insert('end',actMsg[1] + "\n")
                    for key in self.attachServer.clientDict:
                        clientInstance = self.attachServer.clientDict[key]
                        self.send(clientInstance.dos,monitorMsg)
                    self.lock.release()



        except:
            import sys
            self.isStart= False
            clientName = None
            for key in self.attachServer.clientDict.keys():
                if self.attachServer.clientDict[key] == self:
                    clientName = key
                    del self.attachServer.clientDict[key]
                    break

            print sys.exc_info()[0],sys.exc_info()[1]
            if clientName:
                print "client [%s] thread exit......"%clientName
            else:
                print "client [Unknown] thread exit......"
                            
    def parseReply(self,reply):
        replyArray = reply.split("!@~`")
        return int(replyArray[0])

    def send(self,dos,msg):
        try:
            dos.write(msg)
        except:
            import sys
            print sys.exc_info()[0],sys.exc_info()[1]
    
