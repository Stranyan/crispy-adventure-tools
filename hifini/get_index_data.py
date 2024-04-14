import request_html_result

def get_result():
    url = 'https://hifini.com/'
    selector = "#body > div > div > div.col-lg-9.main > div > div.card-body > ul"
    excluded_links = ["thread-6.htm", "thread-1575.htm", "thread-16216.htm"]

    result = request_html_result.get_result(url, selector)

    if "ERROR" not in result:
        links_info = [{'name':link.text, 'link':link.get('href')} for link in result.find_all('a') if 'thread-' in link.get('href') and link.get('href') not in excluded_links]
        return links_info
    else:
        return result