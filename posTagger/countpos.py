import pyconll.util
from pathlib import Path

space = " "
equal = " = "
countpos = {'SoS':1, 'EoS':1}

latin_most_used = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/probabilities/latin/most-used-tags.txt")
tags_fp = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/probabilities/latin/tags.txt")
file_path = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master/la_llct-ud-train.conllu")
corpus1 = pyconll.iter_from_file(file_path)

def count_npos(corpus1):
    tot = 2
    for sentence in corpus1:
        for token in sentence:
            tot+=1
            #se non c'è un tag lo aggiunge nelle key di countpos e lo inizializza a 1, altrimenti aumenta di 1 il val del pos
            if token.upos not in countpos.keys():
                countpos.update({token.upos : 1})
            else:
                countpos[token.upos] += 1

    countpos.update({"tot_pos": tot})

    return countpos

def save_tags():

    with open(latin_most_used, 'r') as fileread:
        for line in fileread:
            pos = line.split(equal, 1)[1]
            pos = pos.split(space, 1)[0]

            # scrive nel file i pos
            with open(tags_fp, 'r+') as filewrite:
                content = filewrite.read()
                if pos not in content:
                    filewrite.write("%s\n" % pos)

save_tags()