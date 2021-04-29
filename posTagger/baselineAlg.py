import pyconll
from pathlib import Path
from prob import most_used_tag
import accuracyBaseline
import smooth

pos_tagged = {}


file_path = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master/la_llct-ud-train.conllu")
file_pathdev = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master/la_llct-ud-dev.conllu")
corpus = pyconll.iter_from_file(file_path)
corpus1 = pyconll.iter_from_file(file_pathdev)


#assegna il tag a ogni token in base al più frequente tag di quella parola
def baseline_tagger(corpusx):
    freq_dict = most_used_tag(corpus)
    for sentence in corpusx:
        for token in sentence:

            if token.form not in freq_dict:
                pos = smooth.simple_smooth()
            else:
                pos = freq_dict[token.form]

            pos_tagged.update({token.form: pos})

    accuracyBaseline.calc_accuracy(pos_tagged, file_pathdev)

baseline_tagger(corpus1)
