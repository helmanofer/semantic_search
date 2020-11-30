from search_engine.elk_search_engine import ElkSearch
from search_engine.annoy_level_search_engine import AnnoyLevelSearch
from search_engine.search_engine import SearchEngine
from utils.conf_util import read_app_yaml

conf = read_app_yaml()['searcher']
name = conf['name']
sconf = conf['searcher']


def get_searcher():
    if sconf['type'] == 'elk':
        return ElkSearch(name)
    elif sconf['type'] == 'annoy':
        return AnnoyLevelSearch(name)
    raise Exception(f"{sconf} is not implemented")


searcher: SearchEngine = get_searcher()
