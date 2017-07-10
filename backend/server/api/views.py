from .models import Users, PklModels
from .services import LikesRetriever
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from facebook_api_handler import FacebookAPI
import json
from .. import main_handler

class UsersView(APIView):
    serializer_class = UserSerializer

    #/api/login
    def get(self, request):

        #commented out to test initializing user

        # user_fbid = request.GET.get('user_ID')
        # try:
        #   print(user_fbid)
        #   entry = Users.objects.get(user_fbid=user_fbid)
        #   response = {'name': z.name, 'propic': entry.propic_link}
        #   return JsonResponse(response, status=200)
        # except:
        #   print("ahhh")
        return HttpResponse(status=204)

    #/api/init
    def post(self, request):
        #========= Save User to DB =========

        req = json.loads(request.body)
        access_token = req['token']
        user_id = req['user_ID']
        size = str(req['size'])

        facebook = FacebookAPI(access_token)

        propic_link = facebook.get(link="/me/picture", params={"redirect": False, "width": size, "height": size})['data']['url']
        me = facebook.get(link="/me")
        name = me['name']

        newUser = Users(user_fbid=user_id, name=name, propic_link=propic_link)
        newUser.save()

        #get default skigram model for user
        mh = main_handler.MainHandler()
        userSkipGramModel = PklModels()
        userSkipGramModel.user_fbid = user_id
        userSkipGramModel.pkl_model = mh.getDefaultModel()
        userSkipGramModel.user_keywords = []
        userSkipGramModel.save()

        #Retrieve likes and add keywords, assumes keywords are in a list already
        helper = LikesRetriever(user_id, facebook)
        mh.addKeywords(helper.getLikes()['keyword_list'], user_id)
        mh.addTrainingData(helper.getLikes()['training_data'], user_id)


        response = {'name': name, 'propic': propic_link}
        return JsonResponse(response, status=201)
