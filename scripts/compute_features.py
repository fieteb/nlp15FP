# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 16:30:08 2015

@author: snoran
"""

import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

class FeatureExtractor():
    def __init__(self) :
        self.tfidf = None
        self.tfs = None
        self.featureNames = []

    def train_TF_IDF(self, trainTweets):
        #compute TF-IDF features:
        self.tfidf = TfidfVectorizer(tokenizer=nltk.word_tokenize, stop_words='english')
        self.tfs = self.tfidf.fit([' '.join(trainTweets[k][0]) for k in range(len(trainTweets))])
        self.feature_names = self.tfidf.get_feature_names()

    def getFeatureVector(self, tweet_words) :
        '''
        Returns the feature vector of each tweet, where tweet_words is a list of
        words contained in the tweet.
        '''
        features = {};
        #for pair in bigramFeatures(' '.join(documentWords)):
        #    features['contains_pair({})'.format(pair)] = 1
        #for word in wordFeatures:
        #    features['contains({})'.format(word)] = (word in documentWords);
        response = self.tfidf.transform([' '.join(tweet_words).lower()])
        for col in response.nonzero()[1]:
            try:
                features['tf-idf-index({})'.format(self.feature_names[col])] = response[0, col]
            except:
                pass
        return features