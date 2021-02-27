# https://towardsdatascience.com/fine-tuning-a-bert-model-for-search-applications-33a7a442b9d0


from transformers import BertTokenizerFast

model_name = "google/bert_uncased_L-4_H-512_A-8"
tokenizer = BertTokenizerFast.from_pretrained(model_name)

train_encodings = tokenizer(
    train_queries, train_docs, truncation=True, 
    padding='max_length', max_length=128
)

val_encodings = tokenizer(
    val_queries, val_docs, truncation=True, 
    padding='max_length', max_length=128
)