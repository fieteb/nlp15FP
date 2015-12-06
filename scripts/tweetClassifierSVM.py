# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 13:26:44 2015

@author: snoran
"""

import nltk;
from tweetLoader import loadNonRacistTweets, loadRacistTweets
from sklearn.svm import LinearSVC
from preprocessing import nbPreprocess
from compute_features import FeatureExtractor

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

print("NB start");

#number of  racist tweets
numTrainR = 1500;
numTestR = 500;

#number of normal tweets
numTrainN = 5000;
numTestN = 2000;

#load raw tweets:
rawRacistTweets = loadRacistTweets(numTweets = numTrainR + numTestR, excludeJokes=True)
rawNormalTweets = loadNonRacistTweets(numTweets= numTrainN + numTestN)
rawTweets = rawRacistTweets + rawNormalTweets

#pre-process tweets (i.e. remove certain words):
racistTweets = [(nbPreprocess(d), c) for (d, c) in rawRacistTweets];
normalTweets = [(nbPreprocess(d), c) for (d, c) in rawNormalTweets];
allTweets = racistTweets + normalTweets

print("Number of racist tweets: {}.".format(len(racistTweets)));
print("Number of normal tweets: {}.".format(len(normalTweets)));

#split into train/test sets
trainR = racistTweets[0:numTrainR];
testR = racistTweets[numTrainR:numTrainR + numTestR];

trainN = normalTweets[0:numTrainN];
testN = normalTweets[numTrainN:numTrainN + numTestN];

#combine racist/non-racist tweets into single train/test datasets
trainTweets = trainR + trainN;
testTweets = testR + testN;

#get word frequencies
trainWords = getWords(trainTweets);
wordFreqs = nltk.FreqDist(w for w in trainWords);

# plot of most common words
#wordFreqs.plot(50, cumulative=False);

featureExtractor = FeatureExtractor()

featureExtractor.train_TF_IDF(trainTweets)

#compute training & testing features
trainFeats = [(featureExtractor.getFeatureVector(d), c) for (d,c) in trainTweets];
testFeats = [(featureExtractor.getFeatureVector(d), c) for (d,c) in testTweets];

print(trainFeats[-2])
print(testFeats[-2])

svmClass = nltk.classify.SklearnClassifier(LinearSVC());
svmClass.train(trainFeats);

print("----------------------");
print("SVM Classifier");
print(nltk.classify.accuracy(svmClass, testFeats));

# Incorrect Classifications:
# TODO: Compute precision/recall
incorrect = []
for i in range(numTestN):
    if svmClass.classify(testFeats[i][0]) != testTweets[i][1]:
        incorrect.append(rawTweets[numTrainN+i][0])
