from open_facebook.api import FacebookConnection
from django.utils.http import urlencode
from django.http import QueryDict

class FacebookAPI(object):

    version = "v2.9"
    base_url = 'https://graph.facebook.com/'


    def __init__(self, token):
        self.access_token = token
    '''
        TODO doc this
    '''
    def get(self, link, params=None, fields=None):
        query_dict = QueryDict('', True)
        if params != None:
            query_dict.update(params)
        if fields != None:
            query.appendlist('fields', fields)
        query_dict['access_token'] = self.access_token     
        url = self.base_url + link + "?" + query_dict.urlencode()
        print(url)
        return self.request(url)

    def request(self, url):
        return FacebookConnection._request(url=url)