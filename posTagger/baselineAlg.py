import pyconll
from pathlib import Path
from prob import most_used_tag
import accuracyBaseline
import smooth

pos_tagged = {}


file_path = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master/la_llct-ud-train.conllu")
file_pathdev = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master/la_llct-ud-dev.conllu")
file_pathdevgreek = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Ancient_Greek-Perseus-master/grc_perseus-ud-train.conllu")
file_pathdevgreek1 = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Ancient_Greek-Perseus-master/grc_perseus-ud-dev.conllu")

corpus = pyconll.iter_from_file(file_path)
corpus1 = pyconll.iter_from_file(file_pathdev)
#corpus = pyconll.iter_from_file(file_pathdevgreek)
#corpus1 = pyconll.iter_from_file(file_pathdevgreek1)


# assegna il tag a ogni token in base al più frequente tag di quella parola
def baseline_tagger(corpusx):
    freq_dict = most_used_tag(corpus)
    for sentence in corpusx:
        for token in sentence:

            if token.form not in freq_dict:
                pos = smooth.simple_smooth_bis()
            else:
                pos = freq_dict[token.form]

            pos_tagged.update({token.form: pos})

    accuracyBaseline.calc_accuracy(pos_tagged, file_pathdev)


baseline_tagger(corpus1)
