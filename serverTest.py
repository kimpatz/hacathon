from socket import * 
import threading
import struct
import scapy.all
import time

#globalandmybechange
is_our_network = True
first_time_run = True



# const & magic numbers
HEADER = 0xabcddcba
MESSAGETYPE = 0x2
UDP_PORT = 13117
BUFF_SIZE = 2<<10
FORMAT = 'utf-8'
SERVER_PORT = 2088 # our port from shets
SERVER_IP = 

def mathP ():
    q = ["0+1","0+2","1+3","1+2","8+1","1+4","5+3","1+5","6+3","7+2","3+3","4+5","5+2", "0+0"]
    a = ["1","2","4","3","9","5","8","6","9","9","6","9","7","0"]
    return q,a


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
            print('Server started, listening on IP address {ip}'.format(ip=self.ip))
        else :
             print("Game over, sending out offer requests...")

             
        server_UDP_socket = socket(AF_INET, SOCK_DGRAM)
        server_UDP_socket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) #forcing to talk
        server_UDP_socket.setsockopt(SOL_SOCKET,SO_BROADCAST,1) # open socket for broadcast 
        server_UDP_socket.bind(('',UDP_PORT)) # bind socket to udp-port
        
        # send the offer messages



    def server_up (self,first_time_run):

if __name__ == "__main__":
    first_time_run = True
    while True:
        Server().server_up(first_time_run)
        first_time_run = False