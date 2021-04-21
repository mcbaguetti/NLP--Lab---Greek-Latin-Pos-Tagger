import pyconll.util
from countpos import count_npos
from pathlib import Path


arrow = " -> "
eprob = {'SoS -> SoS': 1, 'EoS -> EoS': 1}


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


countpos = count_npos(corpus1)
calc_eprob(corpus)

print(countpos)
print(eprob)
