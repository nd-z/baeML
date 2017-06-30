from rest_framework import serializers
from .models import Users

#TODO AHHHHHHH
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('id', 'user_fbid', 'name', 'token', 'propic_link')
    	