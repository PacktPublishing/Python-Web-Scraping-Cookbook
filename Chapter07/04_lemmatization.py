from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize, regexp_tokenize, wordpunct_tokenize, blankline_tokenize

with open('sentence1.txt', 'r') as myfile:
    data = myfile.read().replace('\n', '')

sentences = sent_tokenize(data)

from nltk.stem import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer

pst = PorterStemmer()
lst = LancasterStemmer()
wnl = WordNetLemmatizer()

print("Stemming / lemmatization results")
for token in regexp_tokenize(sentences[0], pattern='\w+'):
    print(token, pst.stem(token), lst.stem(token), wnl.lemmatize(token))