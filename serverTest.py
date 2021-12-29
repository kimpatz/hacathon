from socket import *
import threading
import struct
import time
import random
from scapy.all import get_if_addr

#globalandmybechange
is_our_network = True
first_time_run = True
num_of_connected_clients = 0
number_Of_Win_Team = 0

# const & magic numbers
HEADER = 0xabcddcba
MESSAGETYPE = 0x2
UDP_PORT = 2088
BUFF_SIZE = 2<<10 # 2^10 is size of buffer
FORMAT = 'utf-8'
SERVER_PORT = 2088 # our port from shets
#SERVER_IP =
BROADCASTIP = "255.255.255.255"

class Server:

    def __init__ (self):
        self.ans = 0
        self.qu = ""
        if is_our_network:
            self.ip = scapy.all.get_if_addr('eth1')
        else :
            self.ip = scapy.all.get_if_addr('eth2')
        self.clientList = {}
        #self.ip = "127.0.0.1"

    def up_udp (self, first_time_run, message):
        #print message by the time
        if first_time_run:
            print("Server started, listening on IP address " + self.ip)
        else:
            print("Game over, sending out offer requests...") # TODO
            #TODO close server tcp socket

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
            th = threading.Thread(target=self.sync_players, args=(clientSock, ip,serverSocketTcp,num_Of_conected_Clients))
            th.start()
            #th.join()
    #  group names,  waiting for 2 groups, creating the game
    def sync_players(self, client_socket, ip,serverSocketTcp,num_Of_conected_Clients):
        question, answer = mathProbRand()
        self.qu = question
        self.ans = answer
        count = 0
        try:
            print("preper to get name")
            name = client_socket.recv(BUFF_SIZE).decode(FORMAT)
            self.clientList[client_socket] = name
            print("welcome " + name)
        except:
            print("Could not receive group name")
            pass
        try:
                print(str(num_Of_conected_Clients))
                #print("before game")
                # threading.Event.set()
                self.game()  # TODO 10 sec sleep before game
                print("after game")
        except:
             print("Something wrong with client thread")
             pass

    def game(self):
        while len(self.clientList) < 2:
            continue
        time.sleep(10)
        print("ani ba gameeeeeeeeeeeeeeeeeeee")
        group1soc = list(self.clientList.keys())[0]
        group2soc = list(self.clientList.keys())[1]
        group_name1 = list(self.clientList.values())[0]
        group_name2 = list(self.clientList.values())[1]
        print("ani ba 111111111")
        print("ani ba 2222222222")
        message = "Welcome to Quick Maths.\nPlayer 1: " + group_name1 + "Player 2: " +group_name2 + "\nPlease answer the following question as fast as you can:\nHow much is " + self.qu + "?\nanswer: "
        print("ani ba 33333333")
        group1soc.send(str.encode(message + '\n'))
        group2soc.send(str.encode(message + '\n'))
        print("ani ba 44444444")
        try:
            start = time.time()
            print("ani ba bsartttt")
            ans1 = group1soc.recv(BUFF_SIZE).decode(FORMAT)
            print("ani ba ans11")
            ans2 = group2soc.recv(BUFF_SIZE).decode(FORMAT)
            print("ani ba ans22")
            end = time.time()
            print("ani ba 5555555555")
        except:
            print("big problem!!!")
        if end - start >= 10:
            message = "Game over!\nThe correct answer was : " + self.ans + "\nThe game ended in a draw \n "
            group1soc.send(str.encode(message))
            group2soc.send(str.encode(message))
            print(self.ans)
        if int(ans1) == self.ans and int(ans2) != self.ans:
            message = "Game over!\nThe correct answer was " +str(self.ans) + "!\nCongratulations to the winner: "+ self.clients[group1soc]+"" # TODO CHANGE
            group1soc.send(str.encode(message))
            group2soc.send(str.encode(message))
        elif int(ans1) != self.ans and int (ans2) == self.ans:
            message = "Game over!\nThe correct answer was " +str(self.ans) + "!\nCongratulations to the winner: "+ group_name2+""
            group1soc.send(str.encode(message))
            group2soc.send(str.encode(message))
       # else:
        #    message =  "Game over!\nThe correct answer was : " + self.ans + "\nThe game ended in a draw \n "
        #    group1soc.send(str.encode(message))
        #    group2soc.send(str.encode(message))




def mathProbRand():
    x = random.randrange(10)
    y = random.randrange(10)
    if x != y :
        if x < y :
            ans = y - x
            ansString = "" + str(y) + " + " + str(x)
            return (ansString, ans)
        else :
            if x+y < 10 :
                ans = y + x
                ansString = "" + str(x) + " + "+ str(y)
                return (ansString, ans)
            else :
                x = random.randrange(4)
                y = random.randrange(5)
                ans = y + x
                ansString = "" + str(x) + " + " + str(y)
                return (ansString, ans)
    else :
            x = random.randrange(3)
            y = random.randrange(6)
            ansString = "" + str(y) + " + " + str(x)
            ans = y + x
            return (ansString,ans)

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