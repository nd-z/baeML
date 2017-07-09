#from baeML.backend.webcrawler import WebCrawler
from baeML.backend.skipgram import SkipGram
import bz2
import cPickle

class MainHandler(object):
	def __init__(self):
		file = bz2.BZ2File('../model.pkl.bz2', 'rb')
		model = cPickle.load(file)
		file.close()
		self.crawler = WebCrawler()

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