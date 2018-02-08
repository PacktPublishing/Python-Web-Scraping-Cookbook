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

short_word_len = 3
short_words = [word for word in freq_dist.keys() if len(word) <= short_word_len]
print('Distinct # of words of len <= %s: %s' % (short_word_len, len(short_words)))

unshort_words = [word for word in freq_dist.keys() if len(word) > short_word_len]
print('Distinct # of words > len %s: %s' % (short_word_len, len(unshort_words)))
