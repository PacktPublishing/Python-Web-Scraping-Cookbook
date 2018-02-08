from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

with open('job-snippet.txt', 'r') as file:
    data = file.read()

tokens = [word.lower() for word in word_tokenize(data)]
stoplist = stopwords.words('english')
without_stops = [word for word in tokens if word not in stoplist]
print(without_stops)