import pyconll
from pathlib import Path


slash = " / "
countname = {}
cprob = {}
frequent_tag_word = {}

used_tag_latin = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/probabilities/latin/most-used-tags.txt")
file_path = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master/la_llct-ud-train.conllu")
corpus = pyconll.iter_from_file(file_path)
corpus1 = pyconll.iter_from_file(file_path)

#conta le frequenze dei nomi
def count_name(corpus):
    for sentence in corpus:
        for token in sentence:
            name = token.form
            #se non c'è un name lo aggiunge nelle key di eprob e lo inizializza a 1, altrimenti aumenta di 1 il val del pos
            if name not in countname.keys():
                countname.update({name : 1})
            else:
                countname[name] += 1


def most_used_tag(corpus):
    # la prima parte della funzione calcola le occorrenze delle varie combinazioni parola / tag

    for sentence in corpus:
        for token in sentence:

            name = token.form + slash + token.upos

            # se non c'è un name lo aggiunge nelle key di cprob e lo inizializza a 1, altrimenti aumenta di 1 il val del pos
            if name not in cprob.keys():
                cprob.update({name: 1})
            else:
                cprob[name] += 1

    # divide i value di cprob per il corrispettivo value di countname, cioè con lo stesso name
    for name in cprob:
        # salva in una str la prima parte della key di cprob cioè il nome
        key_name = name.split(slash, 1)[0]
        if key_name in countname.keys():
            cprob[name] /= countname[key_name]

    copy_dict = cprob.copy()
    #trova la parola con il tag più frequente per una ciascuna parola
    for name in cprob:
        key_name = name.split(slash, 1)[0]
        key_pos = name.split(slash, 1)[1]
        for copy in copy_dict:
            key_copy_name = copy.split(slash, 1)[0]
            if key_copy_name == key_name and cprob[name] >= copy_dict[copy]:
                frequent_tag_word.update({key_name : key_pos})

    #scrive nel file il dizionario eprob
    with open(used_tag_latin, 'w') as file:
        for key in sorted(frequent_tag_word.keys()):
            file.write("%s = %s \n" % (key, frequent_tag_word[key]))

count_name(corpus)
freq_tag = most_used_tag(corpus1)
