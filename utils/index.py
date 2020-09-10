import os
import xml.etree.ElementTree as ET
from lsh.random_projection import LshGaussianRandomProjection
import numpy

import json

# import tarfile
# tar = tarfile.open("/mnt/c/SourceCode/sematic_search/tapuz_xml2.tar.gz")
# tar.extractall()
# tar.close()
from utils.common import get_project_root
import fasttext


def read_tapuz_data():
    print("loading fasttext")
    ft = fasttext.load_model("cc.he.300.bin")
    print("done loading fasttext")
    directory = "/mnt/c/SourceCode/sematic_search/xml"
    directory = os.path.join(get_project_root(), "xml")
    _id = 0
    with open("tapuz.jsonl", "w", encoding="utf-8") as fw:
        for fname in os.listdir(directory):
            tree = ET.parse(os.path.join(directory, fname))
            root = tree.getroot()
            for paragraph in root.iter("paragraph"):
                par = []
                text = []
                for sentence in paragraph.iter("sentence"):
                    sent = []
                    for token in sentence.iter("token"):
                        sent.append(token.attrib["surface"])
                    par.append(sent)
                    text.append(" ".join(sent))
                fw.write(json.dumps(par, ensure_ascii=False) + os.linesep)
                data = {
                    "_id": _id,
                    "text": "\n".join(text),
                    "paragraphs": [
                        {
                            "par_text": " ".join(p),
                            "par_tokens": p,
                            "par_vector": ft.get_sentence_vector(" ".join(p)),
                        }
                        for p in par
                    ],
                }
                yield data
                _id += 1


def read_tapuz_data_with_vec():
    lsh_g = LshGaussianRandomProjection(
        vector_dimension=300, bucket_size=4, num_of_buckets=40, seed=4
    )
    lsh_g.fit()
    with open("tapuz_with_vectors.jsonl") as rf:
        for line in rf:
            j = json.loads(line)
            for d in j["paragraphs"]:
                vec = d.pop("par_vector")
                d["lsh"] = " ".join(lsh_g.indexable_transform(numpy.array(vec)))
            yield j
