from socket import *
import struct
#from scapy.all import get_if_addr
from serverTest import FORMAT

HEADER = 0xabcddcba
MESSAGETYPE = 0x2
UDP_PORT = 11457
BUFF_SIZE = 2<<10
team_name = "Desperate Programming Apes"

class Client:
    
    def __init__ (self):
        self.ip =  '127.0.0.1'
        self.connection_to_UPD()

    def connection_to_UPD(self):
        clientSocketUDP = socket(AF_INET, SOCK_DGRAM) #open socket udp
        clientSocketUDP.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
        clientSocketUDP.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #brodcasting op
        print("Client started, listening for offer requests...")
        clientSocketUDP.bind(("", UDP_PORT)) #bind ip/port
        self.serverConUDPHandler(clientSocketUDP) #send to connection handler

    def serverConUDPHandler (self,clientSocketUDP):
        try:
            pack, address = clientSocketUDP.recvfrom(BUFF_SIZE)
            print("Received offer from " + address[0] +  " attempting to connect..")
            message = struct.unpack("IBH", pack)
            self.connect_to_TCP((self.ip, message[2]))
        except:
            print("error")
            pass


    def connect_to_TCP(self,address):
        clientSocketTCP = socket(AF_INET, SOCK_STREAM)
        clientSocketTCP.connect((address[0],address[1]))
        clientSocketTCP.send(str.encode(team_name+'\n'))
        while True:
            message = clientSocketTCP.recv(BUFF_SIZE).decode(FORMAT)
            print(message)
            inputs = input()
            clientSocketTCP.send(str.ecnode(inputs +'\n'))
        print("Server disconnect, listen for offer requests...")
        self.connection_to_UPD()



Client()