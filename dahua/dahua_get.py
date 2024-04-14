import requests
import json
import hashlib

def login(ip_address, username, password):
    url = f"http://{ip_address}/RPC2_Login"
    payload = {
        "method": "global.login",
        "params": {
            "userName": username,
            "password": "",
            "clientType": "Web3.0",
            "loginType": "Direct"
        },
        "id": 3
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # 抛出异常以处理网络请求错误
        response_json = response.json()
        session_value = response_json.get("session")
        print("Session值:", session_value)

        random = response_json.get("random")
        realm = response_json.get("realm")

        hashed_value = hex_md5(username + ":" + random + ":" + hex_md5(username + ":" + realm + ":" + password))
        print("Hex MD5 Hash:", hashed_value)

        payload2 = {
            "method": "global.login",
            "params": {
                "userName": username,
                "password": hashed_value,
                "clientType": "Web3.0",
                "loginType": "Direct",
                "authorityType": "Default"
            },
            "id": 4,
            "session": session_value
        }

        response2 = requests.post(url, json=payload2)
        return response2.text

    except requests.RequestException as e:
        print("网络请求错误:", e)
        return None
    except json.JSONDecodeError as e:
        print("JSON 解析错误:", e)
        return None

def hex_md5(data):
    md5_hash = hashlib.md5()
    md5_hash.update(data.encode('utf-8'))
    return md5_hash.hexdigest().upper()

if __name__ == "__main__":
    ip_address = "198.1.2.112"
    username = "admin"
    password = "xzdhjs123"
    response_text = login(ip_address, username, password)
    if response_text:
        print(response_text)
