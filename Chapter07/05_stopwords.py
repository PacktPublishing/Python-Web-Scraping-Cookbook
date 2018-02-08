from nltk.tokenize import sent_tokenize
from nltk.tokenize import regexp_tokenize
from nltk.corpus import stopwords

with open('sentence1.txt', 'r') as myfile:
    data = myfile.read().replace('\n', '')

sentences = sent_tokenize(data)
first_sentence = sentences[0]

print("Original sentence:")
print(first_sentence)

tokenized = regexp_tokenize(first_sentence, '\w+')
print("Tokenized:", tokenized)

stoplist = stopwords.words('english')
cleaned = [word for word in tokenized if word not in stoplist]
print("Cleaned:", cleaned)