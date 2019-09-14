class Request(object):
    def __init__(self, data):
        self.path = ''
        self.method = 'GET'
        self.param = ''
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
        pass