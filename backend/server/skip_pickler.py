from modules.skipgram import SkipGram
import cPickle
import bz2
import time

#FOR PICKLING THE DEFAULT MODEL
'''
default_skipgram = SkipGram()
final_embeddings, low_dim_embs, reverse_dictionary, clustered_synonyms = default_skipgram.train()

file = bz2.BZ2File('./modules/default_skipgram.pkl.bz','wb')
cPickle.dump(default_skipgram, file)
file.close()
print('finished dumping')
'''

#FOR LOADING AND TESTING THE DUMPED MODEL
print('testing the dumped model')
file = bz2.BZ2File('./modules/default_skipgram.pkl.bz','rb')
model = cPickle.load(file)
file.close()
reverse_dictionary = model.reverse_dictionary
dictionary = model.dictionary
final_embeddings = model.final_embeddings
low_dim_embs = model.low_dim_embs
clustered_synonyms = model.clustered_synonyms

#FOR TESTING CLUSTERING
'''
print('beginning clustering')

start_time = time.time()
clustered_synonyms, final_embeddings, low_dim_embs = model.cluster(final_embeddings)
'''

#FOR TESTING CASCADING CLUSTERING
print('now testing re_clustering with target_keyword=dictatorship')
start_time = time.time()
target_keyword='computer'
clustered_synonyms, new_lowdim_embeddings, new_dictionary, new_reverse_dictionary = model.re_cluster(low_dim_embs, clustered_synonyms, target_keyword, dictionary, reverse_dictionary)

while len(new_reverse_dictionary) > 100:
	clustered_synonyms, new_lowdim_embeddings, new_dictionary, new_reverse_dictionary = model.re_cluster(new_lowdim_embeddings, clustered_synonyms, target_keyword, new_dictionary, new_reverse_dictionary)

#print('The new list of words')
#print(new_reverse_dictionary)
'''
def extractSynonyms(clustered_synonyms, target_keyword, dictionary, reverse_dictionary):
	index = dictionary[target_keyword]
	labels = clustered_synonyms.labels_

	target_label = labels[index]

	synonyms = ['']

	for i in range(len(labels)):
		if labels[i] == target_label:
			word = reverse_dictionary[i]
			synonyms.append(word)

	return synonyms
'''
synonyms = model.extractSynonyms(clustered_synonyms, target_keyword, new_dictionary, new_reverse_dictionary)
print("--- %s seconds ---" % (time.time() - start_time))
print('synonyms for '+target_keyword)
print(synonyms)


#FOR PICKLING THE REVERSE DICTIONARY
'''
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
'''