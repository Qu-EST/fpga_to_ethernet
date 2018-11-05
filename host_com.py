'''host computer program to receive data continously till the connection is broken
if the connection is broken, new connection is accepted and data is stored to a new file'''

import socket
from time import strftime
import struct
from Queue import Queue

def get_data(conn):
    data = None
    outfile = open('{}.csv'.format(strftime('%H:%M:%S_%m-%d')), 'a+')
    outq = Queue()
    while True:
        data1 = conn.recv(4)
        data2 = conn.recv(4)
        if((data1==b'') or (data2 == b'')):
            break
        else:
            ref_id = struct.unpack('>I', data1)[0]
            u_time = struct.unpack('>I', data2)[0]
            out = "{},{}\n".format(ref_id, u_time)
            outq.put(out)
            #print(out)
            #outfile.write(out)
            
    conn.close()
    outfile.close()
    while not outq.empty():
        print(outq.get())
        

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
        get_data(conn)
