import nltk;
import string;
import sys;
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier

from tweetLoader import loadNonRacistTweets;
from tweetLoader import loadRacistTweets;

from preprocessing import nbPreprocess;

reload(sys);
sys.setdefaultencoding("utf8");

excludedWords = set();
with open("../data/uninterestingWords.txt") as f :
    for line in f:
        excludedWords.add(line.strip());
        

punct = set(string.punctuation);

def getWords(tupleList):
    res = [];
    for item in tupleList :
        for word in item[0] :
            res.append(word);
    return res;



'''
    I used code from
    http://www.nltk.org/book/ch06.html
    for this

'''
if __name__ == "__main__" :
    print("NB start");
    racistTweets = [(nbPreprocess(d), c) for (d, c) in loadRacistTweets(excludeJokes=True)];
    normalTweets = [(nbPreprocess(d), c) for (d, c) in loadNonRacistTweets(numTweets=len(racistTweets))];   

    print("Number of racist tweets: {}.".format(len(racistTweets)));
    print("Number of normal tweets: {}.".format(len(normalTweets)));
    
    numTrain = 1500;
    numTest = 500; 
     
    trainR = racistTweets[0:numTrain];
    testR = racistTweets[numTrain:numTrain + numTest];
     
    trainN = normalTweets[0:numTrain];
    testN = normalTweets[numTrain:numTrain + numTest];
    
    
    trainTweets = trainR + trainN;
    testTweets = testR + testN;
    
    trainWords = getWords(trainTweets);
    wordFreqs = nltk.FreqDist(w for w in trainWords);
    
    # plot of most common words
    # wordFreqs.plot(50, cumulative=False);
    
    wordFeatures = list(wordFreqs)[:1000];
    
    def getFeatures(document) : 
        documentWords = set(document);
        features = {};
        for word in wordFeatures:
            features['contains({})'.format(word)] = (word in documentWords);
        return features
    
         
    trainFeats = [(getFeatures(d), c) for (d,c) in trainTweets];
    testFeats = [(getFeatures(d), c) for (d,c) in testTweets];
    
    # Bayes
    nbClass = nltk.NaiveBayesClassifier.train(trainFeats);
    
    print("----------------------");
    print("Naive Bayes Classifier");
    print(nltk.classify.accuracy(nbClass, testFeats));
         
    # SVM
    svmClass = nltk.classify.SklearnClassifier(LinearSVC());
    svmClass.train(trainFeats);
    
    print("----------------------");
    print("SVM Classifier");
    print(nltk.classify.accuracy(svmClass, testFeats));
    
    # RF
    rfClass = nltk.classify.SklearnClassifier(RandomForestClassifier(n_estimators = 100));
    rfClass.train(trainFeats);
    
    print("----------------------");
    print("RF Classifier");
    print(nltk.classify.accuracy(rfClass, testFeats));