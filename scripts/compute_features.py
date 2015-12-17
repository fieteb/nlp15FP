# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 16:30:08 2015

@author: snoran
"""

import nltk
from preprocessing import preprocess
from tweetLoader import loadNonRacistTweets
from sklearn.feature_extraction.text import TfidfVectorizer

class FeatureExtractor():
    '''
    This class handles the feature extraction of tweets. When instantiating
    an instance of FeatureExtractor, provide a list of names which refer
    to the features of interest, i.e.

    FeatureExtractor(['TF_IDF', 'bigram'])

    if you are interested only in TF-IDF and bigram BoW features.
    '''

    #IDs for various features:
    TF_IDF = 'TF_IDF'
    UNIGRAM = 'unigram'
    BIGRAM = 'bigram'

    def __init__(self, features) :
        self.tfidf = None
        self.tfs = None
        self.features = features

    def get_unigram_features (self, tokens):
        '''
        Returns the unigram bag-of-words features for a given string.
        '''
        features = {}
        for word in tokens:
            features['contains({})'.format(word)] = 1
        return features

    def get_bigram_features (self, tokens):
        '''
        Returns the bigram bag-of-words features for a given string. See
        http://stackoverflow.com/questions/14003291/n-grams-with-naive-bayes-classifier
        '''
        tweetString = ' '.join(tokens).lower()
        bigrams = []
        features = {}
        for item in nltk.bigrams(tweetString.split()):
            bigrams.append(' '.join(item))
        for pair in bigrams:
            features['contains_pair({})'.format(pair)] = 1
        return features

    def train_TF_IDF(self, trainTweets):
        '''
        Computes the matrix of term-frequency inverse document frequency
        values from the given collection of tweets

        '''
        #compute TF-IDF features:
        self.tfidf = TfidfVectorizer(tokenizer=nltk.word_tokenize, stop_words='english')
        self.tfs = self.tfidf.fit([' '.join(trainTweets[k][0]) for k in range(len(trainTweets))])
        self.feature_names = self.tfidf.get_feature_names()

    def get_TF_IDF_feature_vector(self, tokens):
        '''
        Returns the term-frequency inverse document frequency score of
        the given tweet, where tokens in a list of words contained in
        the tweet.
        '''
        features = {}
        response = self.tfidf.transform([' '.join(tokens).lower()])
        for col in response.nonzero()[1]:
            try:
                features['tf-idf-index({})'.format(self.feature_names[col])] = response[0, col]
            except:
                pass
        return features

    def get_feature_vector(self, tokens) :
        '''
        Returns the feature vector of the given tweet, defined by the
        tokens variable, which is a list of the words contained in the
        tweet.
        '''
        features = {}
        if FeatureExtractor.TF_IDF in self.features:
            features.update(self.get_TF_IDF_feature_vector(tokens))
        if FeatureExtractor.UNIGRAM in self.features:
            features.update(self.get_unigram_features(tokens))
        if FeatureExtractor.BIGRAM in self.features:
            features.update(self.get_bigram_features(tokens))
        return features


if __name__ == "__main__":
    '''
    This is an example to see how to use this class
    '''

    #construct a tiny set of tweets
    tweets = loadNonRacistTweets(numTweets = 10)

    print("First tweet: {}".format(' '.join(tweets[0][0])))

    #preprocess the tweets to filter punctuation and common words
    preprocessedTweets = [(preprocess(tweet),label) for (tweet,label) in tweets]

    #extract bigram features only
    bigramFeatureExtractor = FeatureExtractor([FeatureExtractor.BIGRAM])
    #get_feature_vector() requires the tweet without the label
    bigramFeatures = bigramFeatureExtractor.get_feature_vector(preprocessedTweets[0][0])
    print("\nBigram Feature Vector:\n {}".format(bigramFeatures))

    #extract unigram and TF_IDF features - the TF_IDF features demonstrates the usefulness of having a class
    unigramTDIDFFeatureExtractor = FeatureExtractor([FeatureExtractor.UNIGRAM, FeatureExtractor.TF_IDF])
    unigramTDIDFFeatureExtractor.train_TF_IDF(preprocessedTweets)
    unigramTDFIDFFeatures = unigramTDIDFFeatureExtractor.get_feature_vector(preprocessedTweets[0][0])
    print("\nUnigram and TF-IDF Feature Vector:\n {}".format(unigramTDFIDFFeatures))