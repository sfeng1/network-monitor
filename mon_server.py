import socket
import os
import socket
import struct
import threading
import time
import zlib
import random
import string
import requests
import ntplib
import dns.resolver
import dns.exception
import time
import datetime
from socket import gaierror
from time import ctime
from typing import Tuple, Optional, Any
import monitor_func
import pickle

server_address = '127.0.0.1'
server_port = 65240


def tcp_monitor_server():

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((server_address, server_port))

    x = server_sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE)
    if x == 0:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    print("tcp echo server online")

    while True:
        server_sock.listen(5)

        client_sock, client_address = server_sock.accept()
        print(f"Accepted connection from {client_address}")

        x = client_sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE)
        if x == 0:
            client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        conn = threading.Thread(daemon=True, target=new_connection, args=(client_sock,))
        conn.start()

    server_sock.close()
    print("server socket closed")


def monitor_connection(client_sock, monitor_name, server_data, cancel_event):

    target = server_data

    if target[0] == 'http':
        while True:
            if cancel_event.is_set() == True:
                client_sock.close()
                break
            result = monitor_func.check_server_http(target[1])
            result = ("monitor_server: " + monitor_name + " | http address: " + target[1] + " | " + "status: " + str(result[0]) + "| code:" + str(result[1]) + " | " + str(datetime.datetime.now()))
            client_sock.sendall(result.encode())
            time.sleep(int(target[2]))

    elif target[0] == 'https':
        while True:
            if cancel_event.is_set() == True:
                client_sock.close()
                break
            result = monitor_func.check_server_https(target[1], int(target[3]))
            result = ("monitor_server: " + monitor_name + " | https address: " + target[1] + " | " + "status: " + str(result[0]) + " | code:" + str(result[1]) + " | " + str(datetime.datetime.now()))
            client_sock.sendall(result.encode())
            time.sleep(int(target[2]))

    elif target[0] == 'ntp':
        while True:
            if cancel_event.is_set() == True:
                client_sock.close()
                break
            result = monitor_func.check_ntp_server(target[1])
            result = ("monitor_server: " + monitor_name + " | ntp address: " + target[1] + " | " + "online status: " + str(result[0]) + " | " + str(datetime.datetime.now()))
            client_sock.sendall(result.encode())
            time.sleep(int(target[2]))

    elif target[0] == 'dns':
        while True:
            if cancel_event.is_set() == True:
                client_sock.close()
                break
            result = monitor_func.check_dns_server_status(target[1], target[3], target[4])
            result = ("monitor_server: " + monitor_name + " | dns address: " + target[1] + " | " + "query: " + target[3] + " | type: " + target[4] + " | result: " + str(result[1]) + " | " + str(datetime.datetime.now()))
            client_sock.sendall(result.encode())
            time.sleep(int(target[2]))

    elif target[0] == 'tcp':
        while True:
            if cancel_event.is_set() == True:
                client_sock.close()
                break
            result = monitor_func.check_tcp_port(target[1], int(target[3]))
            result = ("monitor_server: " + monitor_name + "| tcp address: " + target[1] + " | " + "port: " + str(target[3]) + " | result: " + str(result[0]) + " | " "result: " + str(result[1]) + " | " + str(datetime.datetime.now()))
            client_sock.sendall(result.encode())
            time.sleep(int(target[2]))

    elif target[0] == 'udp':
        while True:
            if cancel_event.is_set() == True:
                client_sock.close()
                break
            result = monitor_func.check_udp_port(target[1], int(target[3]))
            result = ("monitor_server: " + monitor_name + "| udp address: " + target[1] + " | " + "port: " + str(target[3]) + " | result: " + str(result[0]) + " | " "result: " + str(result[1]) + " | " + str(datetime.datetime.now()))
            client_sock.sendall(result.encode())
            time.sleep(int(target[2]))

    return


def new_connection(client_sock):
    cancel_event = None

    while True:
        message = client_sock.recv(1024)
        if message:
            data = eval(message.decode())
            print(f"Received message: {data}")

            if data[0] == 'monitor':
                monitor_name = data[1]
                task_dict = data[2:]
                cancel_event = threading.Event()
                # client_sock.sendall(str(data).encode())
                monitor_thread = threading.Thread(daemon=True, target=monitor_connection, args=(client_sock, monitor_name, task_dict, cancel_event,))
                monitor_thread.start()
                continue

            elif data[0] == 'close':
                cancel_event.set()
                break
        else:
            break

if __name__ == "__main__":
    tcp_monitor_server()
