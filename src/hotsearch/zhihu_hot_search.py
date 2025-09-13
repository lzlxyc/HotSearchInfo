import requests
import json
from typing import List
from bs4 import BeautifulSoup
from loguru import logger

from .base_hot_search import BaseHotSearch, Word


class ZhiHuHotSearch(BaseHotSearch):
    def __init__(self):
        super().__init__()
        self.save_dir = 'zhihu-search'
        self.url = "https://api.ba9.cn/api/get.zhihuhot?type=zhihu"
        # self.headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        #     'Cookie': 'SUB=_2AkMVdRtlf8NxqwJRmfoWy2_lb4V0yQvEieKjKeq-JRMxHRl-yT8XqmYatRB6PvU1ijEk4CykabQQvFhJAy31x99v4Ejs;'
        # }


    def get_hot_searches_question(self, size: int = 50) -> List[Word]:
        """
        获取知乎问题的热搜数据：暂时先不用
        """
        url = "https://www.zhihu.com/topsearch"
        try:
            response = requests.get(url, headers=self.headers)
            response.encoding = 'utf-8'

            if not response.ok:
                print(f"请求失败: {response.status_code} - {response.reason}")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            script = soup.find('script', type='text/json', id='js-initialData')

            if not script:
                logger.warning('未找到指定的script标签')
                return []

            obj = json.loads(script.string)
            # 根据实际JSON结构调整路径
            items = obj.get('initialState', {}).get('topsearch', {}).get('data', [])
            words = [{'title': item['queryDisplay'], 'url':''} for item in items]

            return words[:size]

        except Exception as e:
            logger.error(f"获取知乎热搜时出错: {e}")
            return []


    def get_hot_searches(self, size: int = 50) -> List[Word]:
        return super().get_hot_searches(size=size)




