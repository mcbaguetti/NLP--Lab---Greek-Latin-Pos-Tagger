import random
from prob import count_npos, count_name


#ritorna sempre NOUN
def simple_smooth():
    return "NOUN"


#ritorna al 50% NOUN e 50% VERB
def simple_smooth_bis():
    if random.randint(0, 1) < 1:
        return "NOUN"
    else:
        return "VERB"


#ritorna la probabilità 1/n_tag del tag in input
def smooth_ntag(tag):
    pos_dict = count_npos()
    eprob = 1 / pos_dict[tag]
    return eprob


#controllo quante parole compaiono una sola volta nel devtest e ritorno la percentuale del tag in input
def smooth_dev(dev_corpus, tag):

    one_word_dict = {}
    percentage_one_word = {}
    word_dict = count_name(dev_corpus)


    #aggiunge nel dizionario one_word tutte le parole che hanno occorrenza uno
    for word in word_dict:
        if word_dict[word] == 1:
            one_word_dict.update({word: ''})


    #salva i tag delle parole con occorrenza uno
    for sentence in dev_corpus:
        for token in sentence:
            if token.form in one_word_dict:
                one_word_dict[token.form] = token.upos


    #conta quanti tag ci sono fra le parole che compaiono una volta sola e il loro totale
    for word in one_word_dict:
        tot = 0

        if one_word_dict[word] not in percentage_one_word:
            percentage_one_word.update({one_word_dict[word]: 1})
        else:
            percentage_one_word[word] += 1

        tot += 1


    #divide il numero di ciascun tag per il totale
    for pos in one_word_dict:
        percentage_one_word[pos] /= tot

    return percentage_one_word[tag]
