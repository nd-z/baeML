from .models import Users
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from open_facebook.api import FacebookAuthorization
from facebook_api_handler import FacebookAPI
import json
import math
import threading

class UsersView(APIView):
    serializer_class = UserSerializer
    liked_pages = []
    liked_posts = []
    userPageLimit = 25
    feedPostLimit = 100
    categories=['News & Media Website', 'Newspaper']
    page_limit = 3

    #/login
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
        self.liked_pages[:] = []
        self.liked_posts[:] = []
        
        #========= Save User to DB =========

        req = json.loads(request.body)
        access_token = req['token']
        user_id = req['user_ID']
        size = str(req['size'])

        extended_token = FacebookAuthorization.extend_access_token(access_token)['access_token']
        facebook = FacebookAPI(extended_token)
        
        propic_link = facebook.get(link="/me/picture", params={"redirect": False, "width": size, "height": size})['data']['url']    
        me = facebook.get(link="/me")
        name = me['name']

        newUser = Users(user_fbid=user_id, name=name, propic_link=propic_link)
        newUser.save()
        
        #========= Get Likes =========
        user_dict = {"id": user_id, "name": name}
        threads = []

        #== Get Liked Pages and Filter==

        res = facebook.get(link="/me/likes", params={"limit": self.userPageLimit})
        hasNextPage = True  
        while hasNextPage is True:
            thread = ThreadRunner(res, facebook, "category", None)
            threads.append(thread)
            if 'paging' in res:
                cursor_next = res['paging']['cursors']['after']
                res = facebook.get(link="/me/likes", params={"after" : cursor_next, "limit": self.userPageLimit})
            else:
                hasNextPage = False
        
        #run the threads
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        #debug
        print(self.liked_pages)

        threads[:] = []

        #== Get Feeds for each page and get Liked Posts==

        for page in self.liked_pages:
            feed_res = facebook.get(link="/" + page + "/feed", params={"limit":self.feedPostLimit})
            threads.append(ThreadRunner(feed_res, facebook, "feed", user_dict))

        #run the threads
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]    

        print self.liked_posts

        #TODO get stuff from ML module with likes info

        response = {'name': name, 'propic': propic_link}
        return JsonResponse(response, status=201)

class ThreadRunner(threading.Thread, UsersView):
    def __init__(self, response, facebook, threadType, user_dict):
        threading.Thread.__init__(self)
        self.response = response
        self.facebook = facebook
        self.threadType = threadType
        self.user_dict = user_dict
    
    def run(self):
        if self.threadType is "category":
            allLikes = self.response['data']
            for page in allLikes:
                page_id = page['id']
                page_info = self.facebook.get(link="/" + page_id, fields='category,id')['category']
                if page_info in UsersView.categories:
                    #TODO go thru all the pages and see what they've liked? seems EXTREMELY consuming --> multithreading?
                    self.liked_pages.append(page_id)
        elif self.threadType is "feed":
            threads = []
            hasNextPage = True
            feedPageCount = 0
            while feedPageCount <= UsersView.page_limit and hasNextPage is True:
                threads.append(ThreadRunner(self.response['data'], self.facebook, "likes", self.user_dict))
                if 'paging' in self.response:
                    page_id = self.extractPageID(self.response['paging']['next'])
                    cursor_next = self.response['paging']['cursors']['after']
                    self.response = self.facebook.get(link="/" + page_id +"/feed", params={"after" : cursor_next, "limit": UsersView.userPageLimit})
                else: 
                    hasNextPage = False
                feedPageCount+=1
            [thread.start() for thread in threads]
            [thread.join() for thread in threads]     

        elif self.threadType is "likes":
            for post in self.response:
                likes = self.facebook.get(link="/"+post['id'] + "/likes", params={"limit":1000})['data']
                if self.user_dict in likes:
                    post = self.facebook.get(link="/" + post['id'], fields='link,message')
                    if 'link' in post:
                        self.liked_posts.append({"message":post['message'], "link":post['link']})
                    else:    
                        self.liked_posts.append(post['message'])

    #workaround for now to get pageID
    def extractPageID(self, link):
        link = link.replace(self.facebook.base_url + self.facebook.version + "/", "")
        link = link[0:link.index("/")]
        return link
                




