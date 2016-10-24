'''
    Author : Vineeth Ravindra
    Description : This is a simple client program developed
                  for set1 NetSec Lab assignment. This program
                  allows multiple users chat over the network
                  using UDP sockets.
    Usage : python <server_name> -sip <serverip> -sp <port_num>
            sip - server IP    sp - port on which server is running
'''
import sys
import socket
import select
'''
    This client object maintains the client state and handles
    the client socket with the server
'''
class client:
    def __init__(self, dest):
        ''' self.dest -> (IP,Port) Tupple '''
        self.dest = dest
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error, msg:
            print "Failed to create socket"
            sys.exit(0)
    '''
       The method below runs forever, continuously polling
       the socket and the input stream to check if any data
       is available on either one of them. If there is data
       available on the socket the data is parsed and outputted
       on o/p. If there is any data on standard I/P the data is
       formatted and sent to the server
    '''
    def run(self):
        self.sock.sendto("GREETING",self.dest)
        while True:
            inputStreams = [self.sock, sys.stdin]
            sys.stdout.write("+>")
            ready_to_read, ready_to_write, in_error = \
                select.select(inputStreams, [], [])
            for sock in ready_to_read:
                if sock == self.sock:
                    # incoming message from remote server, s
                    data = sock.recv(4096)
                    if data.startswith("INCOMING"):
                        sys.stdout.write(data[8:])
                    sys.stdout.flush()
                else:
                    # user entered a message
                    msg = sys.stdin.readline()
                    self.sock.sendto("MESSAGE:"+msg,self.dest)
                    sys.stdout.flush()
'''
    The controll object validates the arguments in terminal
    and instantiates the client
'''
class controll:
    def __init__(self,args):
        self.args = args

    def check_parameters(self):
        port = None
        ip = None
        for x in self.args :
            if x == "-sip":
                ip = self.args[self.args.index("-sip")+1]
            if x == "-sp":
                port= int(self.args[self.args.index("-sp")+1:][0])
        if port is None or ip is None :
            print "Server port not provided\n" \
                  "Start server in following format : " \
                  "python <server_name> -sip <serverip> -sp <port_num>"
            return False
        else:
            return client((ip, port))

    def run(self):
        client = self.check_parameters()
        if client:
            client.run()
        else:
            sys.exit(0)

if __name__ == "__main__":
    c = controll(sys.argv)
    c.run()
