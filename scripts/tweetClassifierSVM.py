# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 13:26:44 2015

@author: snoran
"""

#%% --------------------------------------------------------------------
#
#                             Imports
#
# ----------------------------------------------------------------------

from __future__ import division

import nltk;
from tweetLoader import loadNonRacistTweets, loadRacistTweets
from sklearn.svm import LinearSVC
from sklearn import metrics
from preprocessing import preprocess
from compute_features import FeatureExtractor
from time import time
from argparse import ArgumentParser
import numpy as np

#%% --------------------------------------------------------------------
#
#                             Main Code
#
# ----------------------------------------------------------------------

def precision_recall_fscore(confusion_matrix, class_index):
	precision = confusion_matrix[class_index,class_index]/sum(confusion_matrix[:,class_index])
	recall = confusion_matrix[class_index,class_index]/sum(confusion_matrix[class_index,:])
	fscore = 2 * precision * recall / (precision + recall)
	return precision, recall, fscore

#%% --------------------------------------------------------------------
#
#                             Evaluate Classifier
#
# ----------------------------------------------------------------------

def evaluate_classifier (numTrainR, numTrainN, numTestR, numTestN, verbose):
    '''
        I used code from
        http://www.nltk.org/book/ch06.html
        for this

    '''

    #load raw tweets:
    rawRacistTweets = loadRacistTweets(numTweets = numTrainR + numTestR, excludeJokes=True)
    rawNormalTweets = loadNonRacistTweets(numTweets = numTrainN + numTestN)
    #rawTweets = rawRacistTweets + rawNormalTweets

    print("Number of racist tweets: {}.".format(len(rawRacistTweets)));
    print("Number of normal tweets: {}.".format(len(rawNormalTweets)));

    #split into train/test sets
    trainR = rawRacistTweets[0:numTrainR];
    print(len(trainR))
    testR = rawRacistTweets[numTrainR:numTrainR + numTestR];
    print(len(testR))

    trainN = rawNormalTweets[0:numTrainN];
    print(len(trainN))
    testN = rawNormalTweets[numTrainN:numTrainN + numTestN];
    print(len(testN))

    #combine racist/non-racist tweets into single train/test datasets
    trainTweets = trainR + trainN;
    testTweets = testR + testN;

    #pre-process tweets (i.e. remove certain words):
    preprocessedTrainTweets = [(preprocess(d), c) for (d, c) in trainTweets];
    preprocessedTestTweets = [(preprocess(d), c) for (d, c) in testTweets];

    featureExtractor = FeatureExtractor([FeatureExtractor.UNIGRAM, FeatureExtractor.BIGRAM, FeatureExtractor.TF_IDF])
    featureExtractor.train_TF_IDF(trainTweets)

    #compute training & testing features
    trainFeats = [(featureExtractor.get_feature_vector(d), c) for (d,c) in preprocessedTrainTweets];
    testFeats = [(featureExtractor.get_feature_vector(d), c) for (d,c) in preprocessedTestTweets];

    svmClass = nltk.classify.SklearnClassifier(LinearSVC());
    svmClass.train(trainFeats);

    #evaluate SVM classifier
    print("----------------------");
    print("SVM Classifier");
    print("accuracy: %.3f" %nltk.classify.accuracy(svmClass, testFeats));

    Y_test = [testFeat[1] for testFeat in testFeats]
    Y_pred = svmClass.classify_many([testFeat[0] for testFeat in testFeats])
    conf=metrics.confusion_matrix(Y_test, Y_pred, [0,1])
    precision, recall, fscore = precision_recall_fscore(conf, 1)



    print("precision: %.3f" %precision)
    print("recall: %.3f" %recall)
    print("f1 score: %.3f" %fscore)
    print("%.1f\%% & %.1f\%% & %.1f\%%" %(100*precision,100*recall,100*fscore))

    print("confusion matrix:")
    print(conf)

    if verbose:
        FP_indeces = np.where(np.subtract(Y_pred, Y_test)==1)[0]
        FN_indeces = np.where(np.subtract(Y_pred, Y_test)==-1)[0]
        for FP_index in FP_indeces:
            print("False positive: {}".format(' '.join(testTweets[FP_index][0])))
        for FN_index in FN_indeces:
            print("False negative: {}".format(' '.join(testTweets[FN_index][0])))

#%% --------------------------------------------------------------------
#
#                             Main Method
#
# ----------------------------------------------------------------------

def main(numTrainR, numTrainN, numTestR, numTestN, verbose):
    '''
    Main method: calls evaluate_classifier() and shows time elapsed
    '''
    t0 = time()
    evaluate_classifier(numTrainR, numTrainN, numTestR, numTestN, verbose)

    tf = time()
    print "Elapsed time: {} seconds".format(tf - t0)

#%% --------------------------------------------------------------------
#
#                             Run Code
#
# ----------------------------------------------------------------------

if __name__ == "__main__" :
    parser = ArgumentParser()
    parser.add_argument("--n-racist-train", type=int, dest="numTrainR",
                default=1000, help="Number of racist tweets in the training set")
    parser.add_argument("--n-normal-train", type=int, dest="numTrainN",
                default=1000, help="Number of non-racist tweets in the training set")
    parser.add_argument("--n-racist-test", type=int, dest="numTestR",
                default=100, help="Number of racist tweets in the test set")
    parser.add_argument("--n-normal-test", type=int, dest="numTestN",
                default=1900, help="Number of non-racist tweets in the test set")
    parser.add_argument("--verbose", type=bool, dest="verbose",
                default=False, help="If verbose=True, print wrong classifications")

    args = parser.parse_args()

    main(**vars(args))