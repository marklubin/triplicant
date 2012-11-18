"""
FlickrExtractor.py : A class with methods for dealing with data from the Flickr
API and processing data.
"""

class FlickrExtractor:
    def __init__(self):
        pass

    """Fetch new unique data from flickr and add to db"""
    def flickFetch(self, limit):
        pass

    """use mean shift clustering to find locations, update db with locations
    and their member photos"""
    def locationMake(self,bandwidth,noise):
        pass

    """compute each user path and the markov model probabilities, store in db"""
    def computeUserTripsAndProbablities(self):
        pass

    """compute the importance vector"""
    def solve():
        pass

if __name__ == '__main__':
    pass