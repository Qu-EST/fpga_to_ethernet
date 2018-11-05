'''host computer program to receive data continously till the connection is broken
if the connection is broken, new connection is accepted and data is stored to a new file'''

import socket
from time import strftime
import struct
from Queue import Queue
import threading


class data_getter(threading.Thread):
    '''Thread to receive the data from the PS
    inputs: socket, data_queue, object of the data processor'''
    def __init__(self, conn, dataq, processor):
        self.soc = conn
        self.dataq = dataq
        self.switch = True
        self.processor = processor
        threading.Thread.__init__(self)

        
    def run(self):
        '''read a four byte length first
        Then read the socket till the length is reached
        put all the read data to the queue'''
        
        while self.switch:
            size, self.switch = self.readndata(4, conn)
            size = struct.unpack('>I', size)
            data, self.switch = self.readndata(size, conn)
            self.dataq.put(data)
        self.soc.close()
        while(self.dataq.empty()==False):
            pass
        self.processor.switch = False
        

    def readndata(self, n, soc):
        ''' reads n bytes from the socket
        returns the data read 
        and status of the connection -- True if open and viceversa'''
        
        data = b''
        conn_status = True
        while len(data)<n:
            temp = soc.recv(n-len(data))
            if(temp== b''):
                conn_status = False
            data += temp
        return data, conn_status

        
class data_processor(threading.Thread):
    '''thread to process the data
    This is the consumer thread for the dataq
    reads the data from the queue and save to the file
    input: dataq'''
    def __init__(self, dataq):
        self.dataq = dataq
        threading.Thread.__init__(self)
        self.outfile = open('{}.csv'.format(strftime('%H:%M:%S_%m-%d')), 'a+')
        self.switch = True


    def run(self):
        while self.switch:
            try:
                data = self.dataq.get(block=False, timeout=1)
            except:
                pass            
            else:
                while len(data)>0 :
                    refid = data[:4]
                    refid = struct.unpack('<I', refid)
                    data = data[4:]
                    utime = data[:4]
                    utime = struct.unpack('<I', utime)
                    data = data[4:]
                    self.outfile.write('{},{}\n'.format(refid, utime))
        self.outfile.close()
                    
                

if __name__ == "__main__":
    HOST, PORT = "10.0.0.1", 9999
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((HOST, PORT))
    #listen for one connection 
    server_sock.listen(1)
    #accept a connection and receive till the connection dies
    while True:
        print("waiting for a connection")
        conn, client_addr = server_sock.accept()
        print("Connected to the {}".format(client_addr))
        dataq = Queue()
        dp = data_processor(dataq)
        dp.start()
        dg = data_getter(conn, dataq, dp)
        dg.start()

