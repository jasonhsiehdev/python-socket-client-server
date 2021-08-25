#!/usr/bin/env python3
import socket
import time

PORT = 4096
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
MSG_DISCONNECT = "DISCONNECTED"


def SocketConnect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client


def SocketSend(client, msg):
    message = msg.encode(FORMAT)
    client.send(message)


def SocketStart():
    conn = SocketConnect()
    while True:
        msg = input("Message (q for quit): ")

        if msg == 'q':
            break

        SocketSend(conn, msg)
        msg = conn.recv(1024).decode(FORMAT)
        print(f"[PY_CLIENT] {msg}")

    SocketSend(conn, MSG_DISCONNECT)
    time.sleep(1)
    print('Disconnected')


SocketStart()
