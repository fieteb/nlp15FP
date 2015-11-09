import time;
import os;

import json;
import configData;

configData = configData.getConfig();

def getCountries() :
	res = []
	with open(configData.countryFile) as f :
		for line in f :
			res.append(line.rstrip())
	return res

def getLanguages() :
	res = []
	with open(configData.languageFile) as f :
		for line in f :
			res.append(line.rstrip())
	return res

def getRacistWords() :
	res = []
	with open(configData.racistWordsFile) as f :
		for line in f :
			res.append(line.rstrip())
	return res

def collectData() :
	countries = getCountries()
	languages = getLanguages()
	racistWords = getRacistWords()
	
      print "Countries: {}".format(countries)
	print "Languages: {}".format(languages)
	print "Racist words: {}".format(racistWords)
	locs = []
	tweets = []

	for fileName in os.listdir(configData.dataDir) :
		print "Processing {}".format(fileName)

		# parse file
		with open(os.path.join(configData.dataDir, fileName)) as dataFile :
			lines = dataFile.readlines()
   
            parsed_data = [sample.split('\t') for sample in json_data[:-1]]
            
            for sample in parsed_data:
                loc = json.loads(sample[2])
                tweet = json.loads(sample[3])                
                
                if tweet["user"]["lang"] in languages and loc["country_iso3"] in countries:	
                    for word in tweet["text"].split() :
                        if word.lower() in racistWords :
                            locs.append(loc)
                            tweets.append(tweet)
                            print tweet["text"]
                            break
			
		print "Reading {} done.".format(fileName)
		break

#		lineNo = 0
#		for line in lines :
#			# split the first (location) and the second (tweet) part.
#			# the location is until the first "}".
#			for splitPos in range(0, len(line)) :
#				if line[splitPos] == '}' : break
#			splitPos += 1
#			
#			# load the line as dictionaries,
#			#  store them if a word matches the keywords and if the language
#			#  is English.
#			try :
#				loc = json.loads(line[0 : splitPos])
#				tweet = json.loads(line[splitPos : -1])	
#								
#				# only check english tweets
#				if tweet["user"]["lang"] in languages and loc["country_iso3"] in countries:	
#					for word in tweet["text"].split() :
#						if word.lower() in racistWords : 
#				
#							locs.append(loc)
#							tweets.append(tweet)
#							print tweet["text"]
#							break
#			except :
#				"Error parsing line. Skipping to next"
#			lineNo += 1



def calcSeconds(start, end) :
	return (end - start) / 60

if __name__ == "__main__" :
	start = time.time()

	collectData()

	end = time.time()
	print "Elapsed time: {}".format(calcSeconds(start, end))
