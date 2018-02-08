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

# all words with one occurrence
dist = [item[0] for item in freq_dist.items() if item[1] <= 2]
print(len(dist))
not_rare = [word for word in without_stops if word not in dist]

freq_dist2 = FreqDist(not_rare)
print(len(freq_dist2))