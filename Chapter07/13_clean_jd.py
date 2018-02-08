from bs4 import BeautifulSoup
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from tech2grams import tech_2grams
from punctuation import remove_punctuation

with open("spacex-job-listing.html", "r") as file:
    content = file.read()

bs = BeautifulSoup(content, "lxml")
script_tag = bs.find("script", {"type": "application/ld+json"})

job_listing_contents = json.loads(script_tag.contents[0])
print(job_listing_contents)

desc_bs = BeautifulSoup(job_listing_contents["description"], "lxml")
print(desc_bs)

just_text = desc_bs.find_all(text=True)
print(just_text)

joined = ' '.join(just_text)
tokens = word_tokenize(joined)

stop_list = stopwords.words('english')
print(stop_list)
with_no_stops = [word for word in tokens if word.lower() not in stop_list]
two_grammed = tech_2grams(with_no_stops)
cleaned = remove_punctuation(two_grammed)
print(cleaned)

"""
print(description_text)
"""
"""
#print(aj.contents)
#print(desc_bs.string)

joined = ' '.join(all_text)
#print(joined)

tokens_word = word_tokenize(joined)
"""
"""
token_pairs = [
    ('c', '#'),
    ('C', '#'),
    ('SQL', 'Server', ' '),
    ('Full', 'Stack', ' '),
    ('Enterprise', 'Software', ' '),
    ('Bachelor', 's'),
    ('Computer', 'science'),
    ('Data', 'Science', ' '),
    ('current', 'trends', ' '),
    ('real', 'world', ' '),
    ('Paid', 'relocation'),
    ('Web', 'server',' '),
    ('relational', 'database', ' ')
]

tokens_patched = patch_tokens(tokens_word, token_pairs)
tokens_cleaned = clean_tokens(tokens_patched, [':', ',', '.', "``", "''", '(', ')', '-', '!'])

stoplist = stopwords.words('english')
print(stoplist)
stopped = [word for word in tokens_cleaned if word.lower() not in stoplist]
print(stopped)
"""





