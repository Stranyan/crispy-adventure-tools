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

    # 直接使用播放链接下载音频内容（不再经过 redirect 辅助函数）。
    url = 'https://hifini.com/' + links

    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        if 'Content-Type' in response.headers:
            content_type = response.headers['Content-Type']
            if "audio/mp4" in content_type:
                last = ".m4a"
            elif "audio/mpeg" in content_type:
                last = ".mp3"
            elif "audio/mp3" in content_type:
                last = ".mp3"
            elif "audio/wav" in content_type:
                last = ".wav"
            else:
                print(f"不支持的类型：{content_type}")
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