import struct
import socket
import sys

HOST, PORT = "10.0.0.1", 9999
data1 = 2004
data2 = 7
data = struct.pack('>I', data1) +struct.pack('>I', data2)
# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    for i in range (0,10):
        sock.sendall(data)
        
