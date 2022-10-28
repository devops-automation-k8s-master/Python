"""This program check port is open or not on remote machine."""
import socket
import logging

logger = logging.getLogger("portTest")
def porttest(config):
    clientSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    hostip=config["portTest"]["ipaddress_url"]
    hostport=int(config["portTest"]["port"])
    output=clientSock.connect_ex((hostip,hostport))
    if output==0:
        logger.debug("{} PORT IS OPEN\n".format(hostport))
    else:
        logger.debug("{} PORT IS CLOSED\n".format(hostport))
        csocket.close_socket()
