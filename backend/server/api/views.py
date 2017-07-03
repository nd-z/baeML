from .models import Users
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from open_facebook.api import FacebookAuthorization
from facebook_api_handler import FacebookAPI
import json
import threading

class UsersView(APIView):
    serializer_class = UserSerializer
    liked_pages = []
    categories=['News & Media Website', 'Newspaper']

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
        
        threads = []

        res = facebook.get(link="/me/likes")
        hasNextPage = True  
        while hasNextPage is True:
            thread = self.CategoryThreadRunner(res, facebook)
            threads.append(thread)
            if 'paging' in res:
                cursor_next = res['paging']['cursors']['after']
                res = facebook.get(link="/me/likes", params={"after" : cursor_next})
            else:
                hasNextPage = False
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()


        print(self.liked_pages)
        response = {'name': name, 'propic': propic_link}
        return JsonResponse(response, status=201)

    class CategoryThreadRunner(threading.Thread):
        def __init__(self, response, facebook):
            threading.Thread.__init__(self)
            self.response = response
            self.facebook = facebook
        
        def run(self):
            allLikes = self.response['data']
            for page in allLikes:
                page_id = page['id']
                page_info = self.facebook.get(link="/" + page_id, fields='category,id')['category']
                print(page_info)
                if page_info in UsersView.categories:
                    #TODO go thru all the pages and see what they've liked? seems EXTREMELY consuming --> multithreading?
                    UsersView.liked_pages.append(page_id)
                    





