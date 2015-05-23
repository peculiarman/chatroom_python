from bk_form import *
from socket import *
from Client import *
import thread

class ChatServer:
    def __init__(self,lock):
        self.lock = lock
        self.clientDict = {}
        self.makewidget()
    def makewidget(self):
        root = Tk()
        root.title('Chat Server...')
        bkInfo = Form(root)
        self.bkInfo = bkInfo
        thread.start_new(self.start,())
        root.mainloop()
    def start(self):
        try:
            ss = socket(AF_INET,SOCK_STREAM)
            ss.bind(('',9082))
            ss.listen(1000)
            while True:
                connection,address = ss.accept()
                clientInstance = Client(attachingChatServer=self,connSocket=connection,lock=self.lock)
                clientInstance.start()
        except IOError,(errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)



if __name__ == '__main__':
    lock = thread.allocate_lock()
    ChatServer(lock)
