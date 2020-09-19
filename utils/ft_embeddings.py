import fasttext.util
import fasttext

fasttext.util.download_model('he', if_exists='ignore')
ft = fasttext.load_model('cc.he.300.bin')