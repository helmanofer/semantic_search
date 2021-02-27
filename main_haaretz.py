

import gzip
from utils.conf_util import conf_to_env
from indexed_docs.indexed_docs import IndexedDocs
from indexed_docs.indexed_doc import IndexedDocJsonWithEmbedding
from typing import Iterable

from tqdm import tqdm
from searcher.annoy_level_search_engine import AnnoyLevelSearch
from searcher.elk_search_engine import ElkSearch


conf_to_env()


def iter() -> Iterable[str]:
    fn = "/mnt/c/SourceCode/sematic_search/data/haarez.jsonl_labse_full.gz"
    with gzip.open(fn, "rb") as rw:
        try:
            for line in tqdm(rw):
                yield line.decode()
        except Exception as e:
            print(e)


ido = IndexedDocs(IndexedDocJsonWithEmbedding, None, None)
ido.iter = iter()
# se = AnnoyLevelSearch("haaretz_test")
se = ElkSearch("haaretz_test")
se.recreate_index()
se.index(ido)
