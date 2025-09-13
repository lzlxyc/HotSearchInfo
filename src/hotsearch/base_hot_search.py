import os
import abc
import json
import time
import requests
from typing import List, Dict, Any
from enum import Enum
from datetime import datetime
import os
from pathlib import Path


# 定义数据类型
Word = Dict[str, Any]

class HotSearchType(str, Enum):
    """热搜平台类型枚举"""
    WEIBO = "微博"
    DOUYIN = "抖音"
    BAIDU = "百度"
    ZHIHU = "知乎"
    BILI = "哔哩哔哩"
    # TOUTIAO = "今日头条"

    @classmethod
    def list(cls):
        return [t.value for t in cls]


class BaseHotSearch(abc.ABC):
    """热搜获取基类
    1、每个搜索类需要继承该基类
    2、需要指定数据保存的路径：self.save_dir=xxx
    3、需要实现特定的get_hot_searches方法
    """
    def __init__(self):
        self.save_dir = 'base'
        self.url = '传入特定的网站url'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Cookie': 'SUB=_2AkMVdRtlf8NxqwJRmfoWy2_lb4V0yQvEieKjKeq-JRMxHRl-yT8XqmYatRB6PvU1ijEk4CykabQQvFhJAy31x99v4Ejs;'
        }



    @abc.abstractmethod
    def get_hot_searches(self, size: int = 50) -> List[Word]:
        '''
        {
            'index': 21,
            'title': '其余五常大概有多长时间能达到df-5c全球轰炸的标准？',
            'hotTag': None,
            'hot': '72万',
            'url': 'https://www.zhihu.com/question/1947248129930934028',
            'mobilUrl': 'https://www.zhihu.com/question/1947248129930934028'
        },
        '''
        response = requests.get(self.url, headers=self.headers)
        data = response.json()
        if not response.ok:
            return []

        items = data['data']
        return [{'title': item['title'], 'hot': item.get('hot',-1), 'url':item['url']}
                for item in items][:size]


    def _merge_words(self, new_words: List[Word], existing_words: List[Word]) -> List[Word]:
        """
        合并新旧热搜数据
        """
        # 简单的合并逻辑 - 在实际应用中可能需要更复杂的去重逻辑
        merged = existing_words.copy()
        for new_word in new_words:
            if not any(word['title'] == new_word['title'] for word in merged):
                merged.append(new_word)

        return merged


    def save_data(self, data: List[Dict], file_path: str) -> None:
        """
        保存数据到JSON文件
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"数据已保存到: {file_path}")
        except Exception as e:
            print(f"保存数据时出错: {e}")


    def run(self, verbose: bool = False):
        """
        主函数
        """
        # 获取当前日期
        yyyyMMdd = datetime.now().strftime("%Y-%m-%d")

        # 获取热搜数据
        words = self.get_hot_searches()

        if not words:
            print("未获取到热搜数据")
            return

        # 文件路径
        raw_dir = Path(f"../../databases/{self.save_dir}")
        raw_dir.mkdir(parents=True, exist_ok=True)
        full_path = raw_dir / f"{yyyyMMdd}.json"

        # 检查是否已有数据文件
        words_already_downloaded: List[Word] = []
        if full_path.exists():
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    words_already_downloaded = json.load(f)
            except Exception as e:
                print(f"读取现有数据时出错: {e}")

        # 合并数据
        words_all = self._merge_words(words, words_already_downloaded)

        # 保存数据
        self.save_data(words_all, str(full_path))

        print(f"成功获取并保存 {len(words)} 条微博热搜数据")

        if verbose:
            # 打印前10条热搜
            print("\n=== 微博热搜TOP10 ===")
            for i, word in enumerate(words[:10], 1):
                print(f"{i}. {word['title']}")