from django.http import HttpResponse, JsonResponse
from open_facebook.api import FacebookAuthorization
from facebook_api_handler import FacebookAPI

import json

#testing, should just return 201 to every call to this
def hello(self):
	print("lol")
	return HttpResponse(status=201)

#TODO implement the logic behind these
def login(self):
	return HttpResponse(status=404)

def login_init(request):
    req = json.loads(request.body)
    access_token = req['token']
    user_id = req['user_ID']
    size = str(req['size'])
    #TODO - put user_id and extended access token in database
    extended_token = FacebookAuthorization.extend_access_token(access_token)['access_token']
    facebook = FacebookAPI(extended_token)
    propic_link = facebook.get(link="me/picture", params={"redirect": False, "width": size, "height": size})['data']['url']    
    name = facebook.get(link="/me")['name']
    response = {'name': name, 'propic': propic_link}
    return JsonResponse(response)
