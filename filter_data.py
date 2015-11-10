# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 20:16:48 2015

@author: snoran
"""

import json
from time import time
import re
import os
import configData

configData = configData.getConfig();

def getRacistWords():
	res = [];
	with open(configData.racistWordsFile) as f :
		for line in f :
			res.append(line.strip())
	return res;
	
def getCountries() :
	res = []
	with open(configData.countryFile) as f :
		for line in f :
			res.append(line.strip())
	return res

def getLanguages() :
	res = []
	with open(configData.languageFile) as f :
		for line in f :
			res.append(line.strip())
	return res
	
countries = getCountries()
languages = getLanguages()
race_related_words = getRacistWords()

# can we filter out specific cases like "Black Swan", "Black Ops", "Black-eyed Peas"
    
regex = r'\b' + race_related_words[0] + r'\b'
for i in range(1,len(race_related_words)):
	word = race_related_words[i].replace(' ', r'\s')
	regex += r' | \b' + word + r'\b'
	regex += r' | \b' + word + 's' + r'\b' #plural form
	regex += r' | \b' + word + '\'s' + r'\b' #possessive form
        
pattern = re.compile(regex, flags=re.I | re.X)

print "Countries: {}".format(countries)
print "Languages: {}".format(languages)
locs = []
tweets = []
for fileName in os.listdir(configData.dataDir) :
	with open(os.path.join(configData.dataDir, fileName)) as dataFile :
		raw_data = dataFile.read().split('\n')
    
	print('Loading all Twitter data from %s' %fileName)
	t0 = time()
	json_data = [sample.split('\t') for sample in raw_data[:-1]] #-1 to ignore last line which is empty
	loc_data = [json.loads(d[0]) for d in json_data]
	all_tweets = [json.loads(d[1]) for d in json_data]
	tf = time()
	print('Time elapsed: %f seconds' %(tf-t0))
	
	#filter by language and location:
	print('Filtering tweets by language and location ...')
	t0 = time()
	loc_filtered_tweets = [all_tweets[i]['text'] for i in range(len(all_tweets)) if loc_data[i]['country_iso3'] in countries and all_tweets[i]['user']['lang'] in languages]
	tf = time()
	print('Time elapsed: %f seconds' %(tf-t0))
    
	print('Filtering tweets by race-relevant words...')
	t0 = time()
	word_filtered_tweets=filter(pattern.search, loc_filtered_tweets)
	tf = time()
	print('Time elapsed: %f seconds' %(tf-t0))
    
	print('Saving filtered tweets to %s' %configData.filtered_tweets_file)
	t0 = time()
	f = open(configData.filtered_tweets_file,'w')
	count = 0
	for tweet in word_filtered_tweets:
		try:
			if '\n' not in tweet: #make sure to ignore tweets with newline character because we are separating tweets based off that
				f.write(tweet + '\n') # python will convert \n to os.linesep
		except:
			count+=1
			pass
	f.close()
	tf = time()
	print('Time elapsed: %f seconds' %(tf-t0))
	print('Skipped %i tweets due to encoding mismatch' %count)