#!/usr/bin/python

import sys
import codecs
import json

def load_mutals_and_adjs(ifn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	scores = {}
	line = sf.readline()
	while line:
		words = line.split()
		scores[words[0]] = []
		for i in range(1, len(words)):
			scores[words[0]].append(float(words[i]))
		line = sf.readline()
	return scores

def sel_ext_senti_words(ifn, scores, ofn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	line = sf.readline()
	of = codecs.open(ofn, 'w', 'utf-8')

	nears = {}
	while line:
		splits = line.split()
		if len(splits) != 1:
			for i in range(1, len(splits)):
				if i%2 == 1 and float(splits[i+1]) > 0.7and splits[i] not in scores.keys():
					if splits[i] not in nears.keys():
						nears[splits[i]] = {}
					nears[splits[i]][splits[0]] = float(splits[i+1])
		line = sf.readline()

	for key in nears.keys():
		tmp = nears[key]
		sorted_tmp = sorted(tmp.items(), key = lambda d: d[1], reverse = True)
		of.write(key + '\t' )
		for number in scores[sorted_tmp[0][0]]:
			of.write(str(number) + ' ')
		of.write('\t' + sorted_tmp[0][0] + '\t'+ str(sorted_tmp[0][1]) + '\t' + '\n')

scores = load_mutals_and_adjs('../data/senti-words/mutals-and-adj')
sel_ext_senti_words('../data/senti-words/extend-mutals-and-adj', scores, '../data/senti-words/sel-ext-senti-words')
