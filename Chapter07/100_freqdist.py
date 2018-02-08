from nltk.probability import FreqDist
from os import path
from wordcloud import WordCloud

items = ["Computer Science", "foo", "bar"]

fd = FreqDist(items)
print(fd)
for i in fd.keys():
    print(i, fd[i])

freq_dist = {}
for key in fd.keys():
    freq_dist[key] = fd[i]

d = path.dirname(__file__)

# Read the whole text.
text = open(path.join(d, 'sentence1.txt')).read()

# Generate a word cloud image
wordcloud = WordCloud().generate_from_frequencies(freq_dist)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
