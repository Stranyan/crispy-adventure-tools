import re
import request_html_result

def get_result(links):
    # 定义目标网址
    url = 'https://hifini.com/' + links
    selector = "#body > div > div > div.col-lg-9.main > div.jan.card.card-thread > div > div.message.break-all > script:nth-child(3)"

    result = request_html_result.get_result(url, selector)

    # 检查是否找到了匹配的标签
    if "ERROR" not in result:
        # print("result", result)
        info = result.string
        # print("info", info)
        if info:
            # music_title = re.findall(r'title: (.*?),', links_info)
            # music_author = re.findall(r'author:(.*?),', links_info)
            # music_url = re.findall(r'url: (.*?),', links_info)
            # print("music_title", music_title[0])
            # print("music_author", music_author[0])
            # print("music_url", music_url[0])
            # 提取音乐信息
            music_info = {}
            
            # 使用正则表达式提取信息并保存到字典中
            music_info['title'] = re.search(r"title:\s*'([^']+)'", info).group(1)
            music_info['author'] = re.search(r"author:\s*'([^']+)'", info).group(1)
            music_info['url'] = re.search(r"url:\s*'([^']+)'", info).group(1)
            
            # 打印或处理保存的音乐信息字典
            # print(music_info)
            links_info = music_info

        else:
            # print(f"没有下载方法哦")
            links_info = f"ERROR：没有下载方法哦"
    else:
        # print(f"错误: {response.status_code}")
        links_info = result

    return links_info