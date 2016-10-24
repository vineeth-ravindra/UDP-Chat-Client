'''
    Author : Vineeth Ravindra
    Description : This is a simple server program developed
                  for set1 NetSec Lab assignment. This server
                  handles multiple UDP clients and helps them
                  communicate among them selves
    Usage : python <server_name> -sp <port_num>
            sp - port on which server is running
'''
#!/usr/bin/env python
import signal
import socket
import sys
'''
    The server object accepts connection from multiple clients.
    The server maintains a history of all clients connected to
    the server since the server was run. When the server receives
    a INCOMING message the message is forwarded to all clients
    currently connected the server
'''
class server:
    def __init__(self, port):
        self.connectedClients = set([])
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error, msg:
            print "Failed to create socket"
            sys.exit(0)
        try:
            self.sock.bind(('', port))
        except socket.error , msg:
            print "Failed to bind to socket"
            sys.exit(0)
    '''
        closeSocket() -> releases the closes the socket and
                         frees the port currently used to create
                         socket
    '''
    def closeSocket(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

    '''
        _parseData(self,data) -> Private methord used to parse the
                                 incoming message from the client
    '''
    def _parseData(self,data):
        if data.startswith("GREETING"):
            return "GREETING"
        elif data.startswith("MESSAGE"):
            return "MESSAGE"
        else:
            return None
    '''
        _sendMessageToAll(self,data,address) -> Private methord used to
                                        send the message received from a
                                        client to all other clients connected
                                        to the server
    '''
    def _sendMessageToAll(self,data,address):
        data = "INCOMING<from "+str(address[0])+":"+str(address[1])+">"+data[8:]
        for x in self.connectedClients:
            self.sock.sendto(data,x)
    '''
        _handleIncoming(self,data,address) -> Parses the incoming message
                                to determine the type of message.
                                There are two types of messages
                                1) GREETING - Client just connected remember
                                            the client
                                2) MESSAGE - Certain client sent a message
                                            forward it to all other clients
    '''
    def _handleIncoming(self,type,data,address):
        if type is "GREETING":
            self.connectedClients.add(address)
            print "Registering client" + str(address)
        elif type is "MESSAGE":
            self._sendMessageToAll(data,address)
        else:
            print "Unknown message"

    '''
        start(self) -> A public method. Runs the server instance forever

    '''
    def start(self):
        while True:
            data , address = self.sock.recvfrom(2048);
            type = self._parseData(data)
            self._handleIncoming(type,data,address)

'''
    The controll object validates the arguments in terminal
    and instantiates the server
'''
class controll:
    def __init__(self,args):
        self.args = args
        self.sock = None

    def run(self):
        self.sock = self.check_parameters()
        if self.sock:
            print "Server Initialized..."
            self.sock.start()
        else:
            sys.exit(0)

    def signal_handler(self,signal, frame):
        print('You pressed Ctrl+C!')
        self.sock.closeSocket()
        sys.exit(0)

    def check_parameters(self):
        for x in self.args :
            if x == "-sp":
                port = int(self.args[self.args.index("-sp")+1:][0])
                s = server(port)
                return s
        else :
            print "Server port not provided\n" \
                  "Start server in following format : " \
                  "python <server_name> -sp <port_num>"
            return False



if __name__ == "__main__":
    c = controll(sys.argv)
    signal.signal(signal.SIGINT, c.signal_handler)
    c.run()


