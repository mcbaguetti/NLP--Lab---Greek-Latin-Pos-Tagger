import viterbiAlg
import baselineAlg

language = ''
name_method = ''
smooth = ''

while language not in ('latin', 'greek'):
    language = input("enter language: [latin/greek]")

while name_method not in ('baseline', 'hmm', 'memm'):
    name_method = input("enter algorithm name: [baseline/hmm/memm]")


#while smooth not in ('simple', '', 'memm'):
#    smooth = input("enter smooth type: [simple]")

if name_method == 'hmm':
    viterbiAlg.viterbi(language)

elif name_method == 'baseline':
    baselineAlg.baseline_tagger(language)

#else :
    #memm