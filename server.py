#!/usr/bin/env python3
import socket 
import threading


PORT = 4096
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
MSG_DISCONNECT = "DISCONNECTED"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clientsSet = set()
clientsLock = threading.Lock()

def HandleClient(conn, addr):
    print(f"[PY_SERVER] new client {addr} Connected")
    try: 
        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break

            if msg == MSG_DISCONNECT:
                connected = False

            print(f"[PY_SERVER] [{addr}] {msg}")
            with clientsLock:
                for c in clientsSet:
                    c.sendall(f"[{addr}] {msg}".encode(FORMAT))

    finally:
        with clientsLock:
            clientsSet.remove(conn)

        conn.close()

def SocketStart():
    print("[PY-SERVER] STARTED")
    server.listen()
    while True:
        conn, addr = server.accept()
        with clientsLock: # context manager
            clientsSet.add(conn)
        thread = threading.Thread(target=HandleClient, args=(conn, addr))
        thread.start()



SocketStart()


