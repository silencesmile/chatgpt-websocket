# -*- coding: utf-8 -*-
# @FileName  : word_vec.py
# @Description
# @Author： 公众号：阿三先生
# @Date 13/3/23 6:00 PM
# @Version 1.0


import logging
from logging import Logger
import os, time
from logging.handlers import TimedRotatingFileHandler


class LoggerConfig(object):
    def __init__(self, log_path, file_name, level):
        if not os.path.exists(log_path):
            os.mkdir(log_path)

        self.file_name = file_name
        self.log_path = log_path
        self.level = self._get_log_level(level)

    def init_logger(self, file_name=None, level=None) -> Logger:
        '''
        初始化日志配置
        :param file_name:
        :param level:
        :return:
        '''

        log_file_name = self.log_path + '/' + self.file_name


        # 初始化filename和level参数
        if file_name is None:
            file_name = log_file_name
        if level is None:
            level = self.level

        log_fmt = '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
        formatter = logging.Formatter(log_fmt)

        log_file_handler = TimedRotatingFileHandler(filename=file_name, when="MIDNIGHT", interval=1, backupCount=100)
        log_file_handler.suffix = "%Y-%m-%d"
        log_file_handler.setFormatter(formatter)
        logging.basicConfig(level=self._get_log_level(level))
        log = logging.getLogger(file_name)
        log.addHandler(log_file_handler)

        return log

    def _get_log_level(self, level):
        '''
        日志级别获取
        :param level:
        :return:
        '''
        log_level = logging.INFO
        if level == 'DEBUG':
            log_level = logging.DEBUG
        elif level == 'WARNING':
            log_level = logging.WARNING
        elif level == 'ERROR':
            log_level = logging.ERROR
        return log_level


def get_logger_conf(log_path, file_name, level) -> Logger:
    return LoggerConfig(log_path, file_name, level).init_logger()

def logger_write(logger_: Logger, info, logger_type=None):
    """
    日志输出公共方法
    :param logger_:
    :param info:
    :param logger_type:
    :return:
    """
    if logger_ is not None:
        if logger_type == logging.ERROR:
            logger_.error(msg=info)
        elif logger_type == logging.DEBUG:
            logger_.debug(msg=info)
        else:
            logger_.info(msg=info)
