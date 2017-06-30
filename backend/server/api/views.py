from .models import Users
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import json
from django.http import HttpResponse, JsonResponse
from open_facebook.api import FacebookAuthorization
from facebook_api_handler import FacebookAPI

class UsersView(APIView):
	serializer_class = UserSerializer

	def get(self, request):
		user_fbid = request.GET.get('user_ID')
		try:
			print(user_fbid)
			entry = Users.objects.get(user_fbid=user_fbid)
			response = {'name': entry.name, 'propic': entry.propic_link}
			return JsonResponse(response, status=200)
		except:
			print("ahhh")
			return HttpResponse(status=204)

	def post(self, request):
	    print("lol")
	    req = json.loads(request.body)
	    access_token = req['token']
	    user_id = req['user_ID']
	    size = str(req['size'])
	    
	    extended_token = FacebookAuthorization.extend_access_token(access_token)['access_token']
	    facebook = FacebookAPI(extended_token)
	    
	    propic_link = facebook.get(link="me/picture", params={"redirect": False, "width": size, "height": size})['data']['url']    
	    name = facebook.get(link="/me")['name']

	    newUser = Users(user_fbid=user_id, name=name, propic_link=propic_link)
	    newUser.save()

	    response = {'name': name, 'propic': propic_link}
	    return JsonResponse(response, status=201)
