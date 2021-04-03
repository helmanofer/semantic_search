import json

from utils.model import IndexedDoc, IndexedChunk


class IndexedDocJsonWithEmbedding(IndexedDoc):
    def __init__(self, data: str, *args, **kwargs) -> None:
        super().__init__(data)
        jdata = json.loads(data)
        self.id = jdata["id"]
        self.text = jdata["text"]
        for chunk_json in jdata['chunks']:
            chunk = IndexedChunk()
            chunk.id = chunk_json["id"]
            chunk.parent_id = self.id
            chunk.text = chunk_json["text"]
            chunk.vector = chunk_json["vector"]
            self.chunks.append(chunk)


if __name__ == "__main__":
    pass