import pyconll.util
from pathlib import Path
import numpy as np
import read_files

file_pathdev = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master/la_llct-ud-dev.conllu")
corpus1 = pyconll.iter_from_file(file_pathdev)


sos = "SoS"
eos = "EoS"
#sono i caratteri SoS + EoS
special_char = 2
space = " "

def viterbi(corpus):

    pos_array = read_files.get_tags()
    pos_len = pos_array.__len__()

    for sentence in corpus:

        s_length = sentence.__len__()
        mat = np.zeros(shape=(pos_len, s_length + special_char))
        token_arr = np.empty(shape=(s_length + special_char), dtype=np.dtype('U15'))
        count = 0
        token_arr[count] = sos
        backtrace = np.empty(shape=(s_length + special_char), dtype=np.dtype('U15'))
        backtrace[0] = sos
<<<<<<< HEAD
        max_col = 1
        #corrisponde a sos nel tagset, quindi è il valora iniziale
        index_max_col = 16
=======
>>>>>>> parent of a9306c1 (Update viterbi.py)

        #inizializzo l'array di token
        for token in sentence:
            count += 1
            token_arr[count] = token.form

        token_arr[count + 1] = eos

        for col in range(token_arr.__len__()):
            for row in range(pos_len):
                #per la prima colonna salva nella matrice tutte le probabilità di emissione (non calcolo quella di transizione perché nella prima colonna non c'è)
                if col == 0:
                    e_prob = read_files.get_eprob(pos_array[row], token_arr[col])
                    mat[row, col] = e_prob

                #per le successive colonne controllo le righe della colonna precedente e salvo la massima prob per ogni casella della colonna attuale
                else:
                    col_prev = col - 1
                    e_prob = read_files.get_eprob(pos_array[row], token_arr[col])
<<<<<<< HEAD
                    old_tag = pos_array[index_max_col]
                    t_prob = read_files.get_tprob(pos_array[row], old_tag)
                    temp_prob = max_col * float(e_prob) * float(t_prob)

                    if temp_prob > mat[row, col]:
                        mat[row, col] = temp_prob
=======
                    if e_prob == 0:
                        e_prob = save_prob

                    for idx in range(pos_len):
                        old_tag = pos_array[idx]
                        t_prob = read_files.get_tprob(pos_array[row], old_tag)
                        if t_prob == 0:
                            t_prob = save_prob

                        temp_prob = mat[idx, col_prev] * float(e_prob) * float(t_prob)

                        if temp_prob > mat[row, col]:
                            mat[row, col] = temp_prob
                            prev_states[row] = old_tag
>>>>>>> parent of a9306c1 (Update viterbi.py)

            #calcolo il max della colonna e salvo il pos del max nel backtrace
            if col != 0:
                index_max_col = mat.argmax(axis=0)[col]
                backtrace[col] = pos_array[index_max_col]



        for i in range(backtrace.__len__()):
            print(token_arr[i] + space + backtrace[i])

viterbi(corpus1)