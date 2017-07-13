
import modules.skipgram
import modules.webcrawler
from modules.webcrawler import WebCrawler
from modules.skipgram import SkipGram
import cPickle
import bz2

class MainHandler(object):
    def __init__(self):
		file = bz2.BZ2File('./modules/default_skipgram.pkl.bz','rb')
		self.default_model = cPickle.load(file) #loads a random model for the user's first login
		self.crawler = WebCrawler()

		#what to do with tags model

#when given new keywords from init,
    def addKeywords(self, keywords_list, user_id):
        user_id = user_id
        keyword_list = keywords_list

		# keywords = Keywords(id='''get the user's id based on fb id)''', keyword=???)
        # keywords.save()


		#add to database

		#update ML module (andy's ML <=> db helper function)
		#give pickled model to db
		#call filtering method

#when asked for next article, frontend goes directly to here
    def getArticles(self, user_id):
		user_id = user_id
		#TODO add read vs unread field to db. mark articles as read so we don't repeat.
		#feed database keywords, newest first, to webcrawler
		#ask webcralwer to return articles and store in db
		#frontend should get articles from main, which fetches newest article from db

    def getDefaultModel(self):
		return self.default_model

    def getUserModel(self, user_id):
		#TODO query Django for the model
		return

	#NOTE: text_corpus should be a giant combination of all the content from processed links
    def trainUserModel(self, model, text_corpus):
		# TODO prepare text as zip and train()
		# TODO update db with new model pkl
		return

    def getLinks(self, keywords):
		query = 'http://www.bing.com/search?q='
		for kw in keywords:
			query += str(kw)+'+'
		links = self.crawler.crawl(query+'&go=Submit&qs=bs&form=QBLH', keywords)
		return links

    def getLinkContent(self, link):
		content = self.crawler.grabContent(link)
		#TODO update db list of links that have been processed
		return content

mh = MainHandler()

