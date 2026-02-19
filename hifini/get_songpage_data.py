import re
import request_html_result


def get_result(links):
    # 定义目标网址
    url = 'https://hifini.com/' + links
    selector = "#body > div > div > div.col-lg-9.main > div.jan.card.card-thread > div > div.message.break-all > script:nth-child(3)"

    result = request_html_result.get_result(url, selector)

    # 检查是否找到了匹配的标签
    if not (isinstance(result, str) and "ERROR" in result):
        info = result.string
        if info:
            # 提取音乐信息
            music_info = {}

            # 使用正则表达式提取信息并保存到字典中
            title_match = re.search(r"title:\s*'([^']+)'", info)
            author_match = re.search(r"author:\s*'([^']+)'", info)
            url_match = re.search(r"url:\s*'([^']+)'", info)

            if not (title_match and author_match and url_match):
                links_info = "ERROR：页面缺少必要的音乐信息"
            else:
                music_info['title'] = title_match.group(1)
                music_info['author'] = author_match.group(1)
                music_info['url'] = url_match.group(1)
                links_info = music_info
        else:
            links_info = "ERROR：没有下载方法哦"
    else:
        links_info = result

    return links_info
