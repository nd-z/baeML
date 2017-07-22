
import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings") #comment out
# import django #comment out
# django.setup() #comment out
import sys
import modules.skipgram
import modules.webcrawler
from modules.webcrawler import WebCrawler
from modules.skipgram import SkipGram
from api.models import *
import requests
import cPickle
import bz2
import zipfile
import json
from random import randrange
import time
from django.core.files import File
from django.http import HttpResponse, JsonResponse
import random
class MainHandler(object):
    def __init__(self):
        file = bz2.BZ2File('./modules/default_skipgram.pkl.bz','rb')
        self.default_model = cPickle.load(file) #loads a random model for the user's first login
        self.crawler = WebCrawler()

    def addTrainingData(self, training_data, user_id):
        file_number = int(time.time())
        f = open("{0}_training_data_{1}".format(user_id, file_number),"w+") #temp file
        normalized_data = WebCrawler.normalizeParagraphs(training_data)
        final_training_data = WebCrawler.replace_nonalpha(normalized_data)
        for content in final_training_data:
            f.write(content)
            f.write(' ')
        f.close()

        training_data_path = PklModels.objects.get(user_fbid=user_id).text_corpus.path
        with zipfile.ZipFile(training_data_path,"a") as training_data_zip:  #zip file to make compatible w/ skipgram module
            training_data_zip.write("{0}_training_data_{1}".format(user_id, file_number))
        os.remove("{0}_training_data_{1}".format(user_id, file_number)) #remove temp files
        skipgram_model = self.getUserModel(user_id)
        self.trainUserModel(skipgram_model, training_data_path, user_id) 

#when given new keywords,
    def addKeywords(self, keywords_list, user_id):
        user_model = PklModels.objects.get(user_fbid=user_id)
        orig_keyword_list = user_model.user_keywords
        jsonDec = json.decoder.JSONDecoder()
        myOrigList = jsonDec.decode(orig_keyword_list)
        myOrigList.extend(keywords_list)
        user_model.user_keywords = json.dumps(myOrigList)
        user_model.save()

    def getDefaultModel(self):
        return self.default_model

    def getUserModel(self, user_id):
        return PklModels.objects.get(user_fbid=user_id).pkl_model 

    def getUserKeywords(self, user_id):
        return PklModels.objects.get(user_fbid=user_id).user_keywords

    #NOTE: text_corpus should be a giant combination of all the content from processed links. The filename refers to a zip
    def trainUserModel(self, model, text_corpus_filename, user_id):
        print('train')
        if os.stat(text_corpus_filename).st_size > 5000000: #file size in bytes, 5mb
            final_embeddings, low_dim_embs, reverse_dictionary, clustered_synonyms = model.train(text_corpus_filename) #train after a threshold. add a field to the model to keep text corpus
            PklModels.objects.get(user_fbid=user_id).pkl_model = model
            PklModels.objects.get(user_fbid=user_id).save()

    def getLinks(self, keywords):
        query = 'http://www.bing.com/news/search?q='
        for kw in keywords:
            query += str(kw)+'+'
        links = self.crawler.crawl(query+'&go=Submit&qs=bs&form=QBLH', keywords)
        return links

    def getLinkContent(self, link):
        content = self.crawler.grabContent(link)
        return content #list of paragraphs

    def get_article(self, user_id):
        keywords = self.getUserKeywords(user_id)
        user_article_dict = Users.objects.get(user_fbid=user_id).articles
        jsonDec = json.decoder.JSONDecoder()
        decoded_user_article_dict = jsonDec.decode(user_article_dict)
        links = self.getLinks(keywords[random.randint(0, len(keywords) - 1)])
        article_content = None
        article_link = None
        print links
        print keywords
        for link in links:
            if link not in decoded_user_article_dict:
               article_link = link 
               decoded_user_article_dict[article_link] = 0
               Users.objects.get(user_fbid=user_id).articles = user_article_dict
               Users.objects.get(user_fbid=user_id).save()
               article_content = self.getLinkContent(article_link)
               break
            else: #return error/ refresh
                print 'broke here'
                return "Error fetching new article"
        if (article_content is not None and article_link is not None):
            self.addTrainingData(article_content, user_id)
        else:
            print 'broke at end'
            return "Error fetching new article"
        response = {'article_link': article_link, 'article': article_content}
        return response

'''Modular Testing'''

# mh = MainHandler()

#==Tested User Init, added to views.py==
# user_id = 136341273775461
# name = "JanicChan"
# propic_link = "http://www.google.com"
# newUser = Users(user_fbid=user_id, name=name, propic_link=propic_link)
# articles_list = {}
# newUser.articles = json.dumps(articles_list)
# newUser.save()

# #==Tested Pkl Model Creation==
# user_id  = 1363412733775461
# userSkipGramModel = PklModels()
# userSkipGramModel.user_fbid = user_id
# userSkipGramModel.pkl_model = mh.getDefaultModel()
# userSkipGramModel.user_keywords = json.dumps([])
# empty_file = open("empty","w+")
# empty_file.close()
# with zipfile.ZipFile("{0}_training_data.zip".format(user_id), "w") as myzip:
#         myzip.write("empty")
# os.remove("empty") #remove temp files
# userSkipGramModel.text_corpus = File(open("{0}_training_data.zip".format(user_id))) 
# os.remove("{0}_training_data.zip".format(user_id))
# userSkipGramModel.save()

#Check model size is the same - ok
# model = PklModels.objects.get(user_fbid=1363412733775461).pkl_model
# print sys.getsizeof(model)
# print sys.getsizeof(mh.getDefaultModel())
'''
#==Tested add keywords==
mh.addKeywords(["keywordssss","listttt"], 1363412733775461)
#Check that it's there
orig_keyword_list = mh.getUserKeywords(1363412733775461)
jsonDec = json.decoder.JSONDecoder()
myOrigList = jsonDec.decode(orig_keyword_list)
print(myOrigList)
'''

#==Tested Pkl Model Add Training Data & train user model==
# mh.addTrainingData(['I am adding a paragraph for training data', 'testing with coherent sentences'], 1363412733775461)

'''
#REMAINING TODO:
#Create new user, Test article fetch  & ratings post 
'''