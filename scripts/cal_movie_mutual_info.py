#!/usr/bin/python

import codecs
import sys
import json
import numpy as np

def load_unigrams(ifn):
	sf = codecs.open(ifn, 'r', 'utf-8')

	unigrams = set()
	unigram_cnt = {}
	line = sf.readline()
	while line:
		unigrams.add(line.split()[0])
		unigram_cnt[line.split('\t')[0]] = line.split('\t')[1]
		line = sf.readline()
	
	return unigrams, unigram_cnt

def load_bigrams(ifn):
	sf = codecs.open(ifn, 'r', 'utf-8')

	bigrams = set()
	bigram_cnt = {}
	line = sf.readline()
	while line:
		bigrams.add(line.split('\t')[0])
		bigram_cnt[line.split('\t')[0]] = line.split('\t')[1]
		line = sf.readline()

	return bigrams, bigram_cnt

# load_unigrams, load_bigrams, load_trigrams are the same.
def load_trigrams(ifn):
	sf = codecs.open(ifn, 'r', 'utf-8')

	trigrams = set()
	line = sf.readline()
	trigram_cnt = {}
	while line:
		trigrams.add(line.split()[0])
		trigram_cnt[line.split('\t')[0]] = line.split('\t')[1]
		line = sf.readline()

	return trigrams, trigram_cnt

