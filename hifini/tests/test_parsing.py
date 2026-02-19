import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

# 让测试在缺少第三方依赖时仍可导入待测模块。
fake_requests = ModuleType('requests')
fake_requests.get = lambda *args, **kwargs: None
sys.modules.setdefault('requests', fake_requests)

fake_bs4 = ModuleType('bs4')
fake_bs4.BeautifulSoup = object
sys.modules.setdefault('bs4', fake_bs4)

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import get_index_data
import get_songpage_data


class MockLink:
    def __init__(self, text, href):
        self.text = text
        self._href = href

    def get(self, key):
        if key == 'href':
            return self._href
        return None


def test_get_index_data_skips_empty_href_and_excluded_links():
    links = [
        MockLink('valid', 'thread-100.htm'),
        MockLink('empty', None),
        MockLink('excluded', 'thread-6.htm'),
        MockLink('other', 'about.htm'),
    ]
    soup_node = SimpleNamespace(find_all=lambda *_: links)

    with patch('request_html_result.get_result', return_value=soup_node):
        result = get_index_data.get_result()

    assert result == [{'name': 'valid', 'link': 'thread-100.htm'}]


def test_get_songpage_data_returns_error_when_music_fields_missing():
    page_script = SimpleNamespace(string="title: 'Song A', author: 'Singer A'")

    with patch('request_html_result.get_result', return_value=page_script):
        result = get_songpage_data.get_result('thread-100.htm')

    assert result == 'ERROR：页面缺少必要的音乐信息'
