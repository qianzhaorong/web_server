# coding: utf-8
import sys
import getopt

import socket

from config import Config
from log import Logger


class Server(object):
    def __init__(self):
        self.logger = Logger().get_logger()

    def run(self):
        host, port = self.get_system_args()
        socket_server = self.create_socket(host, int(port))
        print('server now running in: {}:{}'.format(host, port))
        self.logger.info('server now running in: {}:{}'.format(host, port))

        while True:
            new_socket, addr = socket_server.accept()

            # 接收客户端请求的报文
            request_data = self.get_request_data(new_socket)
            self.logger.info('client {}:{} connect to server success'.format(addr[0], addr[1]))
            new_socket.sendall(b'HTTP/1.1 200 OK\r\n\r\n<html><head><title>Hello</title><body>Hello</body></html>')
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
        @return: 返回一个元组：(host, port)
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
        socket_server.listen()

        return socket_server


if __name__ == '__main__':
    server = Server()
    server.run()
