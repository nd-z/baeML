from django.db import models
from picklefield.fields import PickledObjectField

#Each model has an automatic field named 'id' which increments automatically

class Users(models.Model):
    user_fbid = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    propic_link = models.URLField(max_length=400)


class PklModels(models.Model):
	user_fbid = models.BigIntegerField(primary_key=True)
	pkl_model = PickledObjectField() #automatically pickles and unpickles the skipgram model
	user_keywords = PickledObjectField() 

class article(models.Model): #stores one article per user per row
							 #used to optimize, if users have the same interest

	user_fbid = models.IntegerField()
	article_name = models.CharField(max_length=45)
	# article_id = models.IntegerField()
	article_conent = PickledObjectField()
	user_rating = models.SmallIntegerField()
	article_link = models.URLField(max_length=400)

class Tags(models.Model): #stores the number for the keyword, maps keyword to article like a hash table
	keyword_id = models.IntegerField()
	article_id = models.IntegerField()	

class Keywords(models.Model):  #has a field keyword id by default
	keyword = models.CharField(max_length=45)


