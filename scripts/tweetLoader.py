
LABEL_FILES = ["../data/labels.txt", "../data/labels2.txt", "../data/labels3.txt"];

TWEET_FILES = ["../data/all.txt", "../data/all2.txt", "../data/all3.txt"];

def loadNonRacistTweets(numTweets = None) :
    numLoadedTweets = 0;
    res = [];
    for fileIdx in range(3) :
        
        with open(TWEET_FILES[fileIdx]) as f :
            tweets = f.readlines();
            
        with open(LABEL_FILES[fileIdx]) as f :
            labels = f.readlines();
            
        for lineIdx in range(len(labels)) :
            label = int(labels[lineIdx]);
            
            if label == 1 :
                res.append((tweets[lineIdx].split(" "), 0));
                numLoadedTweets += 1;
                
                if numTweets != None and numLoadedTweets >= numTweets :
                    break;
                
        if numTweets != None and numLoadedTweets >= numTweets :
            break;
        
    return res;
    

def loadRacistTweets(numTweets = None, excludeJokes = False):
    numLoadedTweets = 0;
    res = [];
    for fileIdx in range(3) :
        
        with open(TWEET_FILES[fileIdx]) as f :
            tweets = f.readlines();
            
        with open(LABEL_FILES[fileIdx]) as f :
            labels = f.readlines();
            
        for lineIdx in range(len(labels)) :
            label = int(labels[lineIdx]);
            
            if label == 0 :
                res.append((tweets[lineIdx].split(" "), 1));
                numLoadedTweets += 1;
                
                if numTweets != None and numLoadedTweets >= numTweets :
                    break;
            
            # stop if jokes should be excluded:    
            if excludeJokes and fileIdx == 2 and lineIdx >= 3113 :
                break;
                
        if numTweets != None and numLoadedTweets >= numTweets :
            break;
        
    return res;



if __name__ == "__main__" :
    # with jokes:
    print len(loadRacistTweets());
    # without jokes:
    print len(loadRacistTweets(excludeJokes=True));
    print len(loadNonRacistTweets());
    