import nltk
from nltk.classify import apply_features
import random

#create dictionary of locations and people
location=dict()
people=dict()
NER=dict()
NER.update(location)
NER.update(people)
with open('allplaces.txt',encoding='utf-8') as f:
    content = f.readlines()
    for i in content:

        i=i.replace('LOC',"").strip()
        p={i:'LOC'}
        location.update(p)
#clean dictionary
with open('ner_stoplist.txt',encoding='utf-8')as f:
    content=f.readlines()
    for i in content:
        if '#' not in i:
            location.pop(i.strip())
with open("hebrewnames.txt",encoding="utf-8")as f:
    content=f.readlines()
    for i in content:
        i=i.replace('PER',"").strip()
        p={i:'PER'}
        people.update(p)


#to do: add dictionary of people names

def word2features(word,sent,i):
    features = {}
    #features based on Hebrew Named Entity Recognition Paper
    #structural features:
    features['word is first in sentence']=first(i)
    features['word is last in sentence']=last(i,sent)
    #lexicon features
    features['word'] = word
    features['word is in dictionary'] = foundindict(word)
        # prefixes and suffixes
    features['prefix'] = word[0]
    features['suffix'] = word[-1]
    features['prefixes'] = word[0:2]
    features['suffixes'] = word[len(word) - 2:]

    if i>0:

        features['word before'] = sent[i - 1]
        features['words before'] = foundindict(sent[i - 1])
        features['words around'] = foundindict((sent[i - 1] + word))

    if i>1:

        features['word more before'] = sent[i - 2]
        features['word more before'] = foundindict(sent[i - 2])

    if i<len(sent)-1:
        features['word after'] = sent[i + 1]
        features['words after'] = foundindict(sent[i + 1])
        features['words around'] = foundindict((word + sent[i + 1]))

    if i<len(sent)-2:
        features['word more after'] = sent[i + 2]
        features['word more after'] = str(foundindict(sent[i + 2]))
    return features


def first(i):
    if i==0:
        return True
    else:
        return False

def last(i,sent):
    if i==len(sent)-1:
        return True
    else:
        return False

def foundindict(word):
    if word in location:
        return 'LOC'
    if word in people:
        return 'PER'
    else:
        return False
featuresets=[]
namedents=[]
for key,value in location.items():
    sent=[]
    if len(key)>1:
        key=key.split()
    sent+=key
    namedents.append([sent,value])
for key,value in people.items():
    sent=[]
    if len(key)>1:
        key=key.split()
    sent+=key
    namedents.append([sent,value])
for sent, val in namedents:
    for i in range(len(sent)):
        featuresets.append([word2features(sent[i],sent,i),val])


random.shuffle(featuresets)
print(featuresets[:10])


train_set,test_set,devtest_set=featuresets[:1000],featuresets[1000:2000],featuresets[2000:4000]
classifier=nltk.NaiveBayesClassifier.train(train_set)
sent="בת שבע"
for i in range(len(sent.split())):

    print(classifier.classify(word2features(sent[i],sent,i)))
senta="משה"
print(classifier.classify(word2features(senta,[senta],0)))
print(nltk.classify.accuracy(classifier,devtest_set))

errors = []
for (name, tag) in namedents:
    for i in range(len(name)):
        guess = classifier.classify(word2features(name[i],name,i))
        if guess != tag:
            errors.append((tag, guess, name))
print(errors)
print((len(errors)*100)/len(namedents))