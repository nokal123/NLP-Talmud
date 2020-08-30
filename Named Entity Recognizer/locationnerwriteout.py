from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import ngrams

text = '''וחכמים אומרים: כל העושה מלאכה בתשעה באב ואינו מתאבל על ירושלים אינו רואה בשמחתה, שנאמר "שמחו את ירושלים וגילו בה כל אהביה שישו אתה משוש כל המתאבלים עליה" מכאן אמרו: כל המתאבל על ירושלים זוכה ורואה בשמחתה, ושאינו מתאבל על ירושלים אינו רואה בשמחתה. תניא נמי הכי: כל האוכל בשר ושותה יין בתשעה באב — עליו הכתוב אומר "ותהי עונותם על עצמתם".
'''
print('Begin assemble corpus')
tagged_corpus = []
untagged_corpus = []

i = 0
for line in text.split('\n'):
    line = line.strip() # remove leading and terminating whitespace
    for sentence in sent_tokenize(line):

        sentence = word_tokenize(sentence)
        untagged_corpus.append(sentence)
        sentence = [[word, '_'] for word in sentence]
        tagged_corpus.append(sentence)
        i += 1
print(untagged_corpus[0])

def tagged_corpus_to_tsv_tagged_corpus(tagged_corpus: list):
    unique_id = 0 # for multi-token NER entries; really for any such entry
    dUniqueID = {}

    outputTaggedCorpus = []
    start_pos = 0
    for s, tagged_sentence in enumerate(tagged_corpus, 1):
        sentence = []

        for i, (word, tag) in enumerate(tagged_sentence, 1):
            end_pos = start_pos + len(word)
            if tag == '_':  # no identifier if no NamedEntity
                identifier = '_'
            elif tag.startswith('B-'):
                # is this a multi-token tag?
                if len(tagged_sentence) > i and tagged_sentence[i + 1][1].startswith('I-'):
                    unique_id += 1
                    identifier = '*[' + str(unique_id) + ']'
                    tag = tag[2:] + '[' + str(unique_id) + ']'
                else:
                    identifier = '*'
                    tag = tag[2:]
            elif tag.startswith('I-'):  # multi-token tag
                identifier = '*[' + str(unique_id) + ']'
                tag = tag[2:] + '[' + str(unique_id) + ']'
            else:  # should never get here
                identifier = '*'
                tag = tag[2:]

            # XPOS: fine grained POS tag in POS layer
            # UPOS: universal grained POS tag in POS layer
            # identifier: NER actual name
            # tag: NER tag

            xpos, upos = '_', '_'
            sentence.append([s, i, start_pos, end_pos, word,
                             xpos, upos, identifier, tag, '_', '_', '_'])
            start_pos = end_pos + 1  # because of space

        outputTaggedCorpus.append(sentence)
        start_pos = start_pos + 1  # because of newline

    return outputTaggedCorpus

def sublist_finder(a: list, b: list) -> int:

    for i, item in enumerate(ngrams(a, len(b))):

        if item == b:

            yield i
        yield -1


nametups=list()
f=open('allplaces.txt','r',encoding='utf-8')
for line in f:
    line=line.replace('LOC',"").strip()
    nametups.append(tuple(line.split()))
# for i in nametups:
#     print(i)

for i in range(len(untagged_corpus)):
    for tup in nametups:
        line=untagged_corpus[i]
        found = sublist_finder(line,tup)
        #print(found)
        for k in found:
            if k != (-1):
                sentence=tagged_corpus[i]
                sentence[k][1] = 'B-LOC'
                for j in range(1,len(tup)):
                    sentence[k+j][1]='I-LOC'

for line in tagged_corpus:
    print(line)

outputTaggedCorpus = tagged_corpus_to_tsv_tagged_corpus(tagged_corpus)
print(outputTaggedCorpus)
