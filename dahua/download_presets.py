import requests

device_ip = "198.1.2.101"

url = f"http://{device_ip}/RPC2"

payload = {
    "method": "system.multicall",
    "params": [
        {
            "method": "configManager.getConfig",
            "params": {
                "name": "PtzPreset"
            },
            "id": 337,
            "session": "dc795152a2a76c7f0aa4110a7f74e73c"
        }
    ],
    "id": 338,
    "session": "dc795152a2a76c7f0aa4110a7f74e73c"
}

response = requests.get(url, json=payload)

if response.status_code == 200:
    print("请求成功！")
    print("响应内容:", response.json())
else:
    print("请求失败。")
    print("错误代码:", response.status_code)
    print("错误内容:", response.text)