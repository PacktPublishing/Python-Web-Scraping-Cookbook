from nltk.tokenize import sent_tokenize

with open('sentence1.txt', 'r') as myfile:
    data=myfile.read().replace('\n', '')

sentences = sent_tokenize(data, language="german")

for s in sentences:
    print(s)
