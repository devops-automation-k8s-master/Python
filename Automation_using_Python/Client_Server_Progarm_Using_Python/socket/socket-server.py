#! /usr/bin/python

from socket_client import SocketClient
import socket
import sys
import atexit

PORT=int(sys.argv[1])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST=socket.gethostname()
sock.bind((HOST, PORT))
sock.listen(5)
print('Listening on {}:{}'.format(HOST, PORT))

def close_socket():
    sock.close()

atexit.register(close_socket)

def echo_process(client_sock, data):
    if data.lower() == 'end':
        return False
    client_sock.write(data)
    return True

def get_command_handler(client_sock, params):
    print('GET: {}'.format(params))

def put_command_handler(client_sock, params):
    print('PUT: {}'.format(params))

def ls_command_handler(client_sock, params):
    print('LS: {}'.format(params))

command_handlers = {
    'get': get_command_handler,
    'put': put_command_handler,
    'ls': ls_command_handler
}

def ftp_process(client_sock, data):
    parts = data.split()
    if len(parts) == 0:
        return False
    cmd = parts[0].lower()
    if cmd in command_handlers.keys():
        command_handlers[cmd](client_sock, parts[1:])
    else:
        print('Unknown command')
        client_sock.write('Unknown Command={} Params={} '.format(cmd, parts))

while True:
    conn, addr = sock.accept()
    print('Connected: {}'.format(addr))
    client_sock = SocketClient(sock=conn)

    try:
        data = client_sock.read()
        print('COMMAND: {}'.format(data))
        ftp_process(client_sock, data)
        print('Client Closed')
    except:
        pass
    finally:
        client_sock.close()
