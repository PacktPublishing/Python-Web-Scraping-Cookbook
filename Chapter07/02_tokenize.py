from nltk.tokenize import sent_tokenize

with open('sentence1.txt', 'r') as myfile:
    data = myfile.read().replace('\n', '')

sentences = sent_tokenize(data, language="german")

for s in sentences:
    print(s)

first_sentence = sentences[0]

print(first_sentence.split())

from nltk.tokenize import word_tokenize, regexp_tokenize, wordpunct_tokenize, blankline_tokenize

print(word_tokenize(first_sentence))

print(regexp_tokenize(first_sentence, pattern='\w+'))

print(wordpunct_tokenize(first_sentence))

print(blankline_tokenize(first_sentence))
