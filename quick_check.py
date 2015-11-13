# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 19:16:05 2015

@author: snoran
"""

import os
import re

tweet_file_pattern = re.compile("all[0-9]*\.txt$")

racist_tweets = []	
total_n_labelled_tweets = 0

for tweets_filename in os.listdir('.') :
	#onl load tweets from files in the form all#*.txt
	if not tweet_file_pattern.match(tweets_filename):
		print('Skipping file %s' %tweets_filename)
		continue
	
	#onl load tweets from files in the form all#*.txt
	f_index = tweets_filename[3:tweets_filename.index('.')]
	labels_filename = 'labels' + f_index + '.txt'
	
	try:
		with open(labels_filename) as dataFile:
			labels = dataFile.readlines()
	except:
		print('Error reading %s' %labels_filename)
		continue
	
	with open(tweets_filename) as dataFile:
		all_tweets = dataFile.readlines()
	
	n = len(labels)
	index = 0
	count = 0
	for tweet in all_tweets:
		if int(labels[index]) == 0: #0 indicates racist
			racist_tweets.append(tweet)
			count += 1
		index+=1
		if index >= len(labels):
			break;
			
	print('Found %i racist tweets of %i total tweets (%f %% )' %(count, n, 100 * count / float(n)))
	total_n_labelled_tweets += n
	
print('All data processed')
print('Found %i racist tweets of %i total tweets (%f %% )' %(len(racist_tweets), total_n_labelled_tweets, 100 * len(racist_tweets) / float(total_n_labelled_tweets)))

	
# TODO: We missed offensive words: 'wetback' and 'fob' (fresh off the boat)
# #FoxNewBeLike "Another ..." ... #CNNBeLike -> good example!