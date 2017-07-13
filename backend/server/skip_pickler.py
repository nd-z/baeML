from modules.skipgram import SkipGram
import cPickle
import bz2

'''
#FOR PICKLING THE DEFAULT MODEL
default_skipgram = SkipGram()
default_skipgram.train()

file = bz2.BZ2File('./modules/default_skipgram.pkl.bz','wb')
cPickle.dump(default_skipgram, file)
'''

#FOR PICKLING THE REVERSE DICTIONARY
file = bz2.BZ2File('./modules/default_skipgram.pkl.bz','rb')
default_skipgram = cPickle.load(file)
reverse_dict = default_skipgram.reverse_dictionary

filter_words = []
i = 0

while i < 113:
    #lol this is so shady
    if i != 64 and i != 82 and i != 84 and i != 86 and i != 101 and i != 103:
        filter_words.append(reverse_dict[i])
    i += 1

print(filter_words)
file = open('filter_words.pkl', 'wb')
cPickle.dump(filter_words, file)