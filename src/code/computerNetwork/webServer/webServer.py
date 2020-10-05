# File: webServer.py
# Description: web服务器
# Created: 2020-10-5 12:14:52
# Author: yuzhanglong
# Email: yuzl1123@163.com


from socket import *

HOST = '127.0.0.1'
PORT = 8080
CONNECTION_MAX_SIZE = 1
TCP_MAX_SIZE = 2048

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((HOST, PORT))

# 让服务器聆听来自客户端的TCP连接请求 参数为请求连接的最大数目
serverSocket.listen(CONNECTION_MAX_SIZE)

while True:
    print("Ready to serve...")

    # 创建了一个新的套接字，由这个特定的客户专用
    connectionSocket, addr = serverSocket.accept()
    try:
        # 读取 request
        message = connectionSocket.recv(TCP_MAX_SIZE)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.readlines()

        # 发送首部
        headers = 'HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n'
        connectionSocket.send(bytes(headers, encoding='utf-8'))

        # 发送主体
        for i in range(0, len(outputdata)):
            connectionSocket.send(bytes(outputdata[i], encoding='utf-8'))

    except IOError:
        # 404
        headers = 'HTTP/1.1 404 Not Found\nContent-Type: text/html; charset=utf-8\n\n'
        connectionSocket.send(bytes(headers, encoding='utf-8'))
        connectionSocket.send(bytes("404 Not Found", encoding='utf-8'))
    finally:
        # 关闭连接套接字
        connectionSocket.close()
