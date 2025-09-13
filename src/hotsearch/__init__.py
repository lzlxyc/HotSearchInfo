from .base_hot_search import HotSearchType, BaseHotSearch

from .weibo_hot_search import WeiBoHotSearch
from .zhihu_hot_search import ZhiHuHotSearch
from .douyin_hot_search import DouYinHotSearch
from .baidu_hot_search import BaiDuHotSearch
from .bili_hot_search import BiLiHotSearch


class HotSearchFactory:
    """热搜获取工厂类"""

    @staticmethod
    def create_hot_searcher(hs_type: HotSearchType) -> BaseHotSearch:
        """创建热搜获取器"""
        mapping = {
            HotSearchType.WEIBO: WeiBoHotSearch,
            HotSearchType.ZHIHU: ZhiHuHotSearch,
            HotSearchType.DOUYIN: DouYinHotSearch,
            HotSearchType.BAIDU: BaiDuHotSearch,
            HotSearchType.BILI: BiLiHotSearch
            # 可以继续添加其他平台
        }

        if hs_type not in mapping:
            raise ValueError(f"不支持的热搜类型: {hs_type}")

        return mapping[hs_type]()


# 使用示例
if __name__ == "__main__":
    # 获取微博热搜
    weibo_searcher = HotSearchFactory.create_hot_searcher(HotSearchType.BILI)
    weibo_hot_searches = weibo_searcher.run(verbose=True)

    # print(f"=== 微博热搜 Top {len(weibo_hot_searches)} ===")
    # for item in weibo_hot_searches[:10]:  # 只显示前10条
    #     print(item)