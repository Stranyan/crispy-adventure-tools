import request_html_result

def get_result():
    url = 'https://hifini.com/'
    selector = "#body > div > div > div.col-lg-9.main > div > div.card-body > ul"
    excluded_links = ["thread-6.htm", "thread-1575.htm", "thread-16216.htm"]

    result = request_html_result.get_result(url, selector)

    if not (isinstance(result, str) and "ERROR" in result):
        links_info = []
        for link in result.find_all('a'):
            href = link.get('href')
            if not href:
                continue
            if 'thread-' in href and href not in excluded_links:
                links_info.append({'name': link.text, 'link': href})
        return links_info
    else:
        return result
