import pyconll

tot_word = 0
correct = 0
tot_sentence = 0


def calc_accuracy(pos_dict, path):
    corpus = pyconll.iter_from_file(path)

    global correct
    global tot_word
    global tot_sentence

    for sentence in corpus:
        tot_sentence += 1
        for token in sentence:
            print(token.form)
            print(token.upos)
            if pos_dict[token.form] == token.upos:
                correct += 1
            tot_word += 1

    print("sentences number: " + str(tot_sentence))
    print("correct word: " + str(correct))
    print("tot word: " + str(tot_word))
    print("accuracy: " + str(correct/tot_word))
