from typing import List, Union
from scipy.spatial.distance import cosine
from transformers import BertTokenizer, BertModel
import torch
import logging


logger = logging.getLogger(__name__)


class BertHebEmbeddingModel():
    def __init__(self) -> None:
        self.model_name = 'TurkuNLP/wikibert-base-he-cased'

        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        self.model = BertModel.from_pretrained(self.model_name, output_hidden_states=True)

    def tokenize(self, text: Union[str, List[str]]):
        tok_text = self.tokenizer.tokenize(text)
        logger.info(f"tokenized ids: {tok_text}")
        return tok_text

    def infer(self, text: List[str]):
        self.tokenize(text=text[0])
        tok_ids = self.tokenizer(text, max_length=64, padding="max_length")
        logger.info(f"tokenized ids: {tok_ids}")
        tokens_tensor = torch.tensor(tok_ids['input_ids'])
        segments_tensors = torch.tensor(tok_ids['attention_mask'])
        with torch.no_grad():
            # for input_ids, attention_mask in zip()
            outputs = self.model(tokens_tensor, segments_tensors)
            hidden_states = outputs[2]

        token_vecs = hidden_states[-2]
        sentence_embedding = torch.mean(token_vecs, dim=1)
        return sentence_embedding


def test():
    bhem = BertHebEmbeddingModel()
    vecs = bhem.infer(["אני פורים שמח ומבדח", "הלא רק פעם בשנה אבוא להתארח", "יצחק רבין נרצח בכיכר מלכי ישראל"])
    print(1 - cosine(vecs[0], vecs[1]))
    print(1 - cosine(vecs[0], vecs[2]))


if __name__ == "__main__":
    test()
