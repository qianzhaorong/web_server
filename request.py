class Request(object):
    def __init__(self, data):
        self.path = ''
        self.method = 'GET'
        self.param = {}
        self.headers = {}
        self.cookies = {}
        self.body = ''
        self._initial_object(data)

    def _initial_object(self, data):
        """
        将浏览器发送过来的data封装成Request对象
        :param data: 浏览器发送的HTTP数据
        :return: Request对象
        """
        data_split = data.split('\r\n')
        if len(data_split) < 3:
            return

        # 请求方法
        self.method = data_split[0].split()[0]

        # 解析请求路径和参数
        request_line = data_split[0]
        self.parse_path_and_param(request_line)

        # 获取请求体
        self.body = data_split[-1]

        # 获取请求头
        for header in data_split[1:-1]:
            if ':' in header:
                key = header.split(':')[0]
                value = header.split(':')[1]
                self.headers[key] = value

                if key.lower() == 'cookies':
                    self.cookies[key] = value

    def parse_path_and_param(self, request_line):
        """
        解析请求的路径和请求参数，例如：GET /index?a=1&b=2 HTTP/1.1
        path = /index
        param = {'a': 1, 'b': 2}
        :param request_line: HTTP报文中的首行
        :return:
        """
        uri = request_line.split()[1]
        self.path = uri.split('?')[0]
        params = uri.split('?')[1]

        for param in params.split('&'):
            self.param[param.split('=')[0]] = param.split('=')[1]


if __name__ == '__main__':
    data = 'POST /index?a=1&b=2 HTTP/1.1\r\nHost:baidu.com\r\nCookies: abc\r\n\r\nHello'
    r = Request(data)
    print(234)