from .models import Users, PklModels
from .services import ArticleRetriever
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from facebook_api_handler import FacebookAPI
import json
import sys
import os
import zipfile
from django.core.files import File
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(path)
from main_handler import MainHandler

class UsersView(APIView):
    serializer_class = UserSerializer

    #/api/login
    def get(self, request):

        #commented out to test initializing user
        user_fbid = request.GET.get('user_ID')
        try:
            #print(user_fbid)
            entry = Users.objects.get(user_fbid=user_fbid)
            #print('didnt break at entry=...')
            #print(type(user_fbid))
            #print(entry)

            #=========== Get the article ==========
            mh = MainHandler()

            #response is a dictionary!!
            response = mh.get_article(user_fbid)

            if len(response['article_link']) == 0:
                return JsonResponse({'message': 'could not retrieve article'}, status=400)

            response.update({'name': entry.name, 'propic': entry.propic_link})

            return JsonResponse(response, status=200)
        except:
            print("ahhh")
        return HttpResponse(status=204)

    


class InitView(APIView):
    #checks if this user needs to be initialized
    #/api/status
    def get(self, request):
        try: 
            entry = Users.objects.get(user_fbid=user_fbid)
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=204)
    #/api/init
    def post(self, request):

        #========= Save User to DB =========
        req = json.loads(request.body)
        access_token = req['token']
        user_id = req['user_id']
        size = str(req['size'])

        facebook = FacebookAPI(access_token)

        propic_link = facebook.get(link="/me/picture", params={"redirect": False, "width": size, "height": size})['data']['url']
        me = facebook.get(link="/me")
        name = me['name']

        newUser = Users(user_fbid=user_id, name=name, propic_link=propic_link)
        articles_list = {}
        newUser.articles = json.dumps(articles_list)
        newUser.save()

        #creates zip file for default model to save
        mainHandler = MainHandler()
        userSkipGramModel = PklModels()
        userSkipGramModel.user_fbid = user_id
        userSkipGramModel.pkl_model = mainHandler.getDefaultModel()
        userSkipGramModel.user_keywords = json.dumps(['government'])
        empty_file = open("empty","w+")
        empty_file.close()
        with zipfile.ZipFile("{0}_training_data.zip".format(user_id), "w") as myzip:
                myzip.write("empty")
        os.remove("empty") #remove temp files
        userSkipGramModel.text_corpus = File(open("{0}_training_data.zip".format(user_id))) 
        os.remove("{0}_training_data.zip".format(user_id))
        userSkipGramModel.save()
        #=========== Get the articles==========

        retriever = ArticleRetriever(user_id, facebook)
        response = retriever.return_articles()

        if (type(response) is str):
            return JsonResponse({'message': response}, status=400)

        response.update({'name': name, 'propic': propic_link})

        return JsonResponse(response, status=201)

class ArticlesView(APIView):
    mainHandler = MainHandler()
    #when asked for next article (one), frontend makes a post request,
    def get(self, request):
        '''
        get keywords, get an article
        check that the link isn't in the user dict, rating as 0
        add content to text corpus, call  normalizeParagraphs(), then remove_nonalpha() from webcralwer
        return the content
        '''
        user_id = request.GET.get('user_id')
        response = mainHandler.get_article(user_id)        
        return JsonResponse(response, status=200)
#TODO TEST
#when user rates an article,
    def post(self, request):
        req = json.loads(request.body)
        user_id = req['user_id']
        article_link = req['article_link']
        user_rating = req['user_rating']
        user_article_dict = Users.objects.get(user_fbid=user_id).articles
        jsonDec = json.decoder.JSONDecoder()
        decoded_user_article_dict = jsonDec.decode(user_article_dict)
        decoded_user_article_dict[article_link] = user_rating
        Users.objects.get(user_fbid=user_id).articles = decoded_user_article_dict
        Users.objects.get(user_fbid=user_id).save()
        return JsonResponse("Ok", status=200)
