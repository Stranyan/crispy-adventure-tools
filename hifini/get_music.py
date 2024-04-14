import requests

def redirect(links):
    url = 'https://hifini.com/' + links

    # 发送 HTTP 请求，关闭自动重定向
    response = requests.get(url, allow_redirects=False)

    if response.status_code // 100 == 3:
        # 获取重定向链接
        redirect_url = response.headers['Location']
        
        # print(f"Redirect URL: {redirect_url}")
    else:
        # 处理非重定向响应...
        print(f"Status Code: {response.status_code}")
        redirect_url = f"Status Code: {response.status_code}"
    return redirect_url

def get_result(links, name):

    # url = redirect(links)
    url = 'https://hifini.com/' + links

    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        if 'Content-Type' in response.headers:
            Content_Type = response.headers['Content-Type']
            if "audio/mp4" in Content_Type:
                last = ".m4a"
            elif "audio/mpeg" in Content_Type:
                last = ".mp3"
            elif "audio/mp3" in Content_Type:
                last = ".mp3"
            elif "audio/wav" in Content_Type:
                last = ".wav"
            else:
                print(f"不支持的类型：{Content_Type}")
                last = ""

            file_name = name + last
            # 保存文件
            try:
                with open(file_name, 'wb') as file:
                    file.write(response.content)
                    print(f"下载成功：{file_name}")
            except OSError as e:
                print(f"Error saving file: {e}")
        else:
            print("检测不到文件类型")

    else:
        print(f"错误: {response.status_code}")