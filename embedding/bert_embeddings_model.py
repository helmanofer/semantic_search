from embedding.embbeding import Embedding, Sentences, Vectors
from typing import List, Union
from scipy.spatial.distance import cosine
from transformers import BertTokenizer, BertModel
import torch
import logging
from transformers import AutoTokenizer, AutoModel


logger = logging.getLogger(__name__)


class BertHebEmbeddingModel(Embedding):
    def __init__(self) -> None:
        super().__init__(768)
        self.model_name = 'TurkuNLP/wikibert-base-he-cased'
        self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
        self.model = BertModel.from_pretrained(self.model_name, 
                                               output_hidden_states=True)

    def tokenize(self, text: Union[str, List[str]]):
        tok_text = self.tokenizer.tokenize(text)
        logger.info(f"tokenized ids: {tok_text}")
        return tok_text

    def infer(self, sentences: Sentences) -> Vectors:
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


class LabseEmbeddingModel(Embedding):
    def __init__(self) -> None:
        super().__init__(768)
        self.tokenizer = AutoTokenizer.from_pretrained("pvl/labse_bert",
                                                       do_lower_case=False)
        self.model = AutoModel.from_pretrained("pvl/labse_bert")

    @staticmethod
    def mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return sum_embeddings / sum_mask

    def infer(self, sentences: Sentences) -> Vectors:
        encoded_input = self.tokenizer(sentences, padding="max_length", 
                                       truncation=True, max_length=128, 
                                       return_tensors='pt')
        input_ids = torch.tensor(encoded_input['input_ids'])
        attention_mask = torch.tensor(encoded_input['attention_mask'])

        with torch.no_grad():
            model_output = self.model(input_ids, attention_mask)

        return self.mean_pooling(model_output, attention_mask)


def test():
    bhem = BertHebEmbeddingModel()
    vecs = bhem.infer(["אני פורים שמח ומבדח", "הלא רק פעם בשנה אבוא להתארח", "יצחק רבין נרצח בכיכר מלכי ישראל"])
    print(1 - cosine(vecs[0], vecs[1]))
    print(1 - cosine(vecs[0], vecs[2]))


if __name__ == "__main__":
    test()
