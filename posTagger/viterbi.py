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
save_prob = 0.0000000001

def viterbi(corpus):

    pos_array = read_files.get_tags()
    pos_len = pos_array.__len__()

    for sentence in corpus:

        s_length = sentence.__len__()
        mat = np.ndarray(shape=(s_length + special_char, pos_len), dtype=float, order='F')
        token_arr = np.empty(shape=(s_length + special_char), dtype=np.dtype('U25'))
        count = 0
        token_arr[count] = sos
        backtrace = np.empty(shape=(s_length + special_char), dtype=np.dtype('U25'))
        backtrace[0] = sos

        #inizializzo l'array di token
        for token in sentence:
            count += 1
            token_arr[count] = token.form

        token_arr[count + 1] = eos
        row_length = pos_len
        print(token_arr)

        for col in range(token_arr.__len__()):
            for row in range(pos_len):
                #per la prima colonna salva nella matrice tutte le probabilità di emissione (non calcolo quella di transizione perché nella prima colonna non c'è)
                if col == 0:
                    print(pos_array[row] + token_arr[col])
                    e_prob = read_files.get_eprob(pos_array[row], token_arr[col])
                    mat[row, col] = e_prob
                #per le successive colonne controllo le righe della colonna precedente e salvo la massima prob per ogni casella della colonna attuale
                else:
                    col_prev = col - 1
                    e_prob = read_files.get_eprob(pos_array[row], token_arr[col])
                    print(e_prob)
                    if e_prob == 0:
                        e_prob = save_prob

                    while row_length > 0:
                        old_tag = pos_array[pos_len - row_length]
                        t_prob = read_files.get_tprob(pos_array[row], old_tag)
                        print(t_prob)
                        if t_prob == 0:
                            t_prob = save_prob

                        temp_prob = mat[pos_len - row_length, col_prev] * abs(np.log(float(e_prob)) + np.log(float(t_prob)))

                        if temp_prob > mat[row, col]:
                            mat[row, col] = temp_prob
                            backtrace[col] = old_tag

                        row_length -= 1

        for i in range(backtrace.__len__()):
            print(token_arr[i] + space + backtrace[i])

viterbi(corpus1)