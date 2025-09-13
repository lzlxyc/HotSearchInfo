import re
import json
import requests
from typing import List
from loguru import logger


from .base_hot_search import BaseHotSearch, Word


class WeiBoHotSearch(BaseHotSearch):
    def __init__(self):
        super().__init__()
        self.save_dir = 'weibo-search'
        self.url = 'https://s.weibo.com/top/summary'
        # self.headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        #     'Cookie': 'SUB=_2AkMVdRtlf8NxqwJRmfoWy2_lb4V0yQvEieKjKeq-JRMxHRl-yT8XqmYatRB6PvU1ijEk4CykabQQvFhJAy31x99v4Ejs;'
        # }


    def get_hot_searches(self, size:int=50) -> List[Word]:
        """
        获取微博热搜数据
        """
        try:
            response = requests.get(self.url, headers=self.headers)
            response.encoding = 'utf-8'

            if not response.ok:
                logger.info(f"请求失败: {response.status_code} - {response.reason}")
                return []

            # 使用正则表达式匹配热搜数据:cite[1]
            regexp = r'<a href="(\/weibo\?q=[^"]+)".*?>(.+)<\/a>'
            matches = re.findall(regexp, response.text)

            words: List[Word] = []
            for match in matches:
                words.append({
                    'url': f"https://s.weibo.com/{match[0]}",
                    'title': match[1]
                })

            return words[:size]

        except Exception as e:
            logger.error(f"获取微博热搜时出错: {e}")
            return []
