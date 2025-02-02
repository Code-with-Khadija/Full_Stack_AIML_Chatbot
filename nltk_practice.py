from nltk.corpus import wordnet 

def get_definition(word):
    try:
        print("Hi")
        synset= wordnet.synsets(word)
        print(synset)
        sn_len = len(synset)
        description = ""
        for i in range(sn_len):
            description += synset[i].definition()

        # return description
        return description
    except Exception as e:
        return e


def get_definition1(word):
    try:
        description= ' '
        print("Hi")
        synset = wordnet.synsets(word)
        print(synset)
        sn_len = len(synset)
        print(sn_len)
        for i in range(sn_len):
            description += synset[i].definition()

        # return description
        return description
    except Exception as e:
        return e


def get_description(word):
    description = ' '
    sn = wordnet.synsets(word)
    print('sn: ', sn)
    length = len(sn)
    for i in range(length):
        # description += str(i+1)
        description += sn[i].definition()
        if i + 1 != length:
            description += '\n'
    print('description: ', description)
    return description





