import pyconll.util
from pathlib import Path

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

countpos = {'SoS':1, 'EoS':1}

