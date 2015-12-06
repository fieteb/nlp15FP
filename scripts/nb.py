from random import shuffle as shuf;
import nltk;
import string;
import sys;

reload(sys);
sys.setdefaultencoding("utf8");

excludedWords = ["the", "be", "to", "of", "and", "a", "in", "that", "have", "it", "not", "for", "on", "with", "he", "as", "you", "do"];
exclude = set(string.punctuation);
[exclude.add(w) for w in excludedWords];

print exclude

def preprocess(line) :
    return ''.join(ch for ch in line.lower() if ch not in exclude);

def loadRacistTweets() :
    fileName = "../data/downloadedRacistTweets.txt";

    tweets = [];
    with open(fileName) as f:
        for line in f:
            tweets.append((preprocess(line).split(), 1));

    shuf(tweets);

    return tweets;

def loadNormalTweets() :
    fileName = "../data/randomTweets200k.txt";

    tweets = [];
    with open(fileName) as f:
        for line in f:
            tweets.append((preprocess(line).split(), 0));

    shuf(tweets);

    return tweets;

def getWords(tupleList):
    res = [];
    for item in tupleList :
        for word in item[0] :
            res.append(word);
    return res;

#http://stackoverflow.com/questions/14003291/n-grams-with-naive-bayes-classifier
def bigramReturner (tweetString):
    tweetString = tweetString.lower()
    #tweetString = removePunctuation (tweetString)
    bigramFeatureVector = []
    for item in nltk.bigrams(tweetString.split()):
        bigramFeatureVector.append(' '.join(item))
    return bigramFeatureVector


'''
    I used code from
    http://www.nltk.org/book/ch06.html
    for this

'''
if __name__ == "__main__" :
    print("NB start");
    racistTweets = loadRacistTweets();
    normalTweets = loadNormalTweets();

    print("Number of racist tweets: {}.".format(len(racistTweets)));
    print("Number of normal tweets: {}.".format(len(normalTweets)));

    trainR = racistTweets[0:4000];
    testR = racistTweets[4000:-1];

    numTrain = 4000;
    numTest = 2308;
    trainN = normalTweets[0:numTrain];
    testN = normalTweets[numTrain:numTrain + numTest];


    trainTweets = trainR + trainN;
    testTweets = testR + testN;

    trainWords = getWords(trainTweets);
    wordFreqs = nltk.FreqDist(w for w in trainWords);

    # plot of most common words
    wordFreqs.plot(50, cumulative=False);

    wordFeatures = list(wordFreqs)[:1000];

    def getFeatures(document) :
        documentWords = set(document);
        features = {};
        for pair in bigramReturner(' '.join(documentWords)):
            features['contains_pair({})'.format(pair)] = 1
        for word in wordFeatures:
            features['contains({})'.format(word)] = (word in documentWords);
        return features


    trainFeats = [(getFeatures(d), c) for (d,c) in trainTweets];
    testFeats = [(getFeatures(d), c) for (d,c) in testTweets];

    print trainFeats[-2]
    print testFeats[-2]

    nbClass = nltk.NaiveBayesClassifier.train(trainFeats);


    print(nltk.classify.accuracy(nbClass, testFeats));

    nbClass.show_most_informative_features(10);

    print("NB end");

    #64.14% on bigram features - BoW
    #73% on unigram features - BoW
    #81.45%
