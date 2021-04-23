import pyconll.util
from countpos import count_npos
from pathlib import Path
import _pickle as pickle


arrow = " -> "
eprob = {'SoS -> SoS': 1, 'EoS -> EoS': 1}

latin_file_path = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/probabilities/latin/emission-prob.txt")
file_path = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master/la_llct-ud-train.conllu")
corpus = pyconll.iter_from_file(file_path)
corpus1 = pyconll.iter_from_file(file_path)


def calc_eprob(corpus):

    #la prima parte della funzione calcola le occorrenze delle varie combinazioni tag -> parola

    for sentence in corpus:
        for token in sentence:

            name = token.upos + arrow + token.form

            #se non c'è un name lo aggiunge nelle key di eprob e lo inizializza a 1, altrimenti aumenta di 1 il val del pos
            if name not in eprob.keys():
                eprob.update({name : 1})
            else:
                eprob[name] += 1

    #divide i value di eprob per il corrispettivo value di countpos, caratterizzato dallo stesso tag
    for name in eprob:
        #salva in una str la prima parte della key di eprob cioè il tag
        key_pos = name.split(" ", 1)[0]
        if key_pos in countpos.keys():
            eprob[name] /= countpos[key_pos]

    #scrive nel file il dizionario eprob
    with open(latin_file_path, 'w') as file:
        for key in sorted(eprob.keys()):
            file.write("'%s'='%s', \n" % (key, eprob[key]))



countpos = count_npos(corpus1)
calc_eprob(corpus)


print(countpos)
print(eprob)
