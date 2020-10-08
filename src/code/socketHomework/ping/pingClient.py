# File: pingClient.py
# Description: ping 客户端
# Created: 2020-10-5 13:11:48
# Author: yuzhanglong
# Email: yuzl1123@163.com


import time
from socket import *

SERVER_PORT = 8080
SERVER_HOST = "127.0.0.1"
TIME_OUT = 1

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(TIME_OUT)

for t in range(10):
    startTime = time.time()
    message = "times:" + str(t) + " start:" + str(startTime)
    clientSocket.sendto(bytes(message, encoding="utf-8"), (SERVER_HOST, SERVER_PORT))
    try:
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    except timeout:
        print("Time Out!")
    finally:
        endTime = time.time()
        print("ping:" + str((endTime - startTime) * 1000) + "ms")
clientSocket.close()
