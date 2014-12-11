#!/usr/bin/python

import codecs
import sys
import json

def read_data(ifn):
	sf = codecs.open(ifn)

	line = sf.readline()
	comments = json.loads(line)
	return comments

read_data('../data/raw-data/train.json')
	
