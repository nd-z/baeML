import re
import ssl
import httplib
import urllib2
from urlparse import urlparse
import BeautifulSoup
import unicodedata


class WebCrawler(object):
    def __init__(self):
        self.regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def grabContent(self, url):
        req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        pagesource = urllib2.urlopen(req, context=context)
        s = pagesource.read()
        soup = BeautifulSoup.BeautifulSoup(s)
        
        #remove style components; step 1 of cleanup
        for i in soup.findAll(['script', 'style']):
            i.extract()
    
        soup.prettify('UTF-8')
        
        unprocessedParagraphs = soup.findAll('p')
        
        #clean out tags
        paragraphs = []
        for p in unprocessedParagraphs:
            processedParagraph = re.sub(r'<.*?>', '', unicode(p));
            
            #check that string is not empty
            if processedParagraph and not processedParagraph == 'None':
                paragraphs.append(processedParagraph)
        pagesource.close()
        return paragraphs
    
    @staticmethod
    def grabTitle(url):
        req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})

        pagesource = urllib2.urlopen(req)
        s = pagesource.read()
        soup = BeautifulSoup.BeautifulSoup(s)

        return soup.title.string

    def isValidUrl(self, url):
        if self.regex.match(url) is not None:
            return True;
        return False

    def crawl(self, SeedUrl, keywords):
        links_on_page = []
        req = urllib2.Request(SeedUrl, headers={'User-Agent' : "Magic Browser"}) 

        pagesource = urllib2.urlopen(req)
        s = pagesource.read()
        soup = BeautifulSoup.BeautifulSoup(s)
        links = soup.findAll('a',href=True)
        #print links 

        for l in links:
            skiplink = False

            for word in keywords:
                uni_l = unicode(l)
                uni_word = unicode(word)
                if uni_l.find(uni_word) == -1:
                    #print('no match')
                    skiplink = True
                    break

            if skiplink==True:
                skiplink = False
                continue
            else:
                links_on_page.append(l['href'])

        ret = []
        for l in links_on_page:
            if self.isValidUrl(l):
                ret.append(l)

        return ret

    #normalizes unicode strings into plain ascii
    @staticmethod
    def normalizeParagraphs(unicodeStrings):
        normalized = []

        for unicodeStr in unicodeStrings:
            tempStr = unicodedata.normalize('NFKD', unicodeStr).encode('ascii', 'ignore') #normalize to ascii
            normalized.append(tempStr)

        return normalized

    #replaces all instances of non-alpha characters with spaces
    #normalize first with normalizeParagraphs()!
    @staticmethod
    def replace_nonalpha(norm_paragraphs):
        check = re.compile('[^a-zA-Z]')
        alpha_par = []

        for paragraph in norm_paragraphs:
            paragraph = check.sub(' ', paragraph)
            paragraph = re.sub('\s+', ' ', paragraph)
            paragraph = paragraph.strip()
            alpha_par.append(paragraph)

        return alpha_par

    #method for doing full conversion and filtering of crawled content
    @staticmethod
    def filter_content(unfiltered_content):
        #run normalization
        normalized = WebCrawler.normalizeParagraphs(unfiltered_content)

        #filter out any string that does not contain at least 2 sentences with +5 words
        filter = re.compile(r"(((\b[a-zA-Z]+\b)[^a-zA-Z.?!]+){4,}(\b[a-zA-Z]+\b)[.?!])+")

        filtered = []

        for paragraph in normalized:
            if(filter.match(paragraph)):
                filtered.append(paragraph)

        #strip nonalpha characters
        filtered = WebCrawler.replace_nonalpha(filtered)

        return filtered

'''
crawler = WebCrawler()
keywords = ['global', 'warming']
links = crawler.crawl('http://www.bing.com/search?q=global+warming&go=Submit&qs=bs&form=QBLH', keywords)
#print links
paragraphs = crawler.grabContent(links[3])

print WebCrawler.filter_content(paragraphs)
print crawler.grabTitle(links[3])
'''