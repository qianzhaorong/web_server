# coding: utf-8
import sys
import getopt

import socket
import threading

from config import Config
from log import Logger
from request import Request


class Server(object):
    def __init__(self):
        self.logger = Logger().get_logger()

    def run(self):
        host, port = self.get_system_args()
        try:
            socket_server = self.create_socket(host, int(port))
        except Exception as err:
            self.logger.error('[ERROR]port must be Integer: {}'.format(err))
            sys.exit(-1)
        print('server now running in: {}:{}'.format(host, port))
        self.logger.info('server now running in: {}:{}'.format(host, port))

        while True:
            new_socket, addr = socket_server.accept()

            # 创建一个线程来处理该请求，主线程继续监听连接
            new_thread = threading.Thread(target=self.handle_connection, args=(new_socket, addr))
            new_thread.start()

    def handle_connection(self, new_socket, addr):
        """
        处理已经连接的socket
        :param new_socket: 已经连接的socket
        :param addr: 客户端的地址，是一个元组：(clientHost, clientPort)
        :return:
        """
        # 接收客户端的请求数据
        request_data = self.get_request_data(new_socket)
        self.logger.info('[INFO]handling client: {}:{} now.'.format(addr[0], addr[1]))
        print(request_data)
        # 将浏览器发送的HTTP数据封装成Request对象
        self.request = Request(request_data.decode())
        # 将request对象交给框架去处理，并从框架那里得到response对象
        new_socket.sendall(b'HTTP/1.1 200 OK\r\n\r\nHello')
        new_socket.close()

    def get_request_data(self, new_socket):
        data = b''
        while True:
            d = new_socket.recv(1024)
            data += d

            if len(d) <= 1024:
                break

        return data

    def get_system_args(self):
        """
        获取命令行参数，可以指定host和port：
        python server.py -h <host> -p <port>
        return: 返回一个元组：(host, port)
        """
        host = Config.DEFAULT_HOST
        port = Config.DEFAULT_PORT

        try:
            opts, args = getopt.getopt(sys.argv[1:], 'h:p:')
        except getopt.GetoptError:
            print('python server.py -h <host> -p <port>')
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-h':
                host = arg
            elif opt == '-p':
                port = arg

        return host, port

    def create_socket(self, host, port=9000):
        """
        @host: 绑定的Host
        @port: 绑定的端口，默认为9000
        @return: 返回监听的套接字
        """
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 端口释放
        socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_server.bind((host, port))
        socket_server.listen(5)

        return socket_server


if __name__ == '__main__':
    server = Server()
    server.run()
