import requests
import json
from typing import List
from bs4 import BeautifulSoup
from loguru import logger

from .base_hot_search import BaseHotSearch, Word


class BiLiHotSearch(BaseHotSearch):
    def __init__(self):
        super().__init__()
        self.save_dir = 'bili-search'
        self.url = "https://api.ba9.cn/api/get.bilihot?type=bilihot"


    def get_hot_searches(self, size: int = 50) -> List[Word]:
        return super().get_hot_searches(size=size)