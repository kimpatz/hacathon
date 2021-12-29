from _typeshed import Self
from socket import * 
import threading
import struct
import time
import random

#globalandmybechange
is_our_network = True
first_time_run = True
num_of_connected_clients = 0
number_Of_Win_Team = 0

# const & magic numbers
HEADER = 0xabcddcba
MESSAGETYPE = 0x2
UDP_PORT = 13117
BUFF_SIZE = 2<<10 # 2^10 is size of buffer
FORMAT = 'utf-8'
SERVER_PORT = 2088 # our port from shets
#SERVER_IP = 
BROADCASTIP = "255.255.255.255"


class Server:

    def __init__ (self):
        self.ans = 0
        self.qu = ""
        #   if is_our_network:
        #    self.ip = scapy.all.get_if_addr('eth1')
        #else :
         #   self.ip = scapy.all.get_if_addr('eth2')
        self.clientList = {}
        self.ip = "127.0.0.1"


    def up_udp (self, first_time_run, message):
        #print message by the time
        #if first_time_run:
        print("Server started, listening on IP address " + self.ip)
        #else:
            #print("Game over, sending out offer requests...") # TODO

        serverSocketUdp = socket(AF_INET, SOCK_DGRAM)
        serverSocketUdp.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) # forcing to talk
        serverSocketUdp.setsockopt(SOL_SOCKET,SO_BROADCAST,1) # open socket for broadcast 
        serverSocketUdp.bind(('',UDP_PORT)) # bind socket to udp-port
        
        # send the offer messages every sec
        while num_of_connected_clients < 2:
            serverSocketUdp.sendto(message, (BROADCASTIP, UDP_PORT))
            time.sleep(1) 
        serverSocketUdp.close()   
        

    def server_connection (self,first_time_run):

        #open TCP socket connection
        serverSocketTcp = socket(AF_INET, SOCK_STREAM)
        serverSocketTcp.bind(('', 0))
        serverSocketTcpPort = (serverSocketTcp.getsockname())[1]

        #reset num of connected clients
        num_Of_conected_Clients = 0

        message = struct.pack("IBH",HEADER,MESSAGETYPE,serverSocketTcpPort)
        threadUDP = threading.Thread(target=self.up_udp, args=(first_time_run, message))
        threadUDP.start()

        serverSocketTcp.listen(2)
        while num_Of_conected_Clients < 2:
            clientSock, ip = serverSocketTcp.accept()
            print("Success connect to tcp")
            self.clientList[clientSock] = ""
            num_Of_conected_Clients += 1   #TODO maybe sync
            threading.Thread(target=self.sync_players, args=(clientSock, ip)).start()

    #  group names,  waiting for 2 groups, creating the game
    def sync_players(self, client_socket, ip):
        question, answer = mathProb()
        try:
            name = client_socket.recv(BUFF_SIZE).decode(FORMAT)
            self.clientList[client_socket] = name
            print(name)
        except:
            print("Could not receive group name")
            pass
        try:
             if (num_of_connected_clients == 2):
                 threading.Event.set()
                 self.game(client_socket) #TODO 10 sec sleep before game
             else:
               threading.Event().wait()
        except:
             print("Something wrong with client thread")
             pass

    def game(self,clientSock):
       time.sleep(10)
       players = self.clientList.values()
       players = list(players)
       message = "Welcome to Quick Maths!\n \
       Player 1: "  + players[0]+ "\n \
       Player 2: "+players[1]+"\n \
       Please answer the following question as fast as you can:\n \
       How much is "+self.qu +"?\nanswer: "
       clientSock.send(str.encode(message))





def mathProbRand():
    x = random.randrange(10)
    y = random.randrange(10)
    if x != y :
        if x < y :
            ans = y - x 
            ansString = "" + str(y) + " + " + str(x)
            return (ans,ansString)
        else :
            if x+y < 10 :
                ans = y + x
                ansString = "" + str(x) + " + "+ str(y)
                return (ans, ansString)
            else :
                x = random.randrange(4) 
                y = random.randrange(5)
                ans = y + x 
                ansString = "" + str(x) + " + " + str(y)
                return(ans,ansString)
    else : 
            x = random.randrange(3)
            y = random.randrange(6) 
            ansString = "" + str(y) + " + " + str(x)
            ans = y + x 
            return (ans,ansString)

def mathProb ():
    q = ["0+1","0+2","1+3","1+2","8+1","1+4","5+3","1+5","6+3","7+2","3+3","4+5","5+2", "0+0",
        "6-2","8-3","9-2"]
    a = ["1","2","4","3","9","5","8","6","9","9","6","9","7","0","4","5","7"]
    return q,a


if __name__ == "__main__":
    first_time_run = True
    s = Server()
    while True:
        s.server_connection(first_time_run)
        first_time_run = False