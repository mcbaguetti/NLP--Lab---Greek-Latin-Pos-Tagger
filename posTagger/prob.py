import pyconll
from pathlib import Path

sos = 'SoS'
eos = 'EoS'

space = " "
equal = " = "
arrow = " -> "
slash = " / "

countpos = {'SoS':1, 'EoS':1}
eprob = {'SoS -> SoS': 1, 'EoS -> EoS': 1}
tprob = {}
countname = {}
cprob = {}
frequent_tag_word = {}

file_path = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master/la_llct-ud-train.conllu")
corpus = pyconll.iter_from_file(file_path)
corpus1 = pyconll.iter_from_file(file_path)
corpus2 = pyconll.iter_from_file(file_path)


#salva i tag e conta le loro occorrenze
def count_npos(corpus):
    tot = 2
    for sentence in corpus:
        for token in sentence:
            tot+=1
            #se non c'è un tag lo aggiunge nelle key di countpos e lo inizializza a 1, altrimenti aumenta di 1 il val del pos
            if token.upos not in countpos.keys():
                countpos.update({token.upos : 1})
            else:
                countpos[token.upos] += 1

    countpos.update({"tot_pos": tot})

    return countpos


#calcola le emission probability e le ritorna tramite dizionario
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

                if nameprob not in tprob.keys():
                    tprob.update({nameprob: 1})

                else:
                    tprob[nameprob] += 1

    #trovo l'effettiva probabilità di SoS->tag dividendo per count, ovvero il numero totale di SoS->tag
    for key in tprob:
        tprob[key]/= num_sos

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

    return tprob


#conta le frequenze dei nomi e le ritorna sotto forma di dizionario
def count_name(corpus):
    for sentence in corpus:
        for token in sentence:
            name = token.form
            #se non c'è un name lo aggiunge nelle key di countname e lo inizializza a 1, altrimenti aumenta di 1 il val del pos
            if name not in countname.keys():
                countname.update({name : 1})
            else:
                countname[name] += 1

    return countname


#conta i tag più frequenti per parola e le ritorna sotto forma di dizionario
def most_used_tag(corpus):
    # la prima parte della funzione calcola le occorrenze delle varie combinazioni parola / tag

    for sentence in corpus:
        for token in sentence:

            name = token.form + slash + token.upos

            # se non c'è un name lo aggiunge nelle key di cprob e lo inizializza a 1, altrimenti aumenta di 1 il val del pos
            if name not in cprob.keys():
                cprob.update({name: 1})
            else:
                cprob[name] += 1

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

#aggiunge una una chiave ad una hash oppure se esiste già incrementa il suo valore
def add_to_hash(hash, key):
    if key not in hash.keys():
        hash.update({key: 1})

    else:
        hash[key] += 1


n_pos = count_npos(corpus2)
calc_eprob(corpus1)
t_prob(corpus)
