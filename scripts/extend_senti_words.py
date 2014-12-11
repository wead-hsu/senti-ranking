#!/usr/bin/python

import codecs
import numpy as np

def extend_senti_words(ifn, wfn, ofn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	wf = codecs.open(wfn, 'r', 'utf-8')
	of = codecs.open(ofn, 'w', 'utf-8')

	word_vectors = {}
	line = wf.readline()
	while line:
		words = line.split()
		if not len(words):
			print words
			line = wf.readline()
			continue
		word_vectors[words[0]] = []
		for i in range(1, len(words)):
			word_vectors[words[0]].append(float(words[i]))
		line = wf.readline()

	word_abs_dis = {}
	for key in word_vectors.keys():
		len_1 = 0
		vec = word_vectors[key]
		for x in vec:
			len_1 += x*x
		word_abs_dis[key] = vec[0] * 1 / np.sqrt(len_1)

	line = sf.readline()
	while line:
		word = line.split()[0]
		nears = find_near(word, word_vectors, 1)
		print nears
		line = sf.readline
	
	return

def find_near(word, word_vectors, cnt):
	if word not in word_vectors.keys():
		return None

	word_vector = word_vectors[word]
	dis = {}

	for key in word_vectors.keys():
		dis[w] = cal_cos_dis(word_vectors[key], word_vectors[word])
	
	sorted_dis = sorted(dis, key = lambda d: d[1], reverse = True)
	
	return sorted_dis[0: 5]

def cal_cos_dis(w1, w2):
	len_1 = 0
	len_2 = 0
	
	for x in w1:
		len_1 += x*x
	for x in w2:
		len_2 += x*x
	
	dis = 0
	for i in range(len(w1)):
		dis += w1[i] * w2[i]

	return dis/np.sqrt(len_1)/np.sqrt(len_2)

extend_senti_words('../data/senti-words/mutals-and-adj', '/Users/wdxu/git/qa-demo/data/word2vec/lookup.txt', '../data/senti-words/extend-mutals-and-adj')
