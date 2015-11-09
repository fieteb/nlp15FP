import time;
import os;

import json;

# DATA_DIR = "/home/fiete/Documents/datasets/twitter";
# COUNTRY_FILE = "/home/fiete/ownCloud/eigeneOrdner/WS2015/NLP/finalProject/countries.txt"
# LANGUAGES_FILE = "/home/fiete/ownCloud/eigeneOrdner/WS2015/NLP/finalProject/languages.txt"
# RACIST_WORDS_FILE = "/home/fiete/ownCloud/eigeneOrdner/WS2015/NLP/finalProject/racistWords.txt"

DATA_DIR = "/home/fiete/Documents/twitter";
COUNTRY_FILE = "/media/fiete/data/OwnCloud/eigeneOrdner/WS2015/NLP/finalProject/countries.txt"
LANGUAGES_FILE = "/media/fiete/data/OwnCloud/eigeneOrdner/WS2015/NLP/finalProject/languages.txt"
RACIST_WORDS_FILE = "/media/fiete/data/OwnCloud/eigeneOrdner/WS2015/NLP/finalProject/racistWords.txt"



def getCountries() :
	res = []
	with open(COUNTRY_FILE) as f :
		for line in f :
			res.append(line.rstrip())
	return res

def getLanguages() :
	res = []
	with open(LANGUAGES_FILE) as f :
		for line in f :
			res.append(line.rstrip())
	return res

def getRacistWords() :
	res = []
	with open(RACIST_WORDS_FILE) as f :
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

	for fileName in os.listdir(DATA_DIR) :
		print "Processing {}".format(fileName)

		# parse file
		with open(os.path.join(DATA_DIR, fileName)) as dataFile :
			lines = dataFile.readlines()

		lineNo = 0
		for line in lines :
			# split the first (location) and the second (tweet) part.
			# the location is until the first "}".
			for splitPos in range(0, len(line)) :
				if line[splitPos] == '}' : break
			splitPos += 1
			
			# load the line as dictionaries,
			#  store them if a word matches the keywords and if the language
			#  is English.
			try :
				loc = json.loads(line[0 : splitPos])
				tweet = json.loads(line[splitPos : -1])	
								
				# only check english tweets
				if tweet["user"]["lang"] in languages and loc["country_iso3"] in countries:	
					for word in tweet["text"].split() :
						if word.lower() in racistWords : 
				
							locs.append(loc)
							tweets.append(tweet)
							print tweet["text"]
							break
			except :
				"Error parsing line. Skipping to next"
			lineNo += 1
			
		
			
		print "Reading {} done.".format(fileName)
		break



def calcSeconds(start, end) :
	return (end - start) / 60

if __name__ == "__main__" :
	start = time.time()

	collectData()

	end = time.time()
	print "Elapsed time: {}".format(calcSeconds(start, end))
