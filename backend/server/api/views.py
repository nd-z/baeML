from .models import Users, PklModels
from .services import ArticleRetriever
from .services import ThreadRunner
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from facebook_api_handler import FacebookAPI
import json
import sys
import os
import zipfile
import threading
from django.core.files import File
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(path)
from main_handler import MainHandler
from webcrawler import WebCrawler

class UsersView(APIView):
    serializer_class = UserSerializer
    mainHandler = MainHandler()

    #/api/login
    def get(self, request):

        #commented out to test initializing user
        user_fbid = request.GET.get('user_ID')
        try:
            #=========== Get the article ==========
            #response is a dictionary!!
            response = self.mainHandler.get_article(user_fbid)
            print('didnt break getting a response; here is the response')
            print(response)

            if len(response['article_link']) == 0:
                return JsonResponse({'message': 'could not retrieve article'}, status=400)

            entry = Users.objects.get(user_fbid=user_fbid)
            response.update({'name': entry.name, 'propic': entry.propic_link})

            return JsonResponse(response, status=200)
        except:
            print("ahhh")
        return HttpResponse(status=404)

class InitView(APIView):

    serializer_class = UserSerializer
    #checks if this user needs to be initialized
    #/api/status
    mainHandler = MainHandler()

    def get(self, request):
        try: 
            user_fbid = request.GET.get('user_ID')
            entry = Users.objects.get(user_fbid=user_fbid)
            isComplete = entry.init_complete
            if isComplete:
                return HttpResponse(status=200)
            return HttpResponse(status=204)
        except:
            return HttpResponse(status=204)

    #/api/init
    def post(self, request):
        thread = InitView.InitThread(self.initialize, request)
        thread.start()
        return HttpResponse(status=204)

    def initialize(self, request):
        #Save user to the DB
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

        #Train the model, creates zip file for default model to save
        userSkipGramModel = PklModels()
        userSkipGramModel.user_fbid = user_id
        userSkipGramModel.pkl_model = self.mainHandler.getDefaultModel()
        userSkipGramModel.user_keywords = json.dumps(['government'])
        empty_file = open("empty","w+")
        empty_file.close()
        with zipfile.ZipFile("{0}_training_data.zip".format(user_id), "w") as myzip:
                myzip.write("empty")
        os.remove("empty") #remove temp files
        userSkipGramModel.text_corpus = File(open("{0}_training_data.zip".format(user_id))) 
        os.remove("{0}_training_data.zip".format(user_id))
        userSkipGramModel.save()

        #Initialize user's likes and content
        retriever = ArticleRetriever(user_id, facebook)
        retriever.initialize()

        #init has completed, reflect this in the DB
        user = Users.objects.get(user_fbid=user_id)
        user.init_complete = True
        user.save()

    class InitThread(threading.Thread):
        def __init__(self, target, request):
            threading.Thread.__init__(self)
            self.target = target
            self.request = request

        def run(self):
            self.target(self.request)

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
        response = self.mainHandler.get_article(user_id)        
        return JsonResponse(response, status=200, safe=False)
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
        user = Users.objects.get(user_fbid=user_id)
        user.articles = json.dumps(decoded_user_article_dict)
        user.save()

        article_title = WebCrawler.grabTitle(article_link)
        new_keywords_list = ThreadRunner.filterWords(article_title) #process keywords in title
        self.mainHandler.addKeywords(new_keywords_list, user_id)
        return JsonResponse({'':''}, status=200)
