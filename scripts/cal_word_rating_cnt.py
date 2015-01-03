#!/usr/bin/python

import json
import codecs
import xml.etree.ElementTree as etree
import sys

def cal_director_score(ifn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	line = sf.readline()
	
	rating = {}
	for i in range(1,6):
		rating[str(i)] = i

	while line:
		words = line.split()
		for i in range(1,6):
			rating[str(i)] += int(words[i])

		line = sf.readline()
	
	total = 0
	for key in rating.keys():
		total += rating[key]

	for key in rating.keys():
		rating[key] = rating[key] * 1.0 /total
		print key, rating[key]

cal_director_score('../data/senti-words/mutals-and-adj-slt')
