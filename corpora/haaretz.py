import requests

r = requests.get("https://yeda.cs.technion.ac.il:8443/corpus/software/corpora/haaretz/txt/haaretz_txt.tar.gz", allow_redirects=True)
with open("haaretz_txt.tar.gz", "wb") as f:
    f.write(r.content)