
import os
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
import ast
from random import randrange
import time
from django.core.files import File
from django.http import HttpResponse, JsonResponse
import random
class MainHandler(object):
    def __init__(self):
        #first login
        self.crawler = WebCrawler()
        self.jsonDec = json.decoder.JSONDecoder()

    def addTrainingData(self, training_data, user_id):
        file_number = int(time.time())
        f = open("{0}_training_data_{1}".format(user_id, file_number),"w+") #temp file
        final_training_data = WebCrawler.filter_content(training_data)
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
        myOrigList = self.jsonDec.decode(orig_keyword_list)
        myOrigList.extend(keywords_list)
        user_model.user_keywords = json.dumps(myOrigList)
        user_model.save()

    def getDefaultModel(self):
        file = bz2.BZ2File('./modules/default_skipgram.pkl.bz','rb')
        self.default_model = cPickle.load(file) #loads a random model for the user's 
        return self.default_model

    def getUserModel(self, user_id):
        return PklModels.objects.get(user_fbid=user_id).pkl_model

    def getUserKeywords(self, user_id):
        return str(PklModels.objects.get(user_fbid=user_id).user_keywords)

    #NOTE: text_corpus should be a giant combination of all the content from processed links. The filename refers to a zip
    def trainUserModel(self, model, text_corpus_filename, user_id):
        print('train')
        if os.stat(text_corpus_filename).st_size > 5000000: #file size in bytes, 5mb
            final_embeddings, low_dim_embs, reverse_dictionary, clustered_synonyms = model.train(text_corpus_filename) #train after a threshold. add a field to the model to keep text corpus
            user_model = PklModels.objects.get(user_fbid=user_id)
            user_model.pkl_model = model
            user_model.save()

            #update keywords list with clustered synonyms
            user_model = PklModels.objects.get(user_fbid=user_id)
            orig_keyword_list = user_model.user_keywords
            myOrigList = self.jsonDec.decode(orig_keyword_list)
            
            #run synonym extraction using the custom user model
            # and replace keywords with the synonyms
            #rationale: we don't want to keep outdated keywords, because the
            # new keywords allow for greater accuracy/relevance to the user
            generated_keywords = self.generateNewKeywords(model, myOrigList)

            #add the generated keywords to the user keyword list and update model
            user_model.user_keywords = json.dumps(generated_keywords)
            user_model.save()


    def getLinks(self, keywords):
        print(keywords)
        query = 'http://www.bing.com/news/search?q='
        print('keywords for links: '+keywords)
        
        #if keywords is a string, it will take it char by char
        if (type(keywords) is list):
            for kw in keywords:
                query += str(kw)+'+'
                print(kw, "keyyyy")
        else:
            query += keywords
        print query
        links = self.crawler.crawl(query+'&go=Submit&qs=bs&form=QBLH', keywords)
        return links

    def getLinkContent(self, link):
        print("getting link contnet", link)
        content = self.crawler.grabContent(link)
        return content #list of paragraphs

    def get_article(self, user_id):
        # print('trying to optimize')    
        # user = Users.objects.get(user_fbid=user_id) #optimization: return unread articles first
        # all_user_articles = user.articles
        # all_articles_dict = self.jsonDec.decode(all_user_articles)
        # print('got all articles')
        # for article in all_articles_dict:
        #     print('in for loop')
        #     print(article)
        #     if all_articles_dict[article] == 0:
        #         article_link = article
        #         article_content = self.getLinkContent(article_link)
        #         article_title = WebCrawler.grabTitle(article_link)
        #         response = {'article_link': article_link, 'article': article_content, 'article_title': article_title}
        #         return response
        # print('exited for loop..should be good')
        keywords = self.getUserKeywords(user_id)

        #keywords from db is a skipgram obj, cvt to string then to list
        keywords = ast.literal_eval(keywords)
        
        
        #user_article_dict is a unicode string
        user_article_dict = Users.objects.get(user_fbid=user_id).articles
        decoded_user_article_dict = self.jsonDec.decode(user_article_dict)


        #breaks when keyword is a letter or some nonsensical thing
        target_kw = random.choice(keywords)

        links = self.getLinks(target_kw)
        article_content = None
        article_link = None
        print 'i fucking hate everything'
        print links
        print keywords
        for link in links:

            if link not in decoded_user_article_dict:
                article_link = link 
                decoded_user_article_dict[article_link] = 0
                print('in main handler', decoded_user_article_dict)
                user = Users.objects.get(user_fbid=user_id)
                user.articles = json.dumps(decoded_user_article_dict)
                try:
                    article_content = self.getLinkContent(article_link)
                    user.save()
                    break
                except:
                    continue
                
        
        if (article_content is not None and article_link is not None):
            print('adding training data')
            self.addTrainingData(article_content, user_id)
        else:
            print 'broke at end'
            print(article_link)
            print(article_content)
            return "Error fetching new article"
        article_title = WebCrawler.grabTitle(article_link)
        response = {'article_link': article_link, 'article': article_content, 'article_title': article_title}
        return response

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