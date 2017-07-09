from django.db import models

#Each model has an automatic field named 'id' which increments automatically

class Users(models.Model):
    user_fbid = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    propic_link = models.URLField(max_length=400)

class article(models.Model):
	fk_user = models.IntegerField()
	article_name = models.CharField(max_length=45)
	user_rating = models.SmallIntegerField()

class Tags(models.Model):
	fk_keyword_id = models.IntegerField()
	fk_recommendation_id = models.IntegerField()	

class Keywords(models.Model): 
	keyword = models.CharField(max_length=45)

class PklModels(models.Model):
	user_fbid = models.BigIntegerField(primary_key=True)
	#TODO check if this is okay
	pkl_model = models.FileField(upload_to='pkl_models/'+str(user_fbid)+'/') #
