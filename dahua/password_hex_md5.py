import hashlib

def hex_md5(data):
    # 创建一个 MD5 对象
    md5_hash = hashlib.md5()

    # 更新对象的内容
    md5_hash.update(data.encode('utf-8'))

    # 计算哈希值，并返回十六进制表示
    return md5_hash.hexdigest().upper()

# 调用函数进行加密
login = "admin"
random = "719598984"
realm = "Login to bf6499f25fd397be420ae185146a2047"
pswd = "xzdhjs123"

hashed_value = hex_md5(login + ":" + random + ":" + hex_md5(login + ":" + realm + ":" + pswd))
print("Hex MD5 Hash:", hashed_value)