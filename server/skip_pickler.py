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

#FOR TESTING CLUSTERING
'''
print('beginning clustering')

start_time = time.time()
clustered_synonyms, final_embeddings, low_dim_embs = model.cluster(final_embeddings)
'''
'''
reverse_dictionary = model.reverse_dictionary
dictionary = model.dictionary
final_embeddings = model.final_embeddings
low_dim_embs = model.low_dim_embs
clustered_synonyms = model.clustered_synonyms

#FOR TESTING CASCADING CLUSTERING
print('now testing re_clustering with target_keyword=dictatorship')
start_time = time.time()


target_keyword='dictatorship'
clustered_synonyms, new_lowdim_embeddings, new_dictionary, new_reverse_dictionary = model.re_cluster(low_dim_embs, clustered_synonyms, target_keyword, dictionary, reverse_dictionary)

while len(new_reverse_dictionary) > 10:
	clustered_synonyms, new_lowdim_embeddings, new_dictionary, new_reverse_dictionary = model.re_cluster(new_lowdim_embeddings, clustered_synonyms, target_keyword, new_dictionary, new_reverse_dictionary)

synonyms = model.extractSynonyms(clustered_synonyms, target_keyword, new_dictionary, new_reverse_dictionary)

synonyms.remove('')
synonyms.remove(target_keyword)

print("--- %s seconds ---" % (time.time() - start_time))
print('synonyms for '+target_keyword)
print(synonyms)
'''


#FOR TESTING KEYWORD GENERATION
def generateNewKeywords(model, known_keywords):

	#the generated keyword list
	new_keyword_list = []

	reverse_dictionary = model.reverse_dictionary
	dictionary = model.dictionary
	final_embeddings = model.final_embeddings
	low_dim_embs = model.low_dim_embs
	clustered_synonyms = model.clustered_synonyms

	for kw in known_keywords:
		new_clustered_synonyms, new_lowdim_embeddings, new_dictionary, new_reverse_dictionary = model.re_cluster(low_dim_embs, clustered_synonyms, kw, dictionary, reverse_dictionary)

		while len(new_reverse_dictionary) > 10:
			new_clustered_synonyms, new_lowdim_embeddings, new_dictionary, new_reverse_dictionary = model.re_cluster(new_lowdim_embeddings, new_clustered_synonyms, kw, new_dictionary, new_reverse_dictionary)

		synonyms = model.extractSynonyms(new_clustered_synonyms, kw, new_dictionary, new_reverse_dictionary)

		synonyms.remove('')
		synonyms.remove(kw)

		new_keyword_list.extend(synonyms)

	return new_keyword_list

known_keywords = ['government', 'economics', 'democrat']
generated_list = generateNewKeywords(model, known_keywords)

print(generated_list)

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