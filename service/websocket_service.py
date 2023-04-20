# -*- coding: utf-8 -*-
# @FileName  : word_vec.py
# @Description
# @Author： 公众号：阿三先生
# @Date 13/3/23 6:00 PM
# @Version 1.0
import openai
import websockets
import websockets.exceptions
import logging
import json
import os
import asyncio
import time

from tools.logger_conf import LoggerConfig
from script.openai_003_sdk import openai_davinci
from script.openai_turbo_sdk import openai_turbo
from script.openai_003_sdk_byte import openai_origin_davinci
from script.openai_turbo_sdk_byte import openai_origin_turbo
from setting import LOG_PATH, MODEL_LIST, PROJECT_NAME
from tools.logger_conf import get_logger_conf


module_name = str(os.path.basename(__file__)).split('.')[0]
logger = get_logger_conf(LOG_PATH, module_name + ".log", 'INFO')

class WebsocketServer(object):

    def __init__(self, port: int, logger: logging.Logger = None):
        self._logger = logger
        self._ws_port = port
        self._logger.info(f"loading project ==> ")

    def check_params(self, request_param):
        # msg = eval(param)
        try:
            param = eval(request_param)
            if not isinstance(param, dict):
                raise KeyError(f"json.decoder.JSONDecodeError")
        except Exception as e:
            raise KeyError(f"json.decoder.JSONDecodeError:{str(e)}")

        seq = param.get("seq", "").strip()
        data = param.get("data", {})

        if not isinstance(seq, str) or len(seq) <= 0:
            raise ValueError("param seq error", "seq not find")

        if not isinstance(data, dict) or len(data) <= 0:
            raise ValueError("param data error", seq)

        query = data.get("query", "").strip()
        messages = data.get("messages", [])
        origin_stream = data.get("origin_stream", True)
        openai_parameter = data.get("openai_parameter", True)
        model = data.get("model", "gpt-3.5-turbo").strip()
        max_tokens = data.get("max_tokens", 500)
        temperature = data.get("temperature", 0.0)
        top_p = data.get("top_p", 1)
        frequency_penalty = data.get("frequency_penalty", 0.0)
        presence_penalty = data.get("presence_penalty", 0.0)
        stop = data.get("stop", ["Human:"])
        best_of = data.get("best_of", 1)

        if model == "gpt-3.5-turbo" or model == "gpt-4":
            if not isinstance(messages, list) or len(messages) <= 0:
                raise ValueError(f"param messages error", seq)
        elif model == "text-davinci-003":
            if not isinstance(query, str) or len(query) <= 0:
                raise ValueError(f"param query error", seq)

        if not isinstance(origin_stream, bool):
            raise ValueError(f"param origin_stream error", seq)

        if not isinstance(openai_parameter, bool):
            raise ValueError(f"param openai_parameter error", seq)

        if not isinstance(model, str) or len(model) <= 0 or model not in MODEL_LIST:
            raise ValueError(f"param model error", seq)

        if not isinstance(max_tokens, int) or (max_tokens < 1 or max_tokens > 4097):
            raise ValueError(f"param max_tokens out of range(0~4097): {max_tokens}", seq)

        if not isinstance(float(temperature), float) or (temperature < 0.0 or temperature > 1.0):
            raise ValueError(f"param temperature out of range(0~1.0): {temperature}", seq)

        if not isinstance(float(top_p), float) or (top_p < 0.0 or top_p > 1.0):
            raise ValueError(f"param top_p out of range(0.0~1.0): {top_p}", seq)

        if not isinstance(float(frequency_penalty), float) or (frequency_penalty < 0.0 or frequency_penalty > 2.0):
            raise ValueError(f"param frequency_penalty out of range(0.0~2.0): {frequency_penalty}", seq)

        if not isinstance(float(presence_penalty), float) or (presence_penalty < 0.0 or presence_penalty > 2.0):
            raise ValueError(f"param presence_penalty out of range(0.0~2.0): {presence_penalty}", seq)

        if not isinstance(best_of, int) or (best_of < 0 or best_of > 20):
            raise ValueError(f"param best_of out of range(0~20): {best_of}", seq)

        if not isinstance(stop, list) or len(stop) <= 0:
            raise ValueError("param stop error", seq)

        checked_param = {
            "query": query,
            "messages": messages,
            "model": model,
            "origin_stream": origin_stream,
            "openai_parameter": openai_parameter,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "stop": stop,
            "best_of": best_of
        }

        tmp_param = {
            "seq": seq,
            "data": checked_param
        }
        return tmp_param

    async def __ws_msg_handler(self, ws_: websockets.WebSocketServerProtocol, path):
        # self._logger.info(f"new client connected -> path ::: {path} ::: {ws_.remote_address}")
        while True:
            try:
                msg = await ws_.recv()
                logger.info(f"received msg ==> {msg}")

                # 参数校验
                checked_param = self.check_params(msg)

                logger.info(f"rec:{json.dumps(checked_param, ensure_ascii=False)}")

                if checked_param["data"]["model"] == "text-davinci-003":
                  if checked_param["data"]["origin_stream"]:
                    await openai_origin_davinci(ws_, checked_param)
                  else:
                    await openai_davinci(ws_, checked_param)
                elif checked_param["data"]["model"].strip() in MODEL_LIST:
                    if checked_param["data"]["origin_stream"]:
                      await openai_origin_turbo(ws_, checked_param)
                    else:
                      await openai_turbo(ws_, checked_param)

            except websockets.exceptions.ConnectionClosedOK:
                logger.info(f"client connection closed -> path ::: {path} ::: {ws_.remote_address}")
                break
            except KeyError as e:
                resp = {
                    "code": 129001,
                    "msg": str(e.args[0]),
                    "seq": None,
                    "data": {
                        "consume_time": "0.00",
                        "finish_reason": "stop",
                        "contents": ""
                    }
                }
                logger.info(json.dumps(resp, ensure_ascii=False))
                await ws_.send(json.dumps(resp, ensure_ascii=False))

            except ValueError as e:
                resp = {
                    "code": 129002,
                    "msg": str(e.args[0]),
                    "seq": str(e.args[1]),
                    "data": {
                        "consume_time": "0.00",
                        "finish_reason": "stop",
                        "contents": ""
                    }
                }
                logger.info(json.dumps(resp, ensure_ascii=False))
                await ws_.send(json.dumps(resp, ensure_ascii=False))

            except Exception as e:
                resp = {
                    "code": 129003,
                    "msg": str(e.args[0]),
                    "seq": None,
                    "data": {
                        "consume_time": "0.00",
                        "finish_reason": "stop",
                        "contents": ""
                    }
                }
                logger.info(json.dumps(resp, ensure_ascii=False))
                await ws_.send(json.dumps(resp, ensure_ascii=False))

    def run_forever(self):
        """
        启动websocket服务端
        Returns:
            无返回
        """
        logger.info("websocket starting")
        ws_server = websockets.serve(self.__ws_msg_handler, host='0.0.0.0', port=self._ws_port)
        # websockets.setdefaulttimeout(3)
        asyncio.get_event_loop().run_until_complete(ws_server)
        asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    logger = LoggerConfig(LOG_PATH, PROJECT_NAME, "DEBUG").init_logger( )
    websocket = WebsocketServer(8808, logger)
    websocket.run_forever()
