import pyconll
from countpos import count_npos
from pathlib import Path


arrow = " -> "
cprob = {}
frequent_tag_word = {}


file_path = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master/la_llct-ud-train.conllu")
corpus = pyconll.iter_from_file(file_path)
corpus1 = pyconll.iter_from_file(file_path)


def most_used_tag(corpus):
    # la prima parte della funzione calcola le occorrenze delle varie combinazioni parola -> tag

    for sentence in corpus:
        for token in sentence:

            name = token.form + arrow + token.upos

            # se non c'è un name lo aggiunge nelle key di cprob e lo inizializza a 1, altrimenti aumenta di 1 il val del pos
            if name not in cprob.keys():
                cprob.update({name: 1})
            else:
                cprob[name] += 1

    # divide i value di cprob per il corrispettivo value di countpos, caratterizzato dallo stesso tag
    for name in cprob:
        # salva in una str la seconda parte della key di cprob cioè il tag
        key_pos = name.split(arrow, 1)[1]
        if key_pos in countpos.keys():
            cprob[name] /= countpos[key_pos]

    #trova la parola con il tag più frequente per una ciascuna parola
    for name in cprob:
        key_pos = name.split(arrow, 1)[0]
        if key_pos not in frequent_tag_word:
            frequent_tag_word.update({key_pos: cprob[name]})

        else:
            if cprob[name] > frequent_tag_word[key_pos]:
                frequent_tag_word.update({key_pos : cprob[name]})

    return frequent_tag_word

countpos = count_npos(corpus)
freq_tag = most_used_tag(corpus1)

print(countpos)
print(cprob)
print(frequent_tag_word)
