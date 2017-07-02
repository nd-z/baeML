import os
import numpy as np
import zipfile
import collections
import tensorflow as tf
from six.moves import urllib
from skipgram import SkipGram
#from webcrawler import WebCrawler

'''interacts with database and webcrawler modules (not sure how that will work just yet)
also main communication point w/ frontend'''
class BackendHandler(object):
	def __init__(self):
		#initialize a crawler and default model
		self.crawler = WebCrawler()
		self.def_model = SkipGram()

	def getUserModel(userid):
		#TODO: grab model data from database w/ userid

	def makeUserModel(userid):
		#TODO: train model with a zip of a bunch of articles pulled

	def getLinks():
