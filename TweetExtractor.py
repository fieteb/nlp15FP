import json;
import configData as config;
import utils;
import os;
import time;
import sys;

class TweetExtractor :
    def __init__(self) :
        tweetKeyWords = utils.loadRowsAsList(config.ConfigData().racistWordsFile);
        tweetAttributes = ["lang"];
        tweetConditions = [["en"]];
        self.tweetFilter = utils.Filter(tweetKeyWords, tweetAttributes, tweetConditions);
        
        # no location filtering atm
        locKeyWords = None;
        locAttributes = None; 
        locConditions = None;
        self.locFilter = utils.Filter(locKeyWords, locAttributes, locConditions);
        
    def evaluateTweets(self, data) :
        '''
            tweets = list of \t separated json strings
             where the first one is location data and the second one
             the tweet itself
        '''
        
        tweets = [];
        texts = [];
             
        i = 0;
        for dataLine in data :
            jsonStrings = dataLine.split('\t');
            # if the location filter applies
            if self.locFilter.evalDict(json.loads(jsonStrings[0])) :
                tweet = json.loads(jsonStrings[1]);
                if self.tweetFilter.evalDict(tweet) :
                    i += 1
                    tweets.append(dataLine);
                    texts.append(tweet["text"].replace("\n", ""));
                    
        print("{} detected Tweets.".format(i));
                        
        return tweets, texts; 
        
  
        
if __name__ == "__main__" :
    tweetExtractor = TweetExtractor();
    conf = config.ConfigData();
    
    tweetFiles = [];
    for fileName in os.listdir(conf.dataDir) :
        tweetFiles.append(os.path.join(conf.dataDir, fileName));
    
    reload(sys);
    sys.setdefaultencoding("utf8");
    
    for filename in tweetFiles :
        with open(filename) as dataFile :
            lines = dataFile.readlines();
        
        print("Processing {}".format(filename));
        startTime = time.time();
        tweets, texts = tweetExtractor.evaluateTweets(lines);
        
        f = open(filename + "filteredTweets",'w');
        for line in tweets :
            f.write(line);
        f.close();
        
        f = open(filename + "filteredTexts",'w');
        for line in texts :
            f.write(line + "\n");
        f.close();
        
        endTime = time.time();
        print("Elapsed time: {} seconds.".format((endTime - startTime))) 
        
    
    print("End");
