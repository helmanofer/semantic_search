__all__ = [
    'LabseEmbeddings',
    'DummyEmbeddings',
    'BertHebEmbeddings',
    'Embeddings',
    'FastTextEmbeddings',
    'embedding'
]

from embeddings.embeddings import DummyEmbeddings, Embeddings
from embeddings.bert_embeddings import LabseEmbeddings, BertHebEmbeddings
from embeddings.fasttext_embeddings import FastTextEmbeddings
from utils.conf_util import read_app_yaml


conf = read_app_yaml()['embeddings']


def get_embedding():
    if conf['class'] in globals():
        return globals()[conf['class']]()
    raise Exception(f"{conf['embeddings']} is not implemented")


embedding: Embeddings = get_embedding()
