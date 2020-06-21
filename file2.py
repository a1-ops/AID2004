from socket import *
from time import *
host = ('127.0.0.1', 4396)

sockfd = socket()
sockfd.bind(host)
sockfd.listen(3)
# sockfd.setblocking(False)
sockfd.settimeout(3)

while True:
    print('等待客户端连接')
    try:
        connfd,addr = sockfd.accept()
        print(addr,'连接成功')
    except BlockingIOError as e:
        sleep(2)
        print('未连接')
        with open('text.txt','a') as f:
            data = '%s : %s\n'%(ctime(),f)
            f.write(data)
            f.close()
    except timeout as e:
        print('未连接')
        with open('text.txt', 'a') as f:
            data = '%s : %s\n' % (ctime(), f)
            f.write(data)
            f.close()

    else:

        data = connfd.recv(1024)
        print(data.decode())