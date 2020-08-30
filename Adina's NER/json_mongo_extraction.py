from pymongo import MongoClient
import re

client = MongoClient()
db=client.sefaria
collection=db.lexicon_entry

#filter for place names in Jastrow Dictionary
Jastrow_places_search=({
    '$and': [
        {
            'parent_lexicon': re.compile("Jastrow Dictionary")
        }, {
            '$or': [
                {
                    'content.morphology': re.compile("pr\. n\. pl\.")
                },{
                    'content.senses.definition':re.compile('pr\. n\. pl\.')
                }, {
                    'content.senses.definition': re.compile("Berl\\. Beitr\.")
                }, {
                    'content.senses.definition': re.compile("Hildesh\\. Beitr\.")
                }, {
                    'content.senses.definition': re.compile("Neub\\.")
                },
                {'$and':[ #proper noun could be people or place names, filters using terms used in the definition
                    { 'content.morphology': re.compile("pr\. n\.")},
                    {'$or':[{'content.senses.definition': re.compile("town",re.IGNORECASE)},
                     {'content.senses.definition': re.compile("country",re.IGNORECASE)},
                            {'content.senses.definition':re.compile('district',re.IGNORECASE)},
                            {'content.senses.definition':re.compile("province",re.IGNORECASE)},
                            {'content.senses.definition':re.compile("city",re.IGNORECASE)},
                            {'content.senses.definition':re.compile("canal",re.IGNORECASE)},
                            {'content.senses.definition':re.compile("river",re.IGNORECASE)},
                            {'content.senses.definition':re.compile("tributary",re.IGNORECASE)},
                            {'content.senses.definition':re.compile("street",re.IGNORECASE)},
                            {'content.senses.definition':re.compile("brook",re.IGNORECASE)},
                            {'content.senses.definition':re.compile("valley",re.IGNORECASE)},
                            {'content.senses.definition':re.compile("border",re.IGNORECASE)},
                            {'content.senses.definition':re.compile("mount",re.IGNORECASE)},
                            {'content.senses.definition':re.compile("mountain",re.IGNORECASE)},
                            {'content.senses.definition':re.compile("kingdom",re.IGNORECASE)},
                            {'content.senses.definition':re.compile("land",re.IGNORECASE)},
                            {'content.senses.definition':re.compile("cave",re.IGNORECASE)},
                            {'content.senses.definition':re.compile("lake",re.IGNORECASE)},
                            {'content.senses.definition':re.compile("pond",re.IGNORECASE)},
                            {'content.senses.definition':re.compile("gate",re.IGNORECASE)},
                            {'content.senses.definition':re.compile("tower",re.IGNORECASE)},
                            {'content.senses.definition':re.compile("building",re.IGNORECASE)},
                            {'content.senses.definition':re.compile("peninsula",re.IGNORECASE)},
                            {'content.senses.definition':re.compile("settlement",re.IGNORECASE)}
                            ]}
                    ]
                                                                          }
            ]
        }
    ]
})

BDB_places_search = ({
    '$and': [
        {
            'parent_lexicon': re.compile(r"BDB")
        }, {
            'content.morphology': 'n-pr-loc'
        }
    ]
})
jastrow_places= list(collection.find(Jastrow_places_search))
bdb_places=list(collection.find(BDB_places_search))

