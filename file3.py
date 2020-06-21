import re
from socket import socket
import os
from select import *

#基础方法
# adds = ('127.0.0.1',4397)
# sockfd = socket()
# sockfd.bind(adds)
# sockfd.listen(5)
#
# connfd,addr = sockfd.accept()
# data = connfd.recv(1000)
# print(data.decode())
#
# response = 'HTTP/1.1 200 OK\r\n'
# response+='Content-Type: text/html\r\n'
# response+='\r\n'
# with open('python.html','r') as f:
#     data = f.read()
#     response+=data
#
# print(response)
# connfd.send(response.encode())


#类封装
class My:
    def __init__(self, adds=('127.0.0.1',4396), text=None):
        self.adds =adds
        self.text = text

    def start(self):  #执行函数
        #创建套接字
        sockfd = socket()
        sockfd.bind(self.adds)
        sockfd.setblocking(False)   #设置为非阻塞
        sockfd.listen(5)
        self.map = {}
        self.map[sockfd.fileno()] = sockfd
        #设置监听
        print('等待浏览器连接……')
        p = epoll()
        p.register(sockfd,EPOLLIN)
        while True:
            events = p.poll()
            for fileno,event in events:
                if fileno == sockfd.fileno():
                    connfd,addr=sockfd.accept()
                    print(addr,'有浏览器连接')
                    connfd.setblocking(False)
                    p.register(connfd,EPOLLIN)
                    self.map[connfd.fileno()] = connfd
                else:
                    self.get_data(fileno,p)
    #设置收消息
    def get_data(self,fileno,p):
        connfd = self.map[fileno]
        data = connfd.recv(1000).decode()
        if not data:
            print(connfd,'服务器已经断开连接')
            p.unregister(connfd)
            del self.map[connfd.fileno()]
            return
        # print(data)
        pattern = "[A-Z]+\s+(?P<info>/\S*)"
        result = re.match(pattern, data)
        some = result.group("info")
        print('请求内容:',some)
        self.send_data(some,connfd)
    #发送消息
    def send_data(self,some,connfd):
        file_name = self.text+some
        if some == '/':
            print('执行/函数')
            file_name+='/index.html'
            with open(file_name,'rb') as f:
                data = f.read()
            send_data = 'HTTP/1.1     200       OK\r\n'
            send_data += 'Content-Type: text/html\r\n'
            send_data += 'Content-Length:%d\r\n' % len(data)
            send_data += '\r\n'
            send_data = send_data.encode() + data
            connfd.send(send_data)
        else:
            try:
                f = open(file_name,'rb')
            except:
                send_data = 'HTTP/1.1     404       Not Found\r\n'
                send_data+= 'Content-Type: text/html\r\n'
                # send_data+= 'Content-Length:%d\r\n'%len
                send_data+='\r\n'
                send_data+='NO'
                connfd.send(send_data.encode())
                connfd.close()
            else:
                data = f.read()
                send_data = 'HTTP/1.1     200       OK\r\n'
                send_data += 'Content-Type: text/html\r\n'
                send_data += 'Content-Length:%d\r\n' % len(data)
                send_data+='\r\n'
                send_data = send_data.encode()+data
                f.close()
                connfd.send(send_data)


if __name__ == '__main__':
     httpd = My(adds = ('127.0.0.1',4397),text='../sql_text/static')
     httpd.start()