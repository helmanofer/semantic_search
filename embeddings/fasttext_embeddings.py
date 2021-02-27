import logging
import os
import shutil

import fasttext
import fasttext.util
from embeddings import Embeddings
from embeddings.embeddings import Sentences, Vectors
from utils.conf_util import get_project_root
from utils.common import list_all_files


class FastTextEmbeddings(Embeddings):
    def __init__(self):
        super().__init__(300)
        self.model_name = 'cc.en.300.bin'
        self.download()
        self.model = fasttext.load_model(self.model_name)

    def download(self):
        model_path = os.path.join(get_project_root(), 'models')
        if self.model_name in list_all_files(model_path, 'bin'):
            return
        fasttext.util.download_model('he', if_exists='ignore')  # English
        shutil.move(self.model_name, model_path)

    def infer(self, sentences: Sentences) -> Vectors:
        return self.model.get_sentence_vector(sentences)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    ft = FastTextEmbeddings()
