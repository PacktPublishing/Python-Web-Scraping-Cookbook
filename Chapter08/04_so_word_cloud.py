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
with_no_stops = [word for word in tokens if word.lower() not in stop_list]
two_grammed = tech_2grams(with_no_stops)
cleaned = remove_punctuation(two_grammed)
print(cleaned)

from wordcloud import WordCloud
from nltk.probability import FreqDist

freq_dist = FreqDist(cleaned)
wordcloud = WordCloud(width=1200, height=800).generate_from_frequencies(freq_dist)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

