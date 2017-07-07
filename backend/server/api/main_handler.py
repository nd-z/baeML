#from baeML.backend.webcrawler import WebCrawler
#from baeML.backend.skipgram import SkipGram
import cPickle
import bz2

class MainHandler(object):
	def __init__(self):
		file = bz2.BZ2File('./model.pkl.bz2', 'rb')
		self.default_model = cPickle.load(file) #loads a random model for the user's first login
		self.crawler = WebCrawler()

#when given new keywords from init,
    def post(self, request, user_id):
		req = json.loads(request.body)
		user_id = user_id
		keywords = req['keywords']
		#add to database

		#update ML module (andy's ML <=> db helper function)
		#give pickled model to db

#when asked for next article, frontend goes directly to here
	def get(self, request, user_id):
		user_id = user_id
		#figure out how we're storing the articles (read vs unread)
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
