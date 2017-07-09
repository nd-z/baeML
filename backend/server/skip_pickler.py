from modules.skipgram import SkipGram
import cPickle
import bz2

default_skipgram = SkipGram()
default_skipgram.train()

file = bz2.BZ2File('./modules/default_skipgram.pkl.bz','wb')
cPickle.dump(default_skipgram, file)
