# chatgpt-websocket是一个gpt对话模型的流式服务

## 安装

###Python版本
    3.8及以上

使用 pip 进行安装模块

    pip3 install -r requirements.txt

### 设置API_KEY

    API_KEY = "**********************"

## 运行

    python3 app.py
    
    或后台启动
    nohup python3 app.py >/dev/null 2>&1 & 

websocket测试网址

    http://www.ay1.cc/

##参数说明

*****请求参数*****

| 参数名称        | 必选   |  字段类型  | 取值范围  | 默认值  | 描述  |
| --------   | -----:  | :----:  | :----:  | :----:  | :----:  |
| query     | 否 |   String     |  无     |  无     |  对应gpt-3模型的文本数据(与messages至少存在一组)     |
| messages     | 否 |   List     |  无     |  无     |  对应gpt-3.5/gpt-4模型的文本数据(与query至少存在一组     |
| model     | 否 |   String     |  text-davinci-003/gpt-3.5-turbo/gpt-4     |  gpt-3.5-turbo   |  对话模型     |
| seq     | 是 |   String     |  无     |  无   |  请求唯一值，用于定位返回结果     |
| origin_stream     | 否 |   Bool     |  无     |  true   |  流式返回方式：true：按原生字节返回；false：按短句返回     |
| openai_parameter     | 否 |   Bool     |  无     |  true    |  模型请求方式：true：按openAI默认值请求；false：按传参及默认值请求     |
| temperature     | 否 |   List     |  0~1     |  0.0     |  控制响应的随机性，表示为从 0 到 1 的范围。数值越大越不稳定     |
| max_tokens     | 否 |   Float     |  1~4000     |  500     |  回复文本长度上限     |
| top_p     | 否 |   Float     |  0~1     |  1     |  控制模型应考虑完成多少随机结果(0.1表示只考虑概率质量为前10%)     |
| frequency_penalty     | 否 |   Float     |  0~2     |  0     |  频率惩罚降低了模型通过“惩罚”它逐字重复同一行的可能性     |
| presence_penalty     | 否 |   Float     |  0~2     |  0     |  存在惩罚增加了它谈论新话题的可能性。     |
| best_of     | 否 |   Int     |  1~20      |  1    |  指定要在服务器端生成的完成数 (n) 并返回“n”个完成中的最佳值     |
| stop     | 否 |   List     |  无     |  ["Human:"]     |  指定一组字符，指示 API 停止生成完成。每当 API 遇到该短语时，它将停止生成新的令牌。 不设置，可能回复多轮文本     |

*****请求示例*****

    davinci-003请求格式
    {
      "seq": "yuwrywirw89573459",
      "data": {
        "query": "杭州都有什么景色？",
        "model": "text-davinci-003"
      }
    }
    
    3.5-turbo/gpt-4请求格式
    {
      "seq": "yuwrywirw89573459",
      "data": {
        "query": "",
        "messages": [{
          "role": "system",
          "content": "AI只能用中文回复\n这是Human和AI之间的对话"
        }, {
          "role": "user",
          "content": "你是哪里人？"
        }, {
          "role": "assistant",
          "content": "我是杭州人。"
        }, {
          "role": "user",
          "content": "杭州都有什么景色？"
        }],
        "model": "gpt-3.5-turbo"
      }
    }


*****回复参数*****

| 返回字段        |  类型   | 说明  |
| --------   | -----:  | :----:  | 
| code     | Int |   0：成功，其他:异常    |  
| msg     | String |   信息提示     |  
| seq     | String |   请求唯一值     | 
| data     | Dict |   返回信息     |  
| consume_time     | String |   响应时间     |  
| finish_reason     | String |   是否结束:stop：流式结束；length：流式结束但内容未完； null：正常返回     | 
| contents     | String |   返回响应文本     | 

*****返回示例*****

    {
      "code": 0,
      "msg": "ok",
      "seq": "yuwrywirw89573459",
      "data": {
        "consume_time": "3.83",
        "finish_reason": null,
        "contents": "拥"
      }
    }
