from embedding.embbeding import DummyEmbedding, Embedding
from embedding.bert_embeddings_model import LabseEmbeddingModel
from utils.conf_util import read_app_yaml

conf = read_app_yaml()


def get_embedding():
    if conf['embedding'] == 'labse':
        return LabseEmbeddingModel()
    elif conf['embedding'] == 'DummyEmbedding':
        return DummyEmbedding()
    raise Exception(f"{conf['embedding']} is not implemented")


embedding: Embedding = get_embedding()
# embedding: Embedding = DummyEmbedding()
