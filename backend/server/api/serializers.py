from rest_framework import serializers
import .models

#TODO AHHHHHHH
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('user_fbid', 'name', 'token', 'propic_link')

class PklSerializer(serializers.ModelSerializer):
	class Meta:
		model = PklModels
		fields = ('user_fbid', 'pkl_model')
    	