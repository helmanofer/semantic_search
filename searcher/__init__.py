__all__ = [
    'ElkSearch',
    'AnnoyLevelSearch',
    # 'Searcher',
    'searcher',
    'embedding',
]

from searcher.elk_search_engine import ElkSearch
from searcher.annoy_level_search_engine import AnnoyLevelSearch
# from searcher.searcher import Searcher
from utils.conf_util import read_app_yaml
from embeddings import embedding

conf = read_app_yaml()
name = conf['name']
sconf = conf['searcher']


def get_searcher():
    if sconf['class'] in globals():
        return globals()[sconf['class']](name)
    raise Exception(f"{sconf} is not implemented")


searcher = get_searcher()
