#!/usr/bin/env python3
import sys,time,logging, socket,_thread,struct,select

logging.basicConfig(filename='service.log',filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',level=logging.DEBUG)
from inc.protocol_detection import *
try:
    from inc.config import LOCAL_IP,LOCAL_PORT,MAX_DATA_RECV
except ImportError:
    print("create config file")
    sys.exit(1)

def send_msg(sock, msg):
    logging.debug('To Proxy Request %s',msg)
    sock.sendall(msg)

def recv_msg(sock):
    return recvall(sock)

def recvall(sock):
    data = bytearray(sock.recv(MAX_DATA_RECV))
    logging.debug('Original Response %s',data)
    return data

def proxy_thread(conn):
  request = bytearray(recv_msg(conn))
  port = TCP_Protocol_Detection(request).honeypot_port()
  logging.debug('Original Request %s',request)
  logging.debug('Connection to port %s',port)
  try:
    # create a socket to connect to dockers
    honeypot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    honeypot.connect(('127.0.0.1', port))
    send_msg(honeypot,request) # send request to honeypot
    #magic loop, send response or request to other dest.
    while True:
        # wait until client or remote is available for read
        r, w, e = select.select([conn, honeypot], [], [])
        if conn in r:
            data = conn.recv(4096)
            if honeypot.send(data) <= 0:
                break
        if honeypot in r:
            data = honeypot.recv(4096)
            if conn.send(data) <= 0:
                break
    logging.debug('All connections closed')
    honeypot.close()
    conn.close()
  except socket.error as error:
    message = error
    if honeypot:
      honeypot.close()
    if conn:
      conn.close()
    print("Runtime Error:", message)
    sys.exit(1)

def run():
    print("Python {} on {}\n".format(sys.version, sys.platform))
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.debug(str(LOCAL_PORT)+' - '+str(LOCAL_IP))
    soc.bind((LOCAL_IP,LOCAL_PORT))
    soc.listen(1)
    while True:
        conn, addr = soc.accept()   
        _thread.start_new_thread(proxy_thread, (conn,))


if __name__ == "__main__":
    run()
