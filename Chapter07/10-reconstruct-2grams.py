from buildgrams import build_2grams
from punctuation import remove_punctuation
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

grams = {
    "c": {"#": ""},
    "sql": {"server": " "},
    "fast": {"paced": "-"},
    "highly": {"iterative": " "},
    "adapt": {"quickly": " "},
    "demonstrable": {"experience": " "},
    "full": {"stack": " "},
    "enterprise": {"software": " "},
    "bachelor": {"s": "'"},
    "computer": {"science": " "},
    "data": {"science":  " "},
    "current": {"trends": " "},
    "real": {"world": " "},
    "paid": {"relocation": " "},
    "web": {"server": " "},
    "relational": {"database": " "},
    "no": {"sql": " "}
}

with open('job-snippet.txt', 'r') as file:
    data = file.read()

tokens = word_tokenize(data)
stoplist = stopwords.words('english')
without_stops = [word for word in tokens if word not in stoplist]
result = remove_punctuation(build_2grams(without_stops, grams))
print(result)