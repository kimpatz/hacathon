from socket import *
import struct
import keyboard
import sys
import select

HEADER = 0xabcddcba
MESSAGETYPE = 0x2
UDP_PORT = 13117
BUFF_SIZE = 2<<10
team_name = "Desperate Programming Apes"

class Client:

  

    def connection_to_UPD(self):
        clientSocketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientSocketUDP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        clientSocketUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        print("Client started, listening for offer requests...")
        clientSocketUDP.bind(("", UDP_PORT))
        self.serverConUDP(clientSocketUDP)

    def serverConUDP (self,clientSocketUDP):
        try:
            pack, address = clientSocketUDP.recvfrom(BUFF_SIZE)
            print("Received offer from " + address[0]+", attempting to connect..")
            message = struct.unpack("IBH",pack)
            self.connect_to_TCP(('127.0.0.1',message[2]))
        except:
            pass


    def connect_to_TCP(self,address):
        client_tcp_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_tcp_socket.connect((address[0],address[1]))
        client_tcp_socket.send(bytes(self.group_name+"\n", "utf-8"))
        while True:
            message = client_tcp_socket.recv(BUFF_SIZE)
            print(message.decode('utf-8'))
            my_answer = keyboard.read_key()
            client_tcp_socket.send(bytes(my_answer + "\n", "utf-8"))



Client()