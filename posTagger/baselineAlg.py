import pyconll
from pathlib import Path
from read_files import get_most_used_tag
import accuracyBaseline

pos_tagged = {}


file_path = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master/la_llct-ud-train.conllu")
file_pathdev = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master/la_llct-ud-dev.conllu")
corpus = pyconll.iter_from_file(file_path)
corpus1 = pyconll.iter_from_file(file_pathdev)


#assegna il tag a ogni token in base al più frequente tag di quella parola
def baseline_tagger(corpusx):

    for sentence in corpusx:
        for token in sentence:
            pos = get_most_used_tag(token.form)
            pos_tagged.update({token.form : pos})

    accuracyBaseline.calc_accuracy(pos_tagged, file_pathdev)

baseline_tagger(corpus1)

