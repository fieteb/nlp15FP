import json;
import configData as config;
import os;
import sys;


def processRandomData() :
    conf = config.ConfigData();
        
    tweetFiles = [];
    for fileName in os.listdir(conf.dataDir) :
        tweetFiles.append(os.path.join(conf.dataDir, fileName));
    
    reload(sys);
    sys.setdefaultencoding("utf8");
    
    numLines = 0;
    limit = 200000;
    texts = [];
    
    for filename in tweetFiles :
        with open(filename) as dataFile :
            if numLines >= limit : break;
            print("Reading in {}".format(filename));
            lines = dataFile.readlines();
            
            for line in lines :
                if numLines >= limit : break;
                
                jsonStrings = line.split('\t');
                tweet = json.loads(jsonStrings[1]);
                loc = json.loads(jsonStrings[0]);
                if loc["country_iso3"] == "USA" and tweet["user"]["lang"] == "en":
                    texts.append(tweet["text"].replace("\n", ""));
                    numLines += 1;
                    
                    if numLines % 10000 == 0 :
                        print "processed {} lines.".format(numLines);
            
                
    print("Number of lines: {}".format(numLines));
    
    reload(sys);
    sys.setdefaultencoding("utf8");
    
    with open("randomTweets200k.txt", "w") as f:
        for line in texts :
            f.write(line + "\n");
    
if __name__ == "__main__" :
    processRandomData();
                
