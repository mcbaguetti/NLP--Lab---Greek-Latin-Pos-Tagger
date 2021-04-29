import pyconll.util
from pathlib import Path
import numpy as np
import prob
import accuracyViterbi


file_pathdev = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master/la_llct-ud-train.conllu")
file_pathdev1 = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master/la_llct-ud-dev.conllu")
corpus1 = pyconll.iter_from_file(file_pathdev1)
corpus = pyconll.iter_from_file(file_pathdev)
corpus2 = pyconll.iter_from_file(file_pathdev)
corpus3 = pyconll.iter_from_file(file_pathdev)

#sono i caratteri SoS + EoS
special_char = 2
save_prob = 0.00000000001
space = " "
arrow = " -> "
sos = "SoS"
eos = "EoS"
pos_array = prob.get_tags()
pos_len = pos_array.__len__()
eprob = prob.e_prob(corpus)
prob.t_prob(corpus2)
tprob = prob.t_prob_fin(corpus3)


#se non trova la probabilità ritorna la save_prob altrimenti ritorna quella corretta
def get_eprob(pos, token):
    name = pos + arrow + token
    if name not in eprob:
        return save_prob
    return eprob[name]


#se non trova la probabilità ritorna la save_prob altrimenti ritorna quella corretta
def get_tprob(tag, oldtag):
    name = oldtag + arrow + tag
    if name not in tprob:
        return save_prob
    return tprob[name]


#usa la matrice di viterbi per calcolare i pos
def viterbi(corpus):

    for sentence in corpus:

        s_length = sentence.__len__()
        mat = np.zeros(shape=(pos_len, s_length + special_char))
        token_arr = np.empty(shape=(s_length + special_char), dtype=np.dtype('U20'))
        count = 0
        token_arr[count] = sos
        backtrace = np.empty(shape=(s_length + special_char), dtype=np.dtype('U5'))
        backtrace[0] = sos
        max_col = 1
        #corrisponde a sos nel tagset, quindi è il valora iniziale
        index_max_col = 0


        #inizializzo l'array di token
        for token in sentence:
            count += 1
            token_arr[count] = token.form

        token_arr[count + 1] = eos

        for col in range(token_arr.__len__()):
            for row in range(pos_len):
                #per la prima colonna salva nella matrice tutte le probabilità di emissione (non calcolo quella di transizione perché nella prima colonna non c'è)
                if col == 0:
                    e_prob = get_eprob(pos_array[row], token_arr[col])
                    mat[row, col] = e_prob


                #per le successive colonne controllo le righe della colonna precedente e salvo la massima prob per ogni casella della colonna attuale
                else:
                    e_prob = get_eprob(pos_array[row], token_arr[col])
                    old_tag = pos_array[index_max_col]
                    t_prob = get_tprob(pos_array[row], old_tag)
                    temp_prob = max_col * float(e_prob) * float(t_prob)

                    if temp_prob > mat[row, col]:
                        mat[row, col] = temp_prob

            #calcolo il max della colonna e salvo il pos del max nel backtrace
            if col != 0:
                index_max_col = mat.argmax(axis=0)[col]
                backtrace[col] = pos_array[index_max_col]

        for i in range(backtrace.__len__()):
            print(token_arr[i] + space + backtrace[i])

        accuracyViterbi.save_num(backtrace, sentence)
    accuracyViterbi.print_accuracy()


viterbi(corpus1)