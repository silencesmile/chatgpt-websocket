import os

def project_dir(project_name):
    cwd = os.getcwd()
    pro_list = cwd.split("/")[::-1]

    pro_index = 0
    for index in range(len(pro_list)):
        if project_name in pro_list[index]:
            pro_index = index
            break

    project_path_list = pro_list[pro_index:]
    return "/".join(project_path_list[::-1])

project_path = project_dir("chatgpt-websocket")

# 日志目录配置
LOG_PATH = f'{project_path}/logs'
PROJECT_NAME = "chatgpt-websocket"

MODEL_LIST = ["text-davinci-003", "gpt-3.5-turbo", "gpt-4"]

# ws配置
# 作为ws服务端，端口
SERVICE_PORT = 8808

API_KEY = "**********"
