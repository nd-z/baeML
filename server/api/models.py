from django.db import models
from picklefield.fields import PickledObjectField
import os
#Each model has an automatic field named 'id' which increments automatically

class Users(models.Model):
    user_fbid = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    propic_link = models.URLField(max_length=400)
    articles = models.TextField(null=True) #list of article links
    init_complete = models.BooleanField(default=False)

class PklModels(models.Model):
    user_fbid = models.BigIntegerField(primary_key=True)
    pkl_model = PickledObjectField() #automatically pickles and unpickles the skipgram model
    user_keywords = models.TextField(null=True)
    text_corpus = models.FileField(upload_to='training_data')