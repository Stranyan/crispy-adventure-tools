import requests
import hashlib

# 请求地址和参数
url = "http://198.1.2.107/cgi-bin/snapshot.cgi?channel=1"
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
    print("应答体：" + "response.text")
    response_text = response.content

    # 将响应的内容保存为图片文件
    with open("image_file.jpg", "wb") as file:
        file.write(response_text)
else:
    print("请求失败")
    print("错误码：" + str(response.status_code))

