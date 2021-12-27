from socket import *
import struct
import sys
import select

HEADER = 0xabcddcba
MESSAGETYPE = 0x2
UDP_PORT = 13117
BUFF_SIZE = 2<<10
team_name = "Desperate Programming Apes"
