from modules.skipgram import SkipGram
import cPickle
import bz2

default_skipgram = SkipGram()
default_skipgram.train()

file = open('./modules/default_skipgram.pkl','wb')
cPickle.dump(default_skipgram, file)