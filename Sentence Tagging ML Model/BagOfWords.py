import os
import pickle
from nltk import wordpunct_tokenize, re, bigrams, trigrams, FreqDist
import string

# Creates bag of words, bigrams, and trigrams for MLTaggingAlgo.py

punctuations = '''!()[]—{};:'"\,<>./?@#$%^&*_~'''
directory = '../../PunctuatedText'
unSO= []
bi = []
tri = []
counter = 0
for entry in os.scandir(directory):
    if entry.path.endswith(".txt"):
        file = open(entry.path, mode='r', encoding='utf8')
        file_txt = file.read()
        words = [word for word in re.sub('['+string.punctuation+']', '', file_txt).split()
                 if word != '—']

        uni.extend(words)
        bi.extend(bigrams(words))
        tri.extend(trigrams(words))

uni = FreqDist(uni).most_common(2000)
uni = [word for word, freq in uni]
bi = FreqDist(bi).most_common(2000)
bi = [b for b, freq in bi]
tri = FreqDist(tri).most_common(2000)
tri = [t for t, freq in tri]
bag_of_words = [uni, bi, tri]
pickle.dump(bag_of_words, open("bag_of_words.p", "wb"))
print('unigrams', len(uni), uni)
print('bigrams', len(bi), bi)
print('trigrams', len(tri), tri)


