import pyconll
from countpos import count_npos

arrow = " -> "
tprob = {}
sos = 'SoS'
eos = 'EoS'
corpus = pyconll.iter_from_file('C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master')
corpus1 = pyconll.iter_from_file('C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master')
corpus2 = pyconll.iter_from_file('C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master')


def t_prob(corpus):
    #prima devo calcolare a parte la probabilità di SoS->tag, per fare questo inizio col calcolare il num di Sos->tag
    num_sos = 0
    for sentence in corpus:
        for token in sentence:
            if int(token.id) == 1:

                nameprob = sos + arrow + token.upos
                num_sos += 1

                if nameprob not in tprob.keys():
                    tprob.update({nameprob: 1})

                else:
                    tprob[nameprob] += 1

    #trovo l'effettiva probabilità di SoS->tag dividendo per count, ovvero il numero totale di SoS->tag
    for key in tprob:
        tprob[key]/= num_sos


def tprob2(corpus):
    num_eos = 0
    # calcolo tutte le altre probabilità di SoS->tag
    for sentence in corpus:
        length = sentence.__len__()
        for token in sentence:
            # se il token non è l'ultimo allora o lo salva se è nuovo o incrementa il tag -> tag
            if length > 1:
                next_token = sentence.__getitem__(int(token.id))
                nameprob = token.upos + arrow + next_token.upos
                add_to_hash(tprob, nameprob)

            else:
                num_eos += 1
                nameprob = token.upos + arrow + eos
                add_to_hash(tprob, nameprob)

            length -= 1

    #calcola tutte le altre probabilità di trasmissione tranne sos->tag
    for name in tprob:
        # salva in una str la seconda parte della key di tprob cioè il tag dopo la freccia
        key_eos = name.split("-> ", 1)[1]
        key_sos = name.split(" ->", 1)[0]
        if key_eos == eos:
            tprob[name] /= num_eos

        elif key_sos != sos:
            tprob[name] /= n_pos[key_sos]

    #calcola la vera probabilità dividendo per il numero di casi totali


#aggiunge una una chiave ad una hash oppure se esiste già incrementa il suo valore
def add_to_hash(hash, key):
    if key not in hash.keys():
        hash.update({key: 1})

    else:
        hash[key] += 1

n_pos = count_npos(corpus2)
t_prob(corpus)
tprob2(corpus1)
print(tprob)