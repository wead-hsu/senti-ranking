#!/usr/bin/python

import codecs
import sys
import json

def load_feature_values(ifn1, ifn2, ifn3):
	sf = codecs.open(ifn1, 'r', 'utf-8')
	feature_values = set()
	line = sf.readline()
	while line:
		feature_values.add(line.split()[0])
		line = sf.readline()

	sf = codecs.open(ifn2, 'r', 'utf-8')
	line = sf.readline()
	while line:
		feature_values.add(line.split()[0])
		line = sf.readline()

	sf = codecs.open(ifn3, 'r', 'utf-8')
	line = sf.readline()
	while line:
		feature_values.add(line.split()[0])
		line = sf.readline()

	return feature_values


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
	

def gen_features_via_list(ifn, wfn1, wfn2, wfn3, dfn, ofn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	line = sf.readline()
	comments = json.loads(line)
	of = codecs.open(ofn, 'w', 'utf-8')
	director_score, movie_score = load_director_score(dfn)
	feature_values = load_feature_values(wfn1, wfn2, wfn3)

	for comment in comments:
		seg_res = comment['content'][0]
		features = {}
		idx = 0
		while idx < len(seg_res):
			unigram = ''
			bigram = ''
			trigram = ''
			if idx < len(seg_res) - 2:
				trigram = seg_res[idx] + seg_res[idx+1] + seg_res[idx+2]
				if trigram in feature_values:
					features[trigram] = features.get(trigram, 0) + 1
					idx += 2
			elif idx < len(seg_res) - 1:
				bigram = seg_res[idx] + seg_res[idx+1]
				if bigram in feature_values:
					features[bigram] = features.get(bigram, 0) + 1
					idx += 1
			elif seg_res[idx]:
				unigram = seg_res[idx]
				if unigram in feature_values:
					features[unigram] = features.get(unigram, 0) + 1
			idx += 1

		total = 0
		for feature in features.keys():
			total += features[feature]
		
		movie_id = comment['movie_id']
		of.write(director_score[movie_id] + ' ')
		of.write(movie_score[movie_id] + ' ')

		
		if total == 0:
			for word in feature_values:
				of.write('0 ')
		else:
			for word in feature_values:
				if word in features.keys():
					of.write(str(features[word]/total) + ' ')
				else:
					of.write('0 ')

		of.write(comment['rating'])
		
		of.write('\n')

gen_features_via_list('../data/raw-data/train-translate.json', '../data/selected-words/selected-unigrams', '../data/selected-words/selected-bigrams', '../data/selected-words/selected-trigrams', '../data/feature/director-score', '../data/feature/word-feature')
