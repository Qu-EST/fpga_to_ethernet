import socketserver
import datetime

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def setup(self):
        self.output = open(str(datetime.datetime.now()), 'a+')
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(8)
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.output.write("{}{}".format(self.data,'\n'))

if __name__ == "__main__":
    HOST, PORT = "10.0.0.1", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
