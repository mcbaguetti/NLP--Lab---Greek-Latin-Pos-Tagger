from pathlib import Path

error = 0.0
equal = " = "
arrow = " -> "
tr_latin_file_path = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/probabilities/latin/transmission-prob.txt")
em_latin_file_path = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/probabilities/latin/emission-prob.txt")

#prende le probabilità tag -> word, se non riesce a trovare nulla ritorna 0.0
def get_eprob(tag, word):
    prob_name = tag + arrow + word

    with open(em_latin_file_path, 'r') as file:
        for line in file:
            if prob_name in line:
                prob = line.split(equal, 1)[1]
                float(prob)
                return prob
    return error


#prende le probabilità old_tag -> tag, se non riesce a trovare nulla ritorna 0.0
def get_tprob(tag, old_tag):
    prob_name = old_tag + arrow + tag

    with open(tr_latin_file_path, 'r') as file:
        for line in file:
            if prob_name in line:
                prob = line.split(equal, 1)[1]
                float(prob)
                return prob
    return error