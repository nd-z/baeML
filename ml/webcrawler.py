import re
import httplib
import urllib2
from urlparse import urlparse
import BeautifulSoup

class WebCrawler(object):
    def __init__(self):
        self.regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def isValidUrl(self, url):
        if self.regex.match(url) is not None:
            return True;
        return False

    def crawl(self, SeedUrl):
        tocrawl=[SeedUrl]
        links_on_page=[]
        page=tocrawl.pop()
        #print 'Crawled:'+page
        pagesource=urllib2.urlopen(page)
        s=pagesource.read()
        soup=BeautifulSoup.BeautifulSoup(s)
        links=soup.findAll('a',href=True)   

        for l in links:
            if self.isValidUrl(l['href']):
                links_on_page.append(l['href'])

        return links_on_page

        ''' this was for crawling other links
        while tocrawl:
            page=tocrawl.pop()
            print 'Crawled:'+page
            pagesource=urllib2.urlopen(page)
            s=pagesource.read()
            soup=BeautifulSoup.BeautifulSoup(s)
            links=soup.findAll('a',href=True)        
            if page not in crawled:
                for l in links:
                    if self.isValidUrl(l['href']):
                        tocrawl.append(l['href'])
                crawled.append(page)   
        return crawled
        '''

crawler = WebCrawler()
links = crawler.crawl('https://www.nytimes.com')
print links