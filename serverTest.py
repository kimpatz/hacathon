from socket import * 
import threading
import struct
import scapy.all
import time

#globalandmybechange
is_our_network = True
first_time_run = True
num_Of_conected_Clients = 0
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
        if is_our_network:
            self.ip = scapy.all.get_if_addr('eth1')
        else :
            self.ip = scapy.all.get_if_addr('eth2')



    def up_udp (self, first_time_run, message):
        #print message by the time 
        if first_time_run:
            print("Server started, listening on IP address" + self.ip)
        else :
             print("Game over, sending out offer requests...")

        serverSocketUdp = socket(AF_INET, SOCK_DGRAM)
        serverSocketUdp.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) #forcing to talk
        serverSocketUdp.setsockopt(SOL_SOCKET,SO_BROADCAST,1) # open socket for broadcast 
        serverSocketUdp.bind(('',UDP_PORT)) # bind socket to udp-port
        
        # send the offer messages every sec
        while num_Of_conected_Clients < 2:
            serverSocketUdp.sendto(message, (BROADCASTIP, UDP_PORT))
            time.sleep(1) 
        serverSocketUdp.close()   
        

    def up_Server (self,first_time_run):

        #open TCP SOCKET connection
        serverSocketTcp = socket.socket(AF_INET, SOCK_STREAM)
        serverSocketTcp.bind(('', 0))
        serverSocketTcpPort = (serverSocketTcp.getsockname())[1]

        #reset num of connected clients
        num_Of_conected_Clients = 0
        0
        #UDP message according to the format
        message = struct.pack("IbH",HEADER,MESSAGETYPE,serverSocketTcpPort)
        #start threding udp
        threadUDP = threading.Thread(target=self.up_udp, args=(first_time_run , message))
        threadUDP.start()





def mathProb ():
    q = ["0+1","0+2","1+3","1+2","8+1","1+4","5+3","1+5","6+3","7+2","3+3","4+5","5+2", "0+0",
        "6-2","8-3","9-2"]
    a = ["1","2","4","3","9","5","8","6","9","9","6","9","7","0","4","5","7"]
    return q,a


if __name__ == "__main__":
    first_time_run = True
    while True:
        Server().server_up(first_time_run)
        first_time_run = False