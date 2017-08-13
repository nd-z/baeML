from rest_framework import serializers
import models

#TODO AHHHHHHH
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Users
        fields = ('user_fbid', 'name', 'token', 'propic_link')

class PklSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.PklModels
		fields = ('user_fbid', 'pkl_model')
    	