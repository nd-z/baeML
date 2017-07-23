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
from main_handler import MainHandler

FilterSetContainer()


class ArticleRetriever(object):
    webcrawler = WebCrawler()

    #constants
    userPageLimit = 25
    feedPostLimit = 50
    categories=['News & Media Website', 'Newspaper']
    page_limit = 5

    def __init__(self, user_id, facebook):
        self.user_id = user_id
        self.facebook = facebook
        self.liked_pages = []

        #keywords = individual words 
        #content = coherent paragraphs
        self.keywords = []
        self.content = []

    #TODO finish this
    def return_articles(self):
        self.get_likes()
        mainHandler = MainHandler()
        mainHandler.addKeywords(self.keywords, self.user_id)
        mainHandler.addTrainingData(self.content, self.user_id)
        response = mainHandler.get_article(self.user_id)
        print 'sending articles' 
        return response

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

            threads[:] = []

            #== Get Feeds for each page and get Liked Posts==

            for page in self.liked_pages:
                feed_res = self.facebook.get(link="/" + page + "/feed", params={"limit":self.feedPostLimit})
                threads.append(ThreadRunner(feed_res, self.facebook, "feed", self.liked_pages, self.keywords, self.content))

            #run the threads
            [thread.start() for thread in threads]
            [thread.join() for thread in threads]    

            #debug
            print self.keywords
            print self.content

            if not self.keywords: #user has not liked anything recently
                self.keywords.append("government")
                return self.keywords, self.content
            else:
                print "'likes retrieved'"
                return self.keywords, self.content

#delegate most of the work to multithreading to speed things up 
class ThreadRunner(threading.Thread, ArticleRetriever):
    def __init__(self, response, facebook, threadType, liked_pages, keywords, liked_posts):
        threading.Thread.__init__(self)
        self.response = response
        self.facebook = facebook
        self.threadType = threadType
        self.liked_pages = liked_pages
        self.keywords = keywords
        self.content = liked_posts
    
    def run(self):
        #checks for relevant liked pages (if the page's category is in the specified categories)
        if self.threadType is "category":
            allLikes = self.response['data']

            #create list of ids to query
            idList = ''.join([page['id']+"," for page in allLikes])[:-1]
            response = self.facebook.get(link="/", params={"ids":idList}, fields='category')

            #check which pages are in the appropriate category
            for page_id in response:
                if response[page_id]['category'] in ArticleRetriever.categories:
                    self.liked_pages.append(page_id)
        
        #spawns threads to scrape like data from each page of the feed
        elif self.threadType is "feed":
            threads = []
            hasNextPage = True
            feedPageCount = 0

            #limit to page_limit of feed pages
            while feedPageCount <= ArticleRetriever.page_limit and hasNextPage is True:
                #start threads for retrieving likes
                threads.append(ThreadRunner(self.response['data'], self.facebook, "likes", self.liked_pages, self.keywords, self.content))
                
                #get next pages and start new threads per feed page
                if 'paging' in self.response:
                    page_id = self.extractPageID(self.response['paging']['next'])
                    cursor_next = self.response['paging']['cursors']['after']
                    self.response = self.facebook.get(link="/" + page_id +"/feed", params={"after" : cursor_next, "limit": ArticleRetriever.userPageLimit})
                else: 
                    hasNextPage = False
                feedPageCount+=1

            [thread.start() for thread in threads]
            [thread.join() for thread in threads]     

        #checks every post on the feed page they are given to see if user has liked the post
        #and then adds the keywords to the array
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
                        linkParagraphs = ArticleRetriever.webcrawler.grabContent(likes[post_id]['link'].replace("\"", ''))      
                        for paragraph in linkParagraphs:
                            self.content.append(paragraph)
                            self.keywords.extend(ThreadRunner.filterWords(paragraph))
                        title = WebCrawler.grabTitle(likes[post_id]['link'].replace("\"", ''))
                        self.keywords.extend(ThreadRunner.filterWords(title))

    '''
    Takes in a string and filters out common words using the pickled set
    '''
    @staticmethod
    def filterWords(text):
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
