import pyconll
from pathlib import Path
from mostUsedTag import most_used_tag


pos_tagged = {}


file_path = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master/la_llct-ud-train.conllu")
file_pathdev = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master/la_llct-ud-dev.conllu")
corpus = pyconll.iter_from_file(file_path)
corpus1 = pyconll.iter_from_file(file_pathdev)


#assegna il tag a ogni token in base al più frequente tag di quella parola
def baseline_tagger(corpusx):

    freq_tag_dict = most_used_tag(corpus)

    for sentence in corpusx:
        for token in sentence:
            for freq in freq_tag_dict:
                if freq == token.form and freq not in pos_tagged:
                    pos_tagged.update({freq : freq_tag_dict[freq]})

    return pos_tagged


baseline_tagger(corpus1)

print(pos_tagged)