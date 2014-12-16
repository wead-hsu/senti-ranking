#!/usr/bin/python
#encoding=utf-8

import codecs
import sys
import json
import numpy as np

def load_distributions(ifn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	dis = {}
	line = sf.readline()
	while line:
		splits = line.split()
		dis[splits[0]] = []
		if len(splits) < 7:
			print splits
		for i in range(1, 7):
			dis[splits[0]].append(float(splits[i]))
		#if splits[0] == u'剪辑':
		#	print '`````````````' +line
		line = sf.readline()
	return dis

def load_director_score(ifn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	line = sf.readline()
	director_score = {}
	movie_score = {}
	while line:
		line = line.strip()
		director_score[line.split('\t')[0]] = line.split('\t')[2]
		movie_score[line.split('\t')[0]] = line.split('\t')[3]
		line =  sf.readline()
	return director_score, movie_score

def load_rating_distribution(ifn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	line = sf.readline()
	rating_distribution = {}
	while line:
		rating_distribution[int(line.split()[0]) - 1] = float(line.split()[1])
		line = sf.readline()
	
	total = 0.0
	for key in rating_distribution.keys():
		total += rating_distribution[key]
	
	for key in rating_distribution.keys():
		rating_distribution[key] = rating_distribution[key]/total

	return rating_distribution

def gen_features_via_list(ifn, mfn, efn, dfn,rfn,  ofn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	line = sf.readline()
	comments = json.loads(line)
	of = codecs.open(ofn, 'w', 'utf-8')
	director_score, movie_score = load_director_score(dfn)
	rating_distribution = load_rating_distribution(rfn)

	mutals = load_distributions(mfn)
	extends = load_distributions(efn)

	sentis = dict(mutals.items())# + extends.items())
	print u'的' in sentis.keys()

	for comment in comments:
		seg_res = comment['content'][0]
		features = []
		idx = 0
		while idx < len(seg_res):
			neg = False
			if seg_res[idx] == u'不':
				idx += 1
				neg = True

			if idx + 2 < len(seg_res) and seg_res[idx] + seg_res[idx+1] + seg_res[idx+2] in sentis.keys():
				features.append([seg_res[idx] + seg_res[idx+1] + seg_res[idx+2], neg])
				idx += 3
			elif idx + 1 < len(seg_res) and seg_res[idx] + seg_res[idx+1] in sentis.keys():
				features.append([seg_res[idx] + seg_res[idx+1], neg])
				idx += 2
			elif idx < len(seg_res) and seg_res[idx] in sentis.keys():
				features.append([seg_res[idx], neg])
				idx += 1
			else:
				idx += 1
		'''	
		for feature in features:
			of.write(feature[0] + ' ' + str(feature[1]) + '\t')
		of.write('\n')
		'''

		likelihoods = []
		for i in range(5):
			likelihoods.append(0.0)
		for feature in features:
			distribution = sentis[feature[0]]
			if feature[0] == u'剪辑':
				print distribution
			for i in range(5):
				if feature[1]:
					likelihoods[4-i] += np.log((distribution[i]+1)/(distribution[5]+5))
					likelihoods[4-i] -= np.log(rating_distribution[i])
				else:
					likelihoods[i] += np.log((distribution[i]+1)/(distribution[5]+5))
					likelihoods[i] -= np.log(rating_distribution[i])
		
		
		movie_id = comment['movie_id']
		of.write(director_score[movie_id] + ' ')
		of.write(movie_score[movie_id] + ' ')
		of.write(str(len(seg_res)) + ' ')
	

		max_value = -10000.0
		for value in likelihoods:
			if max_value < value:
				max_value = value
		for idx in range(len(likelihoods)):
			likelihoods[idx] = likelihoods[idx] - max_value

		sum_value = 0.0
		for value in likelihoods:
			sum_value += np.exp(value)

		for idx in range(len(likelihoods)):
			if sum_value != 5:
				likelihoods[idx] = np.exp(likelihoods[idx]) / sum_value
		
		for word in likelihoods:
			of.write(str(word) + ' ')

		of.write('?')
		
		of.write('\n')

gen_features_via_list('../data/raw-data/test-translate.json', '../data/senti-words/mutals-and-adj-slt', '../data/senti-words/sel-ext-senti-words', '../data/feature/director-score', '../data/feature/rating-cnt', '../data/feature/mle-not-ext-slt-norm-test')
