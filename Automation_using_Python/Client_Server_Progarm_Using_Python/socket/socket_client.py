#! /usr/bin/python

import socket

class SocketClient:
    def __init__(self, host=None, port=None, sock=None):
        if sock == None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
        else:
            self.sock = sock

    def write(self, data):
        totalsent = 0
        while totalsent < len(data):
            sentcount = self.sock.send(data[totalsent:])
            totalsent += sentcount
        return totalsent

    def read(self):
        return self.sock.recv(8096)

    def close(self):
        return self.sock.close()
