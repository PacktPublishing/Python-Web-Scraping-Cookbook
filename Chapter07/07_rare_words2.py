from nltk.probability import FreqDist
from nltk.tokenize import regexp_tokenize
from nltk.corpus import stopwords

with open('wotw.txt', 'r') as file:
    data = file.read()

tokens = [word.lower() for word in regexp_tokenize(data, '\w+')]
stoplist = stopwords.words('english')
without_stops = [word for word in tokens if word not in stoplist]

freq_dist = FreqDist(without_stops)

print('Number of words: %s' % len(freq_dist))

two_thirds = int(len(freq_dist) * 2 / 3)
print(freq_dist.most_common()[-two_thirds:])
