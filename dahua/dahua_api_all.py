import requests
import json
import hashlib
import datetime

def get_response(url):
    username = "admin"
    password = "wlmbds123"
    # 发送初始请求获取摘要身份验证参数
    response = requests.get(url)
    nonce = response.headers['WWW-Authenticate'].split('nonce="')[1].split('"')[0]
    realm = response.headers['WWW-Authenticate'].split('realm="')[1].split('"')[0]
    # 生成摘要身份验证的响应值
    ha1 = hashlib.md5((username + ":" + realm + ":" + password).encode()).hexdigest()
    ha2 = hashlib.md5(("GET:" + url).encode()).hexdigest()
    response = hashlib.md5((ha1 + ":" + nonce + ":00000001:randomstring:auth:" + ha2).encode()).hexdigest()

    # 构造请求头
    headers = {
        'Authorization': f'Digest username="{username}", realm="{realm}", nonce="{nonce}", uri="{url}", qop=auth, nc=00000001, cnonce="randomstring", response="{response}"'
    }

    # 发送带有摘要身份验证的请求
    response = requests.get(url, headers=headers)
    # 处理服务器的响应
    if response.status_code == 200:
        print("请求成功")
        print("应答码：" + str(response.status_code))
        print("应答头：")
        for k, v in response.headers.items():
            print(k, v)
        print("应答体已获取：" + str(response.text))
        # return response.text  # 返回响应体1
        return response.content # 返回响应体2
    else:
        print("请求失败")
        print("错误码：" + str(response.status_code))
        return None  # 返回 None，表示请求失败

def getSnapshot(ip, filename=f"image_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}"):
    url = f"http://{ip}/cgi-bin/snapshot.cgi?channel=1"
    result = get_response(url)
    if result:
        # 将响应的内容保存为图片文件
        with open(f"{filename}.jpg", "wb") as file:
            file.write(result)
    return filename

def getDeviceType(ip):
    url = f"http://{ip}/cgi-bin/magicBox.cgi?action=getDeviceType"
    return get_response(url)

def getDeviceClass(ip):
    url = f"http://{ip}/cgi-bin/magicBox.cgi?action=getDeviceClass"
    return get_response(url)
