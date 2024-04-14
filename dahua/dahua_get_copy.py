import requests
import json
import hashlib
from requests.exceptions import Timeout

def hex_md5(data):
    # 创建一个 MD5 对象
    md5_hash = hashlib.md5()

    # 更新对象的内容
    md5_hash.update(data.encode('utf-8'))

    # 计算哈希值，并返回十六进制表示
    return md5_hash.hexdigest().upper()

def get_dahua_preset(ip, pwd):
    # ipstart = "198.1.2."
    # ipend = "112"
    ipstart = ip[:ip.rfind(".") + 1]  # 获取最后一个点之前的所有字符
    ipend = ip[ip.rfind(".") + 1:]    # 获取最后一个点之后的所有字符
    url = f"http://{ipstart + ipend}/RPC2_Login"
    print(ipstart + ipend)
    login = "admin"
    # pswd = "wlmbds123"
    pswd = pwd

    payload = "{\"method\":\"global.login\",\"params\":{\"userName\":\"admin\",\"password\":\"\",\"clientType\":\"Web3.0\",\"loginType\":\"Direct\"},\"id\":3}"
    try:
        response = requests.request("POST", url, data=payload)
        # 解析响应文本为JSON格式
        if response.text:
            response_json = json.loads(response.text)

            # 获取session值
            session_value = response_json.get("session")
            # print(response_json)
            # print("Session值:", session_value)
            # 调用函数进行加密
            # login = "admin"
            # random = "719598984"
            # realm = "Login to bf6499f25fd397be420ae185146a2047"
            # pswd = "xzdhjs123"

            # 获取 params 中的 random 和 realm 值
            params = response_json.get("params")
            if params:
                random = params.get("random")
                realm = params.get("realm")
                # print("Random值:", random)
                # print("Realm值:", realm)
            else:
                print("参数获取失败，响应内容：", response_json)

            hashed_value = hex_md5(login + ":" + random + ":" + hex_md5(login + ":" + realm + ":" + pswd))
            # print("Hex MD5 Hash:", hashed_value)

            # print(response.text)

            # 构建 payload2，将 session_value 插入到字符串中
            payload2 = f"{{\"method\":\"global.login\",\"params\":{{\"userName\":\"admin\",\"password\":\"{hashed_value}\",\"clientType\":\"Web3.0\",\"loginType\":\"Direct\",\"authorityType\":\"Default\"}},\"id\":4,\"session\":\"{session_value}\"}}"

            response2 = requests.request("POST", url, data=payload2)

            # print(response2.text)

            response2_json = json.loads(response2.text)
            result_value = response2_json.get("result")
            if result_value:
                print(result_value)
                url_download = f"http://{ipstart + ipend}/RPC2"
                payload_download = json.dumps({
                                              "method": "system.multicall",
                                              "params": [
                                                {
                                                  "method": "configManager.getConfig",
                                                  "params": {
                                                    "name": "PtzPreset"
                                                  },
                                                  "id": 370,
                                                  "session": session_value
                                                }
                                              ],
                                              "id": 371,
                                              "session": session_value
                                            })
                response_download = requests.request("POST", url_download, data=payload_download)
                # print(response_download.text)
                # 假设 response_download.text 是你要保存的 JSON 内容
                # response_text = response_download.text
                response_content = response_download.content
                # 定义要保存的文件名
                name = ipend

                # 构建文件路径
                file_path = f"backup/{name}.backup"

                # 将 JSON 数据写入文件，设置 ensure_ascii 参数为 False 和 indent 参数为 4
                # with open(file_path, 'w') as file:
                #     json.dump(response_text, file, ensure_ascii=False, indent=4)
                with open(file_path, "wb") as file:
                      file.write(response_content)
                      print("响应保存成功！")

                print(f"文件 '{file_path}' 已成功保存。")
            else:
                print("预置位请求失败，状态码：", response2.status_code)
        else:
            print("登录请求失败，状态码：", response.status_code)
    except Timeout:
        print("请求超时，请检查网络连接或者服务器状态。")

# ip = "198.1.2.104"
# pwd = "wlmbds123"
# get_dahua_preset(ip, pwd)