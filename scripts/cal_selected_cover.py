#!/usr/bin/python

import codecs
import sys

def load_selected(ifn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	sels = set()
	line = sf.readline()
	while line:
		sels.add(line.split()[0])
		line = sf.readline()

	return sels

def load_mutals(ifn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	mutals = []
	line = sf.readline()
	while line:
		mutals.append(line.split()[0])
		line = sf.readline()

	return mutals

def cal_rating(sels, mutals):
	len_mutals = len(mutals)
	patch_num = 20
	patch_len = len_mutals/patch_num
	cnt = 0
	
	print len_mutals/patch_num
	print 


	for i in range(patch_num):
		patch_start = patch_len * i
		patch_end = min(patch_len * (i+1), len_mutals)
		
		cnt = 0
		for j in range(patch_start, patch_end):
			if mutals[j] in sels:
				cnt += 1
			#else:
			#	print mutals[j]

		print cnt*1.0
	

sels = load_selected('../data/senti-words/mutals-and-adj')
mutals = load_mutals('../data/mutal-info/rating-trigram-re')
cal_rating(sels, mutals)
