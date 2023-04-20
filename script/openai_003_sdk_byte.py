# -*- coding: utf-8 -*-
# @FileName  : openai_003_sdk.py
# @Description
# @Author： 公众号：阿三先生
# @Date 3/27/23 4:06 PM
# @Version 1.0
import time
import json
import openai
import os
import asyncio

from setting import LOG_PATH,API_KEY
from tools.logger_conf import get_logger_conf
from tools.check_match_texts import character, func_match_text

module_name = str(os.path.basename(__file__)).split('.')[0]
logger = get_logger_conf(LOG_PATH, module_name+".log", 'INFO')

openai.api_key = API_KEY

async def openai_origin_davinci(ws_, checked_param):
    timeout_count = 0
    model = "text-davinci-003"

    try:
        data = checked_param["data"]
        start_time = time.time()
        if data["openai_parameter"]:
            response = await openai.Completion.acreate(
                engine=model,
                prompt=data["query"],
                temperature=0.0,
                max_tokens=500,
                stream=True,
                timeout=3
            )
        else:
            response = await openai.Completion.acreate(
                engine=model,
                prompt=data["query"],
                temperature=data["temperature"],
                max_tokens=data["max_tokens"],
                stop=data["stop"],
                top_p=data["top_p"],
                frequency_penalty=data["frequency_penalty"],
                presence_penalty=data["presence_penalty"],
                best_of=data["best_of"],
                stream=True,
                timeout=3
            )

        texts = ""
        async for tmp in response:
            event_time = time.time() - start_time
            # response_ms = tmp.response_ms
            # print(response_ms)
            choices = tmp["choices"]

            if choices[0]["finish_reason"] is not None and (
                    choices[0]["finish_reason"] == "stop" or choices[0]["finish_reason"] == "length"):
                texts_dict = {
                    "code": 0,
                    "msg": "ok",
                    "seq": checked_param["seq"],
                    "data": {
                        "consume_time": f"{event_time:.2f}",
                        "finish_reason": choices[0]["finish_reason"],
                        "contents": texts
                    }
                }

                logger.info(json.dumps(texts_dict, ensure_ascii=False))
                await ws_.send(json.dumps(texts_dict, ensure_ascii=False))
                await asyncio.sleep(0)
                texts = ""
                # break
            else:
                # 删除了strip()处理， 防止英文单词连片
                text = choices[0]["text"]
                # 按符号检查完整文本返回
                texts_dict = {
                    "code": 0,
                    "msg": "ok",
                    "seq": checked_param["seq"],
                    "data": {
                        "consume_time": f"{event_time:.2f}",
                        "finish_reason": choices[0]["finish_reason"],
                        "contents": text
                    }
                }

                logger.info(json.dumps(texts_dict, ensure_ascii=False))
                await ws_.send(json.dumps(texts_dict, ensure_ascii=False))
                await asyncio.sleep(0)
                texts = ""
        else:
            event_time = time.time() - start_time
            texts_dict = {
                "code": 0,
                "msg": "ok",
                "seq": checked_param["seq"],
                "data": {
                    "consume_time": f"{event_time:.2f}",
                    "finish_reason": "stop",
                    "contents": texts
                }
            }
            logger.info(json.dumps(texts_dict, ensure_ascii=False))
            await ws_.send(json.dumps(texts_dict, ensure_ascii=False))
            await asyncio.sleep(0)
            texts = ""

    except asyncio.TimeoutError:
        timeout_count += 1
        if timeout_count >= 3:
            ws_.close()
        else:
            pass
