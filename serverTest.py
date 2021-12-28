from socket import * 
import threading
import struct
import scapy.all
import time

#globalandmybechange
is_our_network = True
first_time_run = True
clients = 0
number_Win_Team = 0

# const & magic numbers
HEADER = 0xabcddcba
MESSAGETYPE = 0x2
UDP_PORT = 13117
BUFF_SIZE = 2<<10 # 2^10 is size of buffer
FORMAT = 'utf-8'
SERVER_PORT = 2088 # our port from shets
#SERVER_IP = 


class Server:

    def __init__ (self):
        if is_our_network:
            self.ip = scapy.all.get_if_addr('eth1')
        else :
            self.ip = scapy.all.get_if_addr('eth2')


    def up_udp (self, first_time_run, socketPortTcp):
        #UDP message according to the format
        message = struct.pack("IbH",HEADER,MESSAGETYPE,SERVER_PORT)

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
        while clients < 2:
            serverSocketUdp.sendto(message, ("255.255.255.255", UDP_PORT))
            time.sleep(1) 
        serverSocketUdp.close()   
        

    def server_up (self,first_time_run):
        serverSocketTcp = socket.socket(AF_INET, SOCK_STREAM)
        serverSocketTcp.bind(('', 0))




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