import threading
from utility import *

CRLF = "\r\n"

class Receive(threading.Thread):
    def __init__(self,attachingChatClient=None,connSocket=None,lock=None):
        self.attachChatClient = attachingChatClient
        self.lock = lock
        try :
            self.connSocket = connSocket
            self.dis = self.connSocket['inputstream']
            self.isStart = True
        except :
            import sys
            print sys.exc_info()[0],sys.exc_info()[1]
        threading.Thread.__init__(self)
    def run(self):
        while(self.isStart):
            try :
                msg = self.dis.readUTF()
                tmpMsg = msg.split("!@~`")
                if self.parseReply(msg) == 70:
                    nickname = tmpMsg[1]
                    content = tmpMsg[3]
                    if (not tmpMsg[2]) or (not cmp("null",tmpMsg[2])) or (not cmp("all online",tmpMsg[2])):
                        self.attachChatClient.text.text.insert('end',"[" + nickname + "]" + " broadcasting:" + content + "\n")
                    else:
                        self.attachChatClient.text.text.insert('end',"[" + nickname + "]" + content + "\n")
                elif self.parseReply(msg) == 100:
                    actMsg = tmpMsg[1]
                    onlinePeoples = actMsg.split("!#~`")
                    if (len(onlinePeoples) > 1):
                        self.attachChatClient.clientList.listbox.delete(0,'end')
                        for i in range(len(onlinePeoples)):
                            self.attachChatClient.clientList.listbox.insert('end',onlinePeoples[i])
                    else:
                        self.attachChatClient.text.text.insert('end', actMsg + "\n")
            except:
                self.isStart= False
                clientName = self.attachChatClient.clientInfo["nickname"].get()
                print "client [%s] thread exception......"%clientName

    def parseReply(self,reply):
        replyArray = reply.split("!@~`")
        return int(replyArray[0])
