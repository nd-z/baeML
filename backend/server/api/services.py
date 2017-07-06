from facebook_api_handler import FacebookAPI
import math
import threading

class LikesRetriever(object):
    userPageLimit = 25
    feedPostLimit = 100
    categories=['News & Media Website', 'Newspaper']
    page_limit = 3

    def __init__(self, user_id, name, facebook):
        self.user_id = user_id
        self.name = name
        self.facebook = facebook
        self.liked_pages = []
        self.liked_posts = []

    def get_likes(self):    
        #========= Get Likes =========
            user_dict = {"id": self.user_id, "name": self.name}
            threads = []

            #== Get Liked Pages and Filter==

            res = self.facebook.get(link="/me/likes", params={"limit": self.userPageLimit})
            hasNextPage = True  
            while hasNextPage is True:
                thread = ThreadRunner(res, self.facebook, "category", None, self.liked_pages, self.liked_posts)
                threads.append(thread)
                if 'paging' in res:
                    cursor_next = res['paging']['cursors']['after']
                    res = self.facebook.get(link="/me/likes", params={"after" : cursor_next, "limit": self.userPageLimit})
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
                feed_res = self.facebook.get(link="/" + page + "/feed", params={"limit":self.feedPostLimit})
                threads.append(ThreadRunner(feed_res, self.facebook, "feed", user_dict, self.liked_pages, self.liked_posts))

            #run the threads
            [thread.start() for thread in threads]
            [thread.join() for thread in threads]    

            print self.liked_posts

            if not self.liked_posts:
                #TODO return error
                pass    
            
            #TODO get stuff from ML module with likes info

class ThreadRunner(threading.Thread, LikesRetriever):
    def __init__(self, response, facebook, threadType, user_dict, liked_pages, liked_posts):
        threading.Thread.__init__(self)
        self.response = response
        self.facebook = facebook
        self.threadType = threadType
        self.user_dict = user_dict
        self.liked_pages = liked_pages
        self.liked_posts = liked_posts
    
    def run(self):
        if self.threadType is "category":
            allLikes = self.response['data']
            for page in allLikes:
                page_id = page['id']
                page_info = self.facebook.get(link="/" + page_id, fields='category,id')['category']
                if page_info in LikesRetriever.categories:
                    #TODO go thru all the pages and see what they've liked? seems EXTREMELY consuming --> multithreading?
                    self.liked_pages.append(page_id)
        elif self.threadType is "feed":
            threads = []
            hasNextPage = True
            feedPageCount = 0
            while feedPageCount <= LikesRetriever.page_limit and hasNextPage is True:
                threads.append(ThreadRunner(self.response['data'], self.facebook, "likes", self.user_dict, self.liked_pages, self.liked_posts))
                if 'paging' in self.response:
                    page_id = self.extractPageID(self.response['paging']['next'])
                    cursor_next = self.response['paging']['cursors']['after']
                    self.response = self.facebook.get(link="/" + page_id +"/feed", params={"after" : cursor_next, "limit": LikesRetriever.userPageLimit})
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
