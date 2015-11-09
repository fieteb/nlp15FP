import time;
import os;

import json;
import configData;
import re;

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
	regex = ''
		
	with open(configData.racistWordsFile) as f :
		for line in f :
			regex += r'|\b' + line.replace(' ', '\s').strip() + r'\b'
			regex += r'|\b' + line.replace(' ', '\s').strip() + 's' + r'\b' #plural form
			regex += r'|\b' + line.replace(' ', '\s').strip() + '\'s' + r'\b' #possessive form

	return re.compile(regex[2:], flags=re.I | re.X)

def collectData() :
	countries = getCountries()
	languages = getLanguages()
	pattern = getRacistWords()
	
	print "Countries: {}".format(countries)
	print "Languages: {}".format(languages)
	locs = []
	tweets = []

	for fileName in os.listdir(configData.dataDir) :
		print "Processing {}".format(fileName)

		# parse file
		with open(os.path.join(configData.dataDir, fileName)) as dataFile :
			lines = dataFile.readlines()
			
		parsed_data = [sample.split('\t') for sample in lines[:-1]]
		
		for sample in parsed_data:
			loc = json.loads(sample[0])
			tweet = json.loads(sample[1])
			
			if tweet["user"]["lang"] in languages and loc["country_iso3"] in countries:
				if pattern.match(tweet["text"]):
					locs.append(loc)
					tweets.append(tweet)
					print tweet["text"]
					
		print "Reading {} done.".format(fileName)
		break

def calcSeconds(start, end) :
	return (end - start) / 60

if __name__ == "__main__" :
	start = time.time()

	collectData()

	end = time.time()
	print "Elapsed time: {}".format(calcSeconds(start, end))
