import random
from prob import get_tags, count_name
from pathlib import Path
import pyconll

file_pathdev1 = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Latin-LLCT-master/la_llct-ud-dev.conllu")
file_pathdevgreek = Path("C:/Users/funkt/Documents/GitHub/nlp-greek-latin-pos-tagger/UD_Ancient_Greek-Perseus-master/grc_perseus-ud-train.conllu")
corpus = pyconll.iter_from_file(file_pathdev1)
save_prob = 0.00000000001


# ritorna sempre NOUN
def simple_smooth():
    return "NOUN"


def simple_smooth_viterbi(pos):
    if pos == "NOUN":
        return 1
    else:
        return save_prob


# ritorna al 50% NOUN e 50% VERB
def simple_smooth_bis():
    if random.randint(0, 1) < 1:
        return "NOUN"
    else:
        return "VERB"


def simple_smooth_bis_viterbi(pos):
    if pos == "NOUN":
        return 0.5
    elif pos == "VERB":
        return 0.5
    else:
        return save_prob



# ritorna la probabilità 1/n_tag
def smooth_ntag():
    pos_array = get_tags()
    l_tag = len(pos_array)
    prob = 1 / l_tag
    return prob


# controllo quante parole compaiono una sola volta nel devtest e ritorno la percentuale del tag in input
def smooth_dev(dev_corpus, tag):

    one_word_dict = {}
    percentage_one_word = {}
    word_dict = count_name(dev_corpus)

    # aggiunge nel dizionario one_word tutte le parole che hanno occorrenza uno
    for word in word_dict:
        if word_dict[word] == 1:
            one_word_dict.update({word: ''})

    # salva i tag delle parole con occorrenza uno
    for sentence in dev_corpus:
        for token in sentence:
            if token.form in one_word_dict:
                one_word_dict[token.form] = token.upos

    # conta quanti tag ci sono fra le parole che compaiono una volta sola e il loro totale
    for word in one_word_dict:

        if one_word_dict[word] not in percentage_one_word:
            percentage_one_word.update({one_word_dict[word]: 1})
        else:
            percentage_one_word[word] += 1

    # divide il numero di ciascun tag per il totale
    for pos in one_word_dict:
        percentage_one_word[pos] /= len(one_word_dict)

    return percentage_one_word[tag]
