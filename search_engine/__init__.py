from search_engine.elk_search_engine import ElkSearch
from search_engine.annoy_level_search_engine import AnnoyLevelSearch
from search_engine.search_engine import SearchEngine
from utils.conf_util import read_app_yaml

conf = read_app_yaml()['searcher']


def get_searcher():
    if conf['type'] == 'elk':
        return ElkSearch(conf['name'])
    elif conf['type'] == 'annoy':
        return AnnoyLevelSearch(conf['name'])
    raise Exception(f"{conf['searcher']} is not implemented")


searcher: SearchEngine = get_searcher()
