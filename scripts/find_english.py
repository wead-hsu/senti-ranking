#!/usr/bin/python 

import codecs
import sys

def find_english(ifn, ofn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	of = codecs.open(ofn, 'w', 'utf-8')

	line = sf.readline()
	while line:
		word = line.split()[0]
		if is_alphabet(word[0]):
			of.write(line.split()[0] + '\n')
		line = sf.readline()

	return 0

def is_alphabet(char):
	if 'a' <= char and char <= 'z':
		return True
	if 'A' <= char and char <= 'Z':
		return True

if __name__ == '__main__':
	find_english('../data/word-list/unigram', '../data/english/english-words')
