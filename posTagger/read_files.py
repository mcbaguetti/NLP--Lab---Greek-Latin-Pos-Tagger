from pathlib import Path
import numpy as np

#easy smooth
noun = "NOUN"
new_line = "\n"
error = 0.0
n_tag = 17
equal = " = "
space = " "
arrow = " -> "
tr_latin_file_path = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/probabilities/latin/transmission-prob.txt")
em_latin_file_path = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/probabilities/latin/emission-prob.txt")
latin_most_used = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/probabilities/latin/most-used-tags.txt")
tags_fp = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/probabilities/latin/tags.txt")

#ritorna il pos_tag più usato per quella parola, se non c'è ritorna NOUN
def get_most_used_tag(word):

    with open(latin_most_used, 'r') as file:
        for line in file:
            if word in line:
                pos = line.split(equal, 1)[1]
                pos = pos.split(space, 1)[0]
                return pos

    #se il codice non ha trovato nessun risultato a word sarà assegnato NOUN
    return noun


#ritorna un array con i tag in ordine
def get_tags():

    pos_array = np.empty(shape=n_tag, dtype=np.dtype('U25'))

    with open(tags_fp, 'r') as file:

        count = 0

        for line in file:
            pos = line.split(new_line, 1)[0]
            pos_array[count] = pos
            count += 1

    return pos_array