def cal_unigram_mutal_infos(ifn, ufn, ofn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	of = codecs.open(ofn, 'w', 'utf-8')
	comments = json.loads(sf.readline())
	unigrams, unigram_cnt = load_unigrams(ufn)

	movie_ids = set()
	for comment in comments:
		movie_ids.add(comment['movie_id'])
	
	print len(unigrams)
	cnt = {}
	for i in movie_ids:
		cnt[i] = {}
		for word in unigrams:
			cnt[i][word] = 0

	for comment in comments:
		seg_res = comment['content'][0]
		movie_id = comment['movie_id']
		for word in seg_res:
			if word not in unigrams:
				print word
			else:
				cnt[movie_id][word] += 1

	cnt_movie = {}
	for i in movie_ids:
		cnt_movie[i] = 0
		for word in unigrams:
			cnt_movie[i] += cnt[i][word]

	cnt_unigram = {}
	for word in unigrams:
		cnt_unigram[word] = 0
		for i in movie_ids:
			cnt_unigram[word] += cnt[i][word]

	total_cnt = 0.0
	for i in cnt_movie.keys():
		total_cnt += cnt_movie[i]
		
	mutals = {}
	for word in unigrams:
		mutals[word] = 0.0
	
	for word in unigrams:
		# x = 1, which indicates that word does appear
		for j in movie_ids:
			px_1y = cnt[i][word]/total_cnt
			px_1 = cnt_unigram[word]/total_cnt
			py = cnt_movie[i]/total_cnt
			px_0y = py - px_1y
			px_0 = 1 - px_1
			#print px_1y, px_0y, px_1, px_0, py
			if cnt[i][word]:
				mutals[word] += px_1y*np.log(px_1y/px_1/py)
			mutals[word] += px_0y*np.log(px_0y/px_0/py)
	
	sorted_mutals = sorted(mutals.items(), key = lambda d: d[1], reverse = True)
	
	for item in sorted_mutals:
		of.write(item[0] + '\t' + str(item[1]) + '\t' + unigram_cnt[item[0]])

def cal_bigram_mutal_infos(ifn, ufn, ofn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	of = codecs.open(ofn, 'w', 'utf-8')
	comments = json.loads(sf.readline())
	bigrams, bigram_cnt = load_bigrams(ufn)

	movie_ids = set()
	for comment in comments:
		movie_ids.add(comment['movie_id'])
	
	print len(bigrams)
	cnt = {}
	for i in movie_ids:
		cnt[i] = {}
		for word in bigrams:
			cnt[i][word] = 0

	for comment in comments:
		seg_res = comment['content'][0]
		movie_id = comment['movie_id']
		for idx in range(len(seg_res) - 1):
			word = seg_res[idx] + seg_res[idx+1]
			if word not in bigrams:
				print word
			else:
				cnt[movie_id][word] += 1

	cnt_movie = {}
	for i in movie_ids:
		cnt_movie[i] = 0
		for word in bigrams:
			cnt_movie[i] += cnt[i][word]

	cnt_bigram = {}
	for word in bigrams:
		cnt_bigram[word] = 0
		for i in movie_ids:
			cnt_bigram[word] += cnt[i][word]

	total_cnt = 0.0
	for i in cnt_movie.keys():
		total_cnt += cnt_movie[i]
		
	mutals = {}
	for word in bigrams:
		mutals[word] = 0.0
	
	for word in bigrams:
		# x = 1, which indicates that word does appear
		for j in movie_ids:
			px_1y = cnt[i][word]/total_cnt
			px_1 = cnt_bigram[word]/total_cnt
			py = cnt_movie[i]/total_cnt
			px_0y = py - px_1y
			px_0 = 1 - px_1
			#print px_1y, px_0y, px_1, px_0, py
			if cnt[i][word]:
				mutals[word] += px_1y*np.log(px_1y/px_1/py)
			mutals[word] += px_0y*np.log(px_0y/px_0/py)
	
	sorted_mutals = sorted(mutals.items(), key = lambda d: d[1], reverse = True)
	
	for item in sorted_mutals:
		of.write(item[0] + '\t' + str(item[1]) + '\t' + bigram_cnt[item[0]])

def cal_trigram_mutal_infos(ifn, ufn, ofn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	of = codecs.open(ofn, 'w', 'utf-8')
	comments = json.loads(sf.readline())
	trigrams, trigram_cnt = load_trigrams(ufn)

	movie_ids = set()
	for comment in comments:
		movie_ids.add(comment['movie_id'])
	
	print len(trigrams)
	cnt = {}
	for i in movie_ids:
		cnt[i] = {}
		for word in trigrams:
			cnt[i][word] = 0

	for comment in comments:
		seg_res = comment['content'][0]
		movie_id = comment['movie_id']
		for idx in range(len(seg_res) - 2):
			word = seg_res[idx] + seg_res[idx+1] + seg_res[idx+2]
			if word not in trigrams:
				print word
			else:
				cnt[movie_id][word] += 1

	cnt_movie = {}
	for i in movie_ids:
		cnt_movie[i] = 0
		for word in trigrams:
			cnt_movie[i] += cnt[i][word]

	cnt_trigram = {}
	for word in trigrams:
		cnt_trigram[word] = 0
		for i in movie_ids:
			cnt_trigram[word] += cnt[i][word]

	total_cnt = 0.0
	for i in cnt_movie.keys():
		total_cnt += cnt_movie[i]
		
	mutals = {}
	for word in trigrams:
		mutals[word] = 0.0
	
	for word in trigrams:
		# x = 1, which indicates that word does appear
		for j in movie_ids:
			px_1y = cnt[i][word]/total_cnt
			px_1 = cnt_trigram[word]/total_cnt
			py = cnt_movie[i]/total_cnt
			px_0y = py - px_1y
			px_0 = 1 - px_1
			#print px_1y, px_0y, px_1, px_0, py
			if cnt[i][word]:
				mutals[word] += px_1y*np.log(px_1y/px_1/py)
			mutals[word] += px_0y*np.log(px_0y/px_0/py)
	
	sorted_mutals = sorted(mutals.items(), key = lambda d: d[1], reverse = True)
	
	for item in sorted_mutals:
		of.write(item[0] + '\t' + str(item[1]) + '\t' + trigram_cnt[item[0]])

cal_unigram_mutal_infos('../data/raw-data/train.json', '../data/word-list/unigram', '../data/mutal-info/movie-unigram')
cal_bigram_mutal_infos('../data/raw-data/train-translate.json', '../data/word-list/bigram', '../data/mutal-info/movie-bigram')
cal_trigram_mutal_infos('../data/raw-data/train-translate.json', '../data/word-list/trigram', '../data/mutal-info/movie-trigram')
