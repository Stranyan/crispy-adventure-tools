import requests
from bs4 import BeautifulSoup

def get_result(url, selector):
    # 发送请求并获取页面内容
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 使用 BeautifulSoup 解析页面内容
        soup = BeautifulSoup(response.text, 'html.parser')

        finder = soup.select_one(selector)

        if finder:
            result = finder
            
        else:
            result = f"ERROR：未找到{selector}"
    else:
        result = f"ERROR: 状态码{response.status_code}"

    return result