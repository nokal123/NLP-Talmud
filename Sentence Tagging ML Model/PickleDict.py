
import pickle

class PickleDict:
    diction = {}
    category = ""
    with open('word_list.txt') as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1].strip() #getting rid of \n and whitespaces
            if line.startswith('*'):
                line = line.replace('*', '')
                category = line
            elif line != "":
                diction[line] = category

    pickle.dump(diction, open("wordDict.p", "wb"))