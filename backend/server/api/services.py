from facebook_api_handler import FacebookAPI
from filter_set import FilterSetContainer
import math
import threading
import re
import sys
import os
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'modules')
sys.path.append(path)
from webcrawler import WebCrawler

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(path)
import main_handler

FilterSetContainer()

class ArticleRetriever(object):
    webcrawler = WebCrawler()
    userPageLimit = 25
    feedPostLimit = 50
    categories=['News & Media Website', 'Newspaper']
    page_limit = 5

    def __init__(self, user_id, facebook):
        self.user_id = user_id
        self.facebook = facebook
        self.liked_pages = []
        self.keywords = []
        self.content = []

    def returnArticles(self):
        mainHandler = MainHandler()
        keywords, content = self.get_likes()
        mainHandler.addKeywords(keywords, self.user_id)
        mainHandler.addTrainingData(content, self.user_id)

    def get_likes(self):    
        #========= Get Likes =========
            threads = []

            #== Get Liked Pages and Filter==

            res = self.facebook.get(link="/me/likes", params={"limit": self.userPageLimit})
            hasNextPage = True  
            while hasNextPage is True:
                thread = ThreadRunner(res, self.facebook, "category", self.liked_pages, self.keywords, self.content)
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
                threads.append(ThreadRunner(feed_res, self.facebook, "feed", self.liked_pages, self.keywords, self.content))

            #run the threads
            [thread.start() for thread in threads]
            [thread.join() for thread in threads]    

            print self.keywords
            print self.content

            if not self.keywords:
                #TODO return error
                pass    
            else:
                return self.keywords, self.content

#delegate most of the work to multithreading to speed things up 
class ThreadRunner(threading.Thread, LikesRetriever):
    def __init__(self, response, facebook, threadType, liked_pages, keywords, liked_posts):
        threading.Thread.__init__(self)
        self.response = response
        self.facebook = facebook
        self.threadType = threadType
        self.liked_pages = liked_pages
        self.keywords = keywords
        self.content = liked_posts
    
    def run(self):
        if self.threadType is "category":
            allLikes = self.response['data']

            #create list of ids to query
            idList = ''.join([page['id']+"," for page in allLikes])[:-1]
            response = self.facebook.get(link="/", params={"ids":idList}, fields='category')

            #check which pages are in the appropriate category
            for page_id in response:
                if response[page_id]['category'] in LikesRetriever.categories:
                    self.liked_pages.append(page_id)
        
        elif self.threadType is "feed":
            threads = []
            hasNextPage = True
            feedPageCount = 0

            #limit to page_limit of feed pages
            while feedPageCount <= LikesRetriever.page_limit and hasNextPage is True:
                #start threads for retrieving likes
                threads.append(ThreadRunner(self.response['data'], self.facebook, "likes", self.liked_pages, self.keywords, self.content))
                
                #get next pages and start new threads per feed page
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
            #get all likes
            likeIds = ''.join([post['id']+"," for post in self.response])[:-1]
            likes = self.facebook.get(link="/", params={"ids":likeIds}, fields='likes.summary(true).fields(name).limit(1),message,link')

            #check each post to see if the user has liked the post
            for post_id in likes:
                if likes[post_id]['likes']['summary']['has_liked']:
                    print "ayus"
                    if 'link' in likes[post_id]:
                        #get link content and filter
                        linkParagraphs = LikesRetriever.webcrawler.grabContent(likes[post_id]['link'].replace("\"", ''))      
                        for paragraph in linkParagraphs:
                            self.content.append(self.filterWords(paragraph))
                    #otherwise just filter the message body
                    self.keywords.append(self.filterWords(likes[post_id]['message']))

    '''
    Takes in a string and filters out common words using the pickled set
    '''
    def filterWords(self, text):
        #get only alphanumeric characters
        alnum = re.compile('([^\s\w]|_)+')
        alnumText = alnum.sub('', text).lower()
        print alnumText
        #filter
        words = alnumText.split(' ')
        for word in words:
            if word in FilterSetContainer.filtered_set:
                words.remove(word)
        return words                

    #workaround for now to get pageID from an API call response
    def extractPageID(self, link):
        link = link.replace(self.facebook.base_url + self.facebook.version + "/", "")
        link = link[0:link.index("/")]
        return link
