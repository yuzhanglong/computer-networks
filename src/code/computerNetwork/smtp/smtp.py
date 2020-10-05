# File: smtp.py
# Description: 一个简单的邮件客户端
# Created: 2020-10-5 13:52:03
# Author: yuzhanglong
# Email: yuzl1123@163.com


import base64
from socket import *


class SMTPService:
    DEFAULT_MAIL_SERVER = "smtp.163.com"
    DEFAULT_SMTP_PORT = 25

    host = None
    port = None
    username = None
    password = None
    clientSocket = None

    def __init__(self, username, password, host=DEFAULT_MAIL_SERVER, port=DEFAULT_SMTP_PORT):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.makeSocket()
        self.sendHello()
        self.checkAuth()

    def command(self, command=[], size=1024):
        if len(command) != 0:
            for c in command:
                self.clientSocket.send(c)
        recv = self.clientSocket.recv(size)
        print(recv)
        return {
            "code": recv[:3],
            "message": recv
        }

    def makeSocket(self):
        # 创建一个名为clientSocket的套接字，并与mailserver建立TCP连接
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((self.host, self.port))
        self.clientSocket = clientSocket

    def sendHello(self):
        # 发送HELO命令并打印服务器响应。
        heloCommand = b'HELO Alice\r\n'
        self.command([heloCommand])

    def checkAuth(self):
        # 登录初始化
        authCommand = b'AUTH LOGIN\r\n'
        self.command([authCommand])

        # 用户名
        authCommand = base64.b64encode(bytes(self.username, 'ascii')) + b'\r\n'
        self.command([authCommand])

        # 密码
        authCommand = base64.b64encode(bytes(self.password, 'ascii')) + b'\r\n'
        self.command([authCommand])

    def send(self, sender, receiver, data):
        END_MESSAGE = "\r\n.\r\n"

        # 发送MAIL FROM命令并打印服务器响应。
        c = b'MAIL FROM: <' + bytes(sender, 'ascii') + b'>\r\n'
        self.command([c])

        # 发送RCPT TO命令并打印服务器响应。
        c = b'RCPT TO: <' + bytes(receiver, 'ascii') + b'>\r\n'
        self.command([c])

        # 发送DATA命令并打印服务器响应。
        c = b'DATA\r\n'
        self.command([c])

        # 发送消息数据
        if not data.startswith("\r\n"):
            data = "\r\n " + data
        self.command(
            [
                b'Subject: test message\r\n',
                b'From:""< ' + bytes(sender, 'ascii') + b'>\r\n',
                b'To:""< ' + bytes(receiver, 'ascii') + b'>\r\n',
                bytes(data, encoding='ascii'),
                bytes(END_MESSAGE, encoding='ascii')
            ]
        )
        self.quit()

    def quit(self):
        # 发送QUIT命令并获取服务器响应。
        self.command([b'QUIT\r\n'])


if __name__ == '__main__':
    SECRET_KEY = "请去邮箱设置中开通smtp服务，将密码填入这里"
    USERNAME = "yuzl1123@163.com"

    message = "I love computer networks!"
    service = SMTPService(username=USERNAME, password=SECRET_KEY)
    service.send(USERNAME, USERNAME, message)
