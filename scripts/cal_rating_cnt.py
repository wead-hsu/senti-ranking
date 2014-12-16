#!/usr/bin/python

import json
import codecs
import xml.etree.ElementTree as etree
import sys

def cal_director_score(ifn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	comments = json.loads(sf.readline())
	
	rating = {}
	for i in range(1,6):
		rating[str(i)] = 0

	for comment in comments:
		rating[comment['rating']] += 1
		
	for key in rating.keys():
		print key, rating[key]

cal_director_score('../data/raw-data/train-translate.json')