reg = r'[^א-ת|" "|"׳"]'
rReg = re.compile(reg)
location=set()
for i, item in enumerate(jastrow_places):
    if 'headword' in item:
        headword = item['headword'].strip()
        if headword == 'שְׁמָע':
            x = 2
        #
        location.add(('jastrow', headword, headword))
    if 'alt_headwords' in item:
        for alt_headword in item['alt_headwords']:
            alt_headword = re.sub(rReg, "", alt_headword).strip()
            num_words = len(alt_headword.split())
            # case 1, example is בית פ׳ so that the second word is really the headword
            if alt_headword[-1:]=="׳" and num_words == 2:
                alt_headword = alt_headword[:-2] + headword

            # case #2, example is ח׳ in place of עפריים, so switch out the ח
            elif "׳" in alt_headword and num_words == 1:
                print(alt_headword)
                for k in range(len(alt_headword)):
                    # find place of maximum prefix; i think this code is wrong, but should discuss
                    if alt_headword[:k] != headword[:k]:
                        alt_headword = alt_headword[:k] + headword[k-1:]
                        break

            # case 3, two words, with the second character of first word being the quote
            # example ע' ענתות, instead of just עניה
            elif num_words == 2 and alt_headword[1] == "׳":
                alt_headword = alt_headword[2:] + headword

            # case 4, entire replacement of word
            elif "׳" not in alt_headword:
                # alt_headword = alt_headword
                pass

            if alt_headword == 'שמע' or headword == 'שמע':
                x = 1
            # finally, add the pair of alt_headword, headword
            location.add(('jastrow', alt_headword, headword))

for i in range(len(bdb_places)):
    value = bdb_places[i]['headword']
    if value == 'שְׁמָע':
        x = 3
    location.add(('bdb', value, value))

print(location)

f=open("allplaces.csv", "w", encoding="utf8", newline='')
import csv
csv_writer = csv.writer(f, delimiter='\t')
csv_writer.writerow('source,word,headword,type'.split())
location2=set()

# filter out nekudot
for source, word, headword in location:
    word = re.sub(rReg, "", word).strip()
    location2.add((source, word, headword))
print(location2)
for source, word, headword in sorted(location2):
    csv_writer.writerow([source, word, headword, 'LOC'])
f.close()



#filter for female names in Jastrow and BDB
'''femalenamesregx=({
    '$or': [
        {
            '$and': [
                {
                    'parent_lexicon': re.compile("Jastrow Dictionary")
                },
                    {'$or':[{'content.senses.definition': re.compile("pr\\. n\. f\.")},
                            {'content.morphology':re.compile("pr\. n\. f\.")},
                            {'$and':[{'content.morphology':("pr\. n\.")},
                             {'content.senses.definition':re.compile("woman",re.IGNORECASE)}]}]}

            ]
        }, {
            '$and': [
                {
                    'parent_lexicon': 'BDB Augmented Strong'
                }, {
                    'content.morphology': re.compile("n-pr-f")
                }
            ]
        }
    ]
})

femalenames=list(collection.find(femalenamesregx))


#filter for male names in Jastrow and BDB
malenamesregx=({
    '$or': [
        {
            '$and': [
                {
                    'parent_lexicon': 'Jastrow Dictionary'
                }, {'$or':[{
                    'content.senses.definition': re.compile("pr\\. n\. m\.")},
                    {'content.morphology':re.compile("pr\. n\. m\.")},
                        {'$and':[{'content.morphology':re.compile("pr\. n\.")},
                             {'$or':[{'content.senses.definition':re.compile("angel",re.IGNORECASE)},
                                     {'content.senses.definition':re.compile("divinity",re.IGNORECASE)},
                                     {'content.senses.definition':re.compile("family",re.IGNORECASE)},
                                     {'content.senses.definition':re.compile("demon",re.IGNORECASE)},
                                     {'content.senses.definition':re.compile("sorcerer",re.IGNORECASE)},
                                     {'content.senses.definition':re.compile("son",re.IGNORECASE)},
                                     {'content.senses.definition':re.compile("deity",re.IGNORECASE)},
                                     {'content.senses.definition':re.compile("patriarch",re.IGNORECASE)},
                                     {'content.senses.definition':re.compile("tribe",re.IGNORECASE)},
                                     {'content.senses.definition':re.compile("surname",re.IGNORECASE)},
                                     {'content.senses.definition':re.compile("spirit",re.IGNORECASE)}]}]}
                ]
                }
            ]
        }, {
            '$and': [
                {
                    'parent_lexicon': 'BDB Augmented Strong'
                }, {
                    'content.morphology': re.compile("n-pr-m")
                }
            ]
        }
    ]
})


malenames=list(collection.find(malenamesregx))'''

