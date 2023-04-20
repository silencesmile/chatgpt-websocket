# -*- coding: utf-8 -*-
# @FileName  : word_vec.py
# @Description TODO
# @Author： 公众号：阿三先生
# @Date 13/3/23 6:00 PM
# @Version 1.0

import logging
logging.basicConfig(level="INFO")
logger = logging.getLogger()

from setting import *
from service.websocket_service import WebsocketServer

if __name__ == '__main__':
    WebsocketServer(SERVICE_PORT, logger).run_forever()
