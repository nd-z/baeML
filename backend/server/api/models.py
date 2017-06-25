from django.db import models

#TODO wtf is this???
class Article(object):
	title=""
	link=""
	summary=""

	def __init__(self, title, link, summary):
		self.title = title
		self.link = link
		self.summary = summary