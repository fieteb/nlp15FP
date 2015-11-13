import csv;
import os;
import sys;



def getCSVFileNames() :
    dirName = os.path.dirname(os.path.realpath(__file__));
    
    fileNames = [];
    
    for fileName in os.listdir(dirName) :
        if fileName.endswith(".csv") :
            fileNames.append(dirName + "/" + fileName);
            
    return fileNames;

def readInCSVFiles(fileNames) :
    reload(sys);
    sys.setdefaultencoding("utf8");
    
    # (1) read in
    lines = [];
    numTweets = 0;
    for fileName in fileNames :
        with open(fileName) as csvFile :
            csvReader = csv.reader(csvFile, delimiter = ',');
            
            # skip first line
            iterRows = iter(csvReader);
            next(iterRows);
            
            for row in iterRows :
                
                text = (" ".join(row[2].splitlines()));
                numTweets += 1;
                lines.append(text);
                
                    
    print("Total {} tweets.".format(numTweets));
    
    
    # (2) save            
    with open("downloadedTweets.txt", "w") as file :
        for line in lines :
            file.write(line + "\n");



if __name__ == "__main__" :
    
    fileNames = getCSVFileNames();
    
    readInCSVFiles(fileNames);