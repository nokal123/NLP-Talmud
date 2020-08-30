from pymongo import MongoClient
import re
import csv


client = MongoClient()
db=client.sefaria
collection=db.lexicon_entry

#collect female names from Jastrow and BDB
femalenamesregx=({
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

#collect male names from Jastrow and BDB
malenamesregx = ({
    '$or': [
        {
            '$and': [
                {
                    'parent_lexicon': 'Jastrow Dictionary'
                }, {'$or': [{
                    'content.senses.definition': re.compile("pr\\. n\. m\.")},
                    {'content.morphology': re.compile("pr\. n\. m\.")},
                    {'$and': [{'content.morphology': re.compile("pr\. n\.")},
                              {'$or': [{'content.senses.definition': re.compile("angel", re.IGNORECASE)},
                                       {'content.senses.definition': re.compile("divinity", re.IGNORECASE)},
                                       {'content.senses.definition': re.compile("family", re.IGNORECASE)},
                                       {'content.senses.definition': re.compile("demon", re.IGNORECASE)},
                                       {'content.senses.definition': re.compile("sorcerer", re.IGNORECASE)},
                                       {'content.senses.definition': re.compile("son", re.IGNORECASE)},
                                       {'content.senses.definition': re.compile("deity", re.IGNORECASE)},
                                       {'content.senses.definition': re.compile("patriarch", re.IGNORECASE)},
                                       {'content.senses.definition': re.compile("tribe", re.IGNORECASE)},
                                       {'content.senses.definition': re.compile("surname", re.IGNORECASE)},
                                       {'content.senses.definition': re.compile("spirit", re.IGNORECASE)}]}]}
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

#creates hebrew names gazetteer
#to do: needs rabbis names from xls file
with open('hebrewnames.txt','w',newline='',encoding='utf-8')as f:
    reg = r'[^א-ת," "]'
    femalenames=list(collection.find(femalenamesregx))
    for i in femalenames:
        word = re.sub(reg, "", i.get('headword'), re.A)
        f.write(word+ "\t"+"PER"+"\n")
    malenames=list(collection.find(malenamesregx))
    for i in malenames:
        word=re.sub(reg, "", i.get('headword'), re.A)
        f.write(word+"\t"+"PER"+"\n")

#creates english name gazetteer
with open('englishnames.csv', 'w', newline='',encoding='utf-8') as f:
    fieldnames=['englishname','hebrewname','morphology','definition','transliteration','dictionary']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    femalenames=list(collection.find(femalenamesregx))
    for i in femalenames:
        entry=dict()

        entry['dictionary']=i.get('parent_lexicon')
        entry['hebrewname']=i.get('headword')
        entry['morphology']='pr. n. f.'
        entry['definition']=i.get('content').get('senses')
        #get names for BDB
        if i.get('parent_lexicon')=='BDB Augmented Strong':
            #print(i)
            entry['transliteration']=i.get('pronunciation')
            content=i.get('content')
            if len(content.get('senses'))>0:
                definition=content.get('senses')[0]
                name=definition.get('definition').split()[0]
                entry['englishname']=name

        if i.get('parent_lexicon')=='Jastrow Dictionary':
            #get names from Jastrow
            #print(i)
            if i.get('content').get('morphology')=='pr. n. f.':

                for j in i.get('content').get('senses'):
                    for k in re.findall(re.compile("(?<=<i>).*?(?=</i>)"),j.get('definition')):
                        entry['englishname']=k
            else:
                for j in i.get('content').get('senses'):
                    for k in re.findall(re.compile("(?<=pr\. n\. f\. <i>).*?(?=</i>)"),j.get('definition')):
                        entry['englishname']=k
        writer.writerow(entry)


    malenames=list(collection.find(malenamesregx))
    for i in malenames:
        entry=dict()
        entry['dictionary'] = i.get('parent_lexicon')
        entry['hebrewname'] = i.get('headword')
        entry['morphology'] = 'pr. n. m.'
        entry['definition'] = i.get('content').get('senses')

        if i.get('parent_lexicon')=='BDB Augmented Strong':
            content=i.get('content')
            entry['transliteration'] = i.get('pronunciation')
            if len(content.get('senses'))>0:
                definition=content.get('senses')[0]
                name=definition.get('definition').split()[0]
                entry['englishname']=name
        if i.get('parent_lexicon')=='Jastrow Dictionary':
            #get names from Jastrow
            if i.get('content').get('morphology')=='pr. n. m.':
                for j in i.get('content').get('senses'):
                    if len(j)>0:
                        for k in re.findall(re.compile("(?<=<i>).*?(?=</i>)"),j.get('definition')):
                            entry['englishname']=k
            else:
                for j in i.get('content').get('senses'):
                    if len(j)>0:
                        for k in re.findall(re.compile("(?<=pr\. n\. m\. <i>).*?(?=</i>)"), j.get('definition')):
                            entry['englishname'] = k
        writer.writerow(entry)
f.close()


