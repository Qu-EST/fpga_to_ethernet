import struct
import socket
from Queue import Queue
import threading

HOST, PORT = "10.0.0.1", 9999
CONTROL_ADDR = ""
DATA_ADDR = ""
TDC_REG_ADDR = ""
TEST = True

class TCP_sender(threading.Thread):
    '''sender thread'''
    def __init__(self, sock, dataq):
        self.sock = sock
        self.dataq = dataq
        self.switch = threading.Event()
        self.switch.set()
        threading.Thread.__init__(self)

    def run(self):
        while self.switch.is_set():
            try:
                data = self.dataq.get(block=False, timeout=1)
            except:
                pass
            
            else:
                self.sock.sendall(data)
        self.sock.close()


class test_generator(threading.Thread):
    def __init__(self, dataq, sender):
        self.dataq = dataq
        self.switch = threading.Event()
        self.switch.set()
        self.sender = sender
        threading.Thread.__init__(self)

    def run(self):
        while self.switch.is_set():
            for i in range(1, 1048500):
                msg = struct.pack('>I', i)
                msg = msg+msg
                self.dataq.put(msg)
            while(self.dataq.empty()==False):
                pass
            
            self.sender.switch.clear()
            self.switch.clear()
            
        

if __name__ == "__main__":
#open the TCP Connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    data_queue = Queue()
    sender = TCP_sender(sock, data_queue)
    sender.start()

    

    #test data generator for the ethernet queeu
    if(TEST):
        gen = test_generator(data_queue, sender)
        gen.start()
        

    
        
