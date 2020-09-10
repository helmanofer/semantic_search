mapping = {
    "settings": {
        "index": {
            "knn": True,
            "knn.space_type": "cosinesimil"
        },
        "analysis": {
            "analyzer": {
                "analyzer_shingle": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "filter_shingle"
                    ]
                }
            },
            "filter": {
                "filter_shingle": {
                    "type": "shingle",
                    "max_shingle_size": 3,
                    "min_shingle_size": 2,
                    "output_unigrams": False
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "text": {
                "type": "text",
                "copy_to": "phrases",
            },
            "phrases": {
                "search_analyzer": "analyzer_shingle",
                "analyzer": "analyzer_shingle",
                "type": "text",
                "store": True,
                "fielddata": True,
            },
            "paragraphs": {
                "type": "nested",
                "properties": {
                    "par_vector": {
                        "type": "knn_vector",
                        "dimension": 300
                    }
                }
            }
        }
    }

}
