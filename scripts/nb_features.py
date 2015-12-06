# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 13:26:44 2015

@author: snoran
"""

import nltk;
from tweetLoader import loadNonRacistTweets, loadRacistTweets
from sklearn.svm import LinearSVC

from sklearn.feature_extraction.text import TfidfVectorizer

def getWords(tweets):
    words = []
    for tweet in tweets:
        for w in tweet[0]:
            words.append(w.lower())
    return words

#http://stackoverflow.com/questions/14003291/n-grams-with-naive-bayes-classifier
def bigramFeatures (tweetString):
    tweetString = tweetString.lower()
    bigramFeatureVector = []
    for item in nltk.bigrams(tweetString.split()):
        bigramFeatureVector.append(' '.join(item))
    return bigramFeatureVector

'''
    I used code from
    http://www.nltk.org/book/ch06.html
    for this

'''
#if __name__ == "__main__" :
print("NB start");
N = 4800
train_size = 3600
racistTweets = loadRacistTweets(numTweets=N);
normalTweets = loadNonRacistTweets(numTweets=N);
allTweets = racistTweets + normalTweets

print("Number of racist tweets: {}.".format(len(racistTweets)));
print("Number of normal tweets: {}.".format(len(normalTweets)));

trainR = racistTweets[:train_size];
testR = racistTweets[train_size:];

trainN = normalTweets[0:train_size];
testN = normalTweets[train_size:];

trainTweets = trainR + trainN;
testTweets = testR + testN;

trainWords = getWords(trainTweets);
wordFreqs = nltk.FreqDist(w for w in trainWords);

# plot of most common words
wordFreqs.plot(50, cumulative=False);

#wordFeatures = list(wordFreqs)[:1000];

tfidf = TfidfVectorizer(tokenizer=nltk.word_tokenize, stop_words='english')
tfs = tfidf.fit([' '.join(trainTweets[k][0]) for k in range(2*train_size)])
feature_names = tfidf.get_feature_names()

def getFeatures(document) :
    #documentWords = set(document);
    features = {};
    #for pair in bigramFeatures(' '.join(documentWords)):
    #    features['contains_pair({})'.format(pair)] = 1
    #for word in wordFeatures:
    #    features['contains({})'.format(word)] = (word in documentWords);
    response = tfidf.transform([' '.join(document).lower()])
    for col in response.nonzero()[1]:
        try:
            features['tf-idf-index({})'.format(feature_names[col])] = response[0, col]
        except:
            pass
    return features


trainFeats = [(getFeatures(d), c) for (d,c) in trainTweets];
testFeats = [(getFeatures(d), c) for (d,c) in testTweets];

print(trainFeats[-2])
print(testFeats[-2])

svmClass = nltk.classify.SklearnClassifier(LinearSVC());
svmClass.train(trainFeats);

print("----------------------");
print("SVM Classifier");
print(nltk.classify.accuracy(svmClass, testFeats));

#64.14% on bigram features - BoW
#73% on unigram features - BoW
#81.45% using both BoW features
