import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
import django
django.setup()
import modules.skipgram
import modules.webcrawler
from modules.webcrawler import WebCrawler
from modules.skipgram import SkipGram
from api.models import *
import requests
import cPickle
import bz2
import zipfile
from random import randrange

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
            orig_keyword_list = getUserKeywords()

        except PklModels.DoesNotExist:
            print('failed to get model')

        orig_keyword_list.append(keywords_list)
        PklModels.objects.get(user_fbid=user_id).save()


#TODO FINISH
#when asked for next article (one), frontend makes a get request, probably move parts of this to views.py
    def get(self, user_id):
        keywords = getUserKeywords(user_id)

        links, linked_keywords = getLinks(keywords) #assuming webcrawler can return the keyword a particular link is associated with
        random_index = randrange(0,len(links)) #get a random keyword
        article_link = links[random_index]
        article_content, article_name = getLinkContent(article_link)
        article_keyword = linked_keywords[random_index]
# check if link exists  in tags model, then check read vs unread; while read, then get another keyword; if link doesn't exist then fetch link content
#update keywords
        articleModel = article(user_fbid=user_id, article_name=article_name, article_content=article_content, user_rating=0, article_link=article_link)
        articleModel.save()

        tagModel = Tags(keyword_id=Keywords.objects.get(keyword=article_keyword).pk, article_link=article_link, article_id=article.get(articleModel).pk)
        tagModel.save()
        return article_content, article_link

    def getDefaultModel(self):
        return self.default_model

    def getUserModel(self, user_id):
        return PklModels.objects.get(user_fbid=user_id).pkl_model 

    def getUserKeywords(self, user_id):
        return PklModels.objects.get(user_fbid=user_id).user_keywords

#TODO TEST
    #NOTE: text_corpus should be a giant combination of all the content from processed links. The filename refers to a zip
    def trainUserModel(self, model, text_corpus_filename, user_id):
        final_embeddings, reverse_dictionary, similarity, clustered_synonyms = model.train(text_corpus_filename)
        PklModels.objects.get(user_fbid=user_id).pkl_model = model #update db model
        PklModels.objects.get(user_fbid=user_id).pkl_model.save()

    def getLinks(self, keywords):
        query = 'http://www.bing.com/search?q='
        for kw in keywords:
            query += str(kw)+'+'
        links = self.crawler.crawl(query+'&go=Submit&qs=bs&form=QBLH', keywords)
        return links

    def getLinkContent(self, link):
        content = self.crawler.grabContent(link)
        return content

'''Testing'''
mh = MainHandler()
userSkipGramModel = PklModels()
userSkipGramModel.user_fbid = 1363412733775461
userSkipGramModel.pkl_model = mh.getDefaultModel()
# userSkipGramModel.user_keywords = []
# userSkipGramModel.save()
# mh.addTrainingData()

