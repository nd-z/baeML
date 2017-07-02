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

	categories=['News & Media Website', 'Newspaper']

	def get(self, request):

		#commented out to test initializing user

		# user_fbid = request.GET.get('user_ID')
		# try:
		# 	print(user_fbid)
		# 	entry = Users.objects.get(user_fbid=user_fbid)
		# 	response = {'name': z.name, 'propic': entry.propic_link}
		# 	return JsonResponse(response, status=200)
		# except:
		# 	print("ahhh")
		return HttpResponse(status=204)

	def post(self, request):
	    print("lol")
	    req = json.loads(request.body)
	    access_token = req['token']
	    user_id = req['user_ID']
	    size = str(req['size'])
	    
	    extended_token = FacebookAuthorization.extend_access_token(access_token)['access_token']
	    facebook = FacebookAPI(extended_token)
	    
	    propic_link = facebook.get(link="/me/picture", params={"redirect": False, "width": size, "height": size})['data']['url']    
	    name = facebook.get(link="/me")['name']

	    newUser = Users(user_fbid=user_id, name=name, propic_link=propic_link)
	    newUser.save()

	    #TODO set up getting the likes and feeding to ML 
	    
	    res = facebook.get(link="/me/likes", params={"limit": 25})
	    
	    liked_pages = []

	    hasNextPage = True	
	    while hasNextPage is True:
		    allLikes = res['data']
		    for page in allLikes:
		    	page_id = page['id']
		    	page_info = facebook.get(link="/" + page_id, fields='category,id')['category']
		    	if page_info in self.categories:
		    		#TODO go thru all the pages and see what they've liked? seems EXTREMELY consuming --> multithreading?
		    		liked_pages.append(page_id)
		    		print(page_info)
		    if 'paging' in res:
		    	cursor_next = res['paging']['cursors']['after']
		    	res = facebook.get(link="/me/likes", params={"limit": 25, "after" : cursor_next})
		    else:
		    	hasNextPage = False

	    response = {'name': name, 'propic': propic_link}
	    return JsonResponse(response, status=201)
