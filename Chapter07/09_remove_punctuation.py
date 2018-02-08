from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

content = "Strong programming experience in C#, ASP.NET/MVC, JavaScript/jQuery and SQL Server"
tokenized = word_tokenize(content)
stop_list = stopwords.words('english')
cleaned = [word for word in tokenized if word not in stop_list]
print(cleaned)

punctuation_marks = [':', ',', '.', "``", "''", '(', ')', '-', '!', '#']
tokens_cleaned = [word for word in cleaned if word not in punctuation_marks]
print(tokens_cleaned)