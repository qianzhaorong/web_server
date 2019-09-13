# coding: utf-8
import os
from datetime import datetime

import logging as dbg

from config import Config

"""
打日志时需要做的工作：
1. 如果logs目录下没有创建今天的日志文件夹，那么需要自己创建文件夹，
文件夹命名为：20190913

2. 如果文件夹有了，日志文件没有，那么需要创建日志文件，
日志文件命名为：server.log
"""


class Logger(object):
    def __init__(self):
        self.log_handler = LogFileHandler()

    def get_logger(self):
        file_name = self.log_handler.get_file_name()
        dbg.basicConfig(level=dbg.DEBUG,
                        filename=file_name,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = dbg.getLogger(__name__)
        return logger


class LogFileHandler(object):
    """
    """
    def __init__(self):
        pass

    def _get_year_month_day(self):
        date = datetime.now()
        year = date.year
        month = date.month
        day = date.day

        if month < 10:
            month = '0' + str(month)

        if day < 10:
            day = '0' + str(day)

        return str(year), str(month), str(day)

    def get_file_name(self):
        # 获取今天的日期
        year, month, day = self._get_year_month_day()
        # 判断logs目录下是否有目录，没有则创建
        log_directory = year + month +day
        if not os.path.exists(os.path.join(Config.DEFAULT_LOG_PATH, log_directory)):
            os.mkdir(os.path.join(Config.DEFAULT_LOG_PATH, log_directory))

        file_name = os.path.join(Config.DEFAULT_LOG_PATH, log_directory, Config.DEFAULT_LOG_NAME)
        return file_name

if __name__ == '__main__':
    logFileHandler = LogFileHandler()
    file_name = logFileHandler.get_file_name()
    print(file_name)
