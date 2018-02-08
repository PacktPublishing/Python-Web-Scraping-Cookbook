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
for key in freq_dist.keys():
    print(key, freq_dist[key])

print(freq_dist.most_common(10))
print(freq_dist.most_common()[-10:])

dist_1 = [item[0] for item in freq_dist.items() if item[1] == 1]
print(len(dist_1), dist_1)