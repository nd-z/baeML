from rest_framework import serializers
from .models import ArticleRetriever

#TODO AHHHHHHH
class ArticleRetrieverSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleRetriever
        fields = ('user_id', 'articles')
        read_only_fields = ('user_id')