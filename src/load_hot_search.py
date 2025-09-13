from hotsearch import HotSearchType, HotSearchFactory


def load_all_hot_search_api():
    '''获取所有热搜数据'''
    for hs_type in HotSearchType.list():
        hs_searcher = HotSearchFactory.create_hot_searcher(hs_type)
        hs_searcher.run(verbose=True)


if __name__ == '__main__':
    load_all_hot_search_api()