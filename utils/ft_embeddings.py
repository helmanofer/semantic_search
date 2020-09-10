import fasttext.util
import fastText

fasttext.util.download_model('he', if_exists='ignore')
ft = fasttext.load_model('cc.he.300.bin')