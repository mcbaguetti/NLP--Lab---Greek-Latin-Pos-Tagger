tot_word = 0
correct = 0
tot_sentence = 0


def save_num(backtrace, sentence):

    count = 1
    global correct
    global tot_word
    global tot_sentence

    for token in sentence:
        if token.upos == backtrace[count]:
            correct += 1

        count += 1
        tot_word += 1

    tot_sentence += 1


def print_accuracy():
    print("sentences number: " + str(tot_sentence))
    print("correct word: " + str(correct))
    print("tot word: " + str(tot_word))
    print("accuracy: " + str(correct/tot_word))