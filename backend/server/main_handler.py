
import modules.skipgram
import modules.webcrawler
from modules.webcrawler import WebCrawler
from modules.skipgram import SkipGram
from api.models import PklModels
import requestsu
import cPickle
import bz2
import zipfile

class MainHandler(object):
    def __init__(self):
        file = bz2.BZ2File('./modules/default_skipgram.pkl.bz','rb')
        self.default_model = cPickle.load(file) #loads a random model for the user's first login
        self.crawler = WebCrawler()

#TODO: TEST
    def addTrainingData(self, training_data, user_id):
         try:
            skipgram_model = getUserModel(user_id)

        except PklModels.DoesNotExist:
            print('failed to get model')
        f = open('training_data/' + user_id,'w+') #temp file
        
        for content in training_data:
            f.write(content)
        f.close()
        with ZipFile('training_data/' + user_id + '.zip', 'w') as myzip:
            myzip.write('training_data/' + user_id)#zip file to make compatible w/ skipgram module
        trainUserModel(skipgram_model, 'training_data/' + user_id + '.zip', user_id)
        os.remove('training_data/' + user_id + '.zip')

#TODO: TEST
#when given new keywords,
    def addKeywords(self, keywords_list, user_id):
        user_id = user_id
        keyword_list = keywords_list #should already be filtered
        try:
            orig_keyword_list = PklModels.objects.get(user_fbid=user_id).user_keywords

        except PklModels.DoesNotExist:
            print('failed to get model')

        orig_keyword_list.append(keywords_list)

#TODO FINISH
#when asked for next article, frontend makes a get request directly to here
    def get(self, user_id):
        user_id = user_id
        #TODO check db that we don't repeat and also to optimize
        #feed user's keywords to webcrawler
        #ask webcralwer to return articles and store name, content, link in db | tags | articles | keywords
        #frontend should get articles from main, which fetches newest article from db

    def getDefaultModel(self):
        return self.default_model

    def getUserModel(self, user_id):
        return PklModels.objects.get(user_fbid=user_id).pkl_model 

#TODO TEST
    #NOTE: text_corpus should be a giant combination of all the content from processed links. The filename refers to a zip
    def trainUserModel(self, model, text_corpus_filename, user_id):
        final_embeddings, reverse_dictionary, similarity, clustered_synonyms = model.train(text_corpus_filename)
        getUserModel(user_id) = model #update db model
        getUserModel(user_id).save()

    def getLinks(self, keywords):
        query = 'http://www.bing.com/search?q='
        for kw in keywords:
            query += str(kw)+'+'
        links = self.crawler.crawl(query+'&go=Submit&qs=bs&form=QBLH', keywords)
        return links

    def getLinkContent(self, link):
        content = self.crawler.grabContent(link)
        return content

