from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize, regexp_tokenize, wordpunct_tokenize, blankline_tokenize
with open('sentence1.txt', 'r') as myfile:
    data = myfile.read().replace('\n', '')

sentences = sent_tokenize(data, language="german")

for s in sentences:
    print(s)

from nltk.stem import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer

pst = PorterStemmer()
lst = LancasterStemmer()

print("Stemming results")
for token in regexp_tokenize(sentences[0], pattern='\w+'):
    print(token, pst.stem(token), lst.stem(token))