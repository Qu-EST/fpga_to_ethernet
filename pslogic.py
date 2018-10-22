import socket
from Queue import Queue
import threading

HOST, PORT = "10.0.0.1", 9999
CONTROL_ADDR = ""
DATA_ADDR = ""
TDC_REG_ADDR = ""


class TCP_sender(threading.Thread):
    '''sender thread'''
    def __init__(self, sock, dataq):
        self.sock = sock
        self.dataq = dataq
        self.switch = threading.Event()
        self.switch.set()

    def run(self):
        while self.switch.is_set():
            data = dataq.get(block=False, timeout=1)
            sock.sendall(data)
        self.sock.close()


#open the TCP Connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
data_queue = Queue()
sender = TCP_sender(sock, data_queue)
sender.start()





