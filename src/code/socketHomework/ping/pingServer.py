import random
from socket import *

HOST = '127.0.0.1'
PORT = 8080

# 创建 UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

# 将IP地址和端口号分配给套接字
serverSocket.bind((HOST, PORT))

while True:
    print("server start...")
    # 产生0到10范围内的随机数
    rand = random.randint(0, 10)
    # 接收客户端数据包以及它来自的地址
    message, address = serverSocket.recvfrom(2048)
    # 字母大写
    message = message.upper()
    # 模拟丢包, 如果rand小于4，则我们视为数据包丢失并且不响应
    if rand < 4:
        continue
    # 否则，服务器响应
    serverSocket.sendto(message, address)
