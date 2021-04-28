import pyconll.util
from pathlib import Path
import numpy as np
import read_files
import emissionProb
import transitionProb
import accuracyTest

file_pathdev = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master/la_llct-ud-train.conllu")
file_pathdev1 = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master/la_llct-ud-test.conllu")
corpus1 = pyconll.iter_from_file(file_pathdev1)
corpus = pyconll.iter_from_file(file_pathdev)
corpus2 = pyconll.iter_from_file(file_pathdev)

save_prob = 0.00000000001
arrow = " -> "
sos = "SoS"
eos = "EoS"
#sono i caratteri SoS + EoS
special_char = 2
space = " "
pos_array = read_files.get_tags()
pos_len = pos_array.__len__()
eprob = emissionProb.calc_eprob(corpus)
tprob = transitionProb.tprob2(corpus2)


def get_eprob(pos, token):
    name = pos + arrow + token
    if name not in eprob:
        return save_prob
    return eprob[name]

def get_tprob(tag, oldtag):
    name = oldtag + arrow + tag
    if name not in tprob:
        return save_prob
    return tprob[name]

def viterbi(corpus):

    for sentence in corpus:

        print(sentence.id)
        s_length = sentence.__len__()
        mat = np.zeros(shape=(pos_len, s_length + special_char))
        token_arr = np.empty(shape=(s_length + special_char), dtype=np.dtype('U15'))
        count = 0
        token_arr[count] = sos
        backtrace = np.empty(shape=(s_length + special_char), dtype=np.dtype('U15'))
        backtrace[0] = sos
        max_col = 1
        #corrisponde a sos nel tagset, quindi è il valora iniziale
        index_max_col = 15


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

        accuracyTest.save_num(backtrace, sentence)

    accuracyTest.print_accuracy()

viterbi(corpus1)