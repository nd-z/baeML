import os
import cPickle

class FilterSetContainer(object):
    filtered_set = {}

    def __init__(self):
        filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',)
        filtered_array = cPickle.load(open(filePath + "/filter_words.pkl", "rb"))
        FilterSetContainer.filtered_set = set(filtered_array)

    def getFilteredSet():
        return FilterSetContainer.filtered_set