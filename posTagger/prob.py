import pyconll
from pathlib import Path
import numpy as np

sos = 'SoS'
eos = 'EoS'
n_tag = 17

space = " "
equal = " = "
arrow = " -> "
slash = " / "
new_line = "\n"

countpos = {'SoS': 1, 'EoS': 1}
eprob = {'SoS -> SoS': 1, 'EoS -> EoS': 1}
tprob = {}
countname = {}
cprob = {}
frequent_tag_word = {}

file_path = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master/la_llct-ud-train.conllu")
corpus = pyconll.iter_from_file(file_path)


#salva i tag e conta le loro occorrenze
def count_npos(corpus):
    tot = 2
    for sentence in corpus:
        for token in sentence:
            add_to_hash(countpos, token.upos)
    return countpos


#calcola le emission probability e le ritorna tramite dizionario
def e_prob(corpus):

    #la prima parte della funzione calcola le occorrenze delle varie combinazioni tag -> parola
    for sentence in corpus:
        for token in sentence:
            name = token.upos + arrow + token.form
            add_to_hash(eprob, name)

    #divide i value di eprob per il corrispettivo value di countpos, caratterizzato dallo stesso tag
    for name in eprob:
        #salva in una str la prima parte della key di eprob cioè il tag
        key_pos = name.split(space, 1)[0]
        if key_pos in n_pos.keys():
            eprob[name] /= n_pos[key_pos]

    return eprob


#calcola le transmission probability e le ritorna tramite dizionario
def t_prob(corpus):
    #prima devo calcolare a parte la probabilità di SoS->tag, per fare questo inizio col calcolare il num di Sos->tag
    num_sos = 0
    for sentence in corpus:
        for token in sentence:
            if int(token.id) == 1:

                nameprob = sos + arrow + token.upos
                num_sos += 1
                add_to_hash(tprob, nameprob)

    #trovo l'effettiva probabilità di SoS->tag dividendo per count, ovvero il numero totale di SoS->tag
    for key in tprob:
        tprob[key]/= num_sos

def t_prob_fin(corpus):
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
        key_eos = name.split(arrow, 1)[1]
        key_sos = name.split(arrow, 1)[0]
        if key_eos == eos:
            tprob[name] /= num_eos

        elif key_sos != sos:
            tprob[name] /= n_pos[key_sos]

    return tprob


#conta le frequenze dei nomi e le ritorna sotto forma di dizionario
def count_name(corpus):
    for sentence in corpus:
        for token in sentence:
            name = token.form
            add_to_hash(countname, name)

    return countname


#conta i tag più frequenti per parola e le ritorna sotto forma di dizionario
def most_used_tag(corpus):
    # la prima parte della funzione calcola le occorrenze delle varie combinazioni parola / tag

    for sentence in corpus:
        for token in sentence:
            name = token.form + slash + token.upos
            add_to_hash(cprob, name)

    # divide i value di cprob per il corrispettivo value di countname, cioè con lo stesso name
    for name in cprob:
        # salva in una str la prima parte della key di cprob cioè il nome
        key_name = name.split(slash, 1)[0]
        if key_name in countname.keys():
            cprob[name] /= countname[key_name]

    copy_dict = cprob.copy()
    #trova la parola con il tag più frequente per una ciascuna parola
    for name in cprob:
        key_name = name.split(slash, 1)[0]
        key_pos = name.split(slash, 1)[1]
        for copy in copy_dict:
            key_copy_name = copy.split(slash, 1)[0]
            if key_copy_name == key_name and cprob[name] >= copy_dict[copy]:
                frequent_tag_word.update({key_name : key_pos})
    return frequent_tag_word


#ritorna un array di tutti i tags
def get_tags():
    pos_array = np.empty(shape=n_tag, dtype=np.dtype('U5'))
    count = 0

    for name in countpos:
        tag = name.split(new_line, 1)[0]
        pos_array[count] = tag
        count += 1

    return pos_array


#aggiunge una una chiave ad una hash oppure se esiste già incrementa il suo valore
def add_to_hash(hash, key):
    if key not in hash.keys():
        hash.update({key: 1})
    else:
        hash[key] += 1


n_pos = count_npos(corpus)