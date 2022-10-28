#! /usr/bin/python

from socket_client import SocketClient
import sys

HOST=sys.argv[1]
PORT=10808

DATA="""GET /?gfe_rd=cr&dcr=0&ei=KdLAWvGbIKby8Af3p5-ABQ&gws_rd=cr HTTP/1.1

"""

done = False

try:
    while not done:
        data = raw_input('Enter Command: ')
        sock = SocketClient(HOST, PORT)
        sock.write(data)
        response = sock.read()
        print('SERVER: {}'.format(response))
except:
    pass
finally:
    sock.close()
