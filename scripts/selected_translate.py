#!/usr/bin/python
#encoding=utf-8

#this script is used for translate the selected words. A UTIL SCRIPT

import xml.etree.ElementTree as etree
import codecs
import jieba.posseg as pseg
import sys
import json

def translate_selected_words(ifn1, ifn2, ifn3, ofn):
	of = codecs.open(ofn, 'w', 'utf-8')
	sf = codecs.open(ifn1, 'r', 'utf-8')
	feature_values = set()
	line = sf.readline()
	while line:
		words = line.split()
		words[0] = dot_translate(words[0])
		of.write('\t'.join(words) + '\n')
		line = sf.readline()

	sf = codecs.open(ifn2, 'r', 'utf-8')
	line = sf.readline()
	while line:
		words = line.split()
		words[0] = dot_translate(words[0])
		of.write('\t'.join(words) + '\n')
		line = sf.readline()

	sf = codecs.open(ifn3, 'r', 'utf-8')
	line = sf.readline()
	while line:
		words = line.split()
		words[0] = dot_translate(words[0])
		of.write('\t'.join(words) + '\n')
		line = sf.readline()


def dot_translate(word):
	word = word.replace(u'.', u'。')
	word = word.replace(u',', u'，')
	word = word.replace(u'?', u'？')
	word = word.replace(u'!', u'！')
	word = word.replace(u':', u'：')
	word = word.replace(u'(', u'（')
	word = word.replace(u')', u'）')
	word = word.replace(u'%', u'％')
	word = word.replace(u'/', u'／')

	return word

if __name__ == '__main__':
	translate_selected_words('../data/selected-words/selected-unigrams', '../data/selected-words/selected-bigrams', '../data/selected-words/selected-trigrams', '../data/selected-words/converted-grams')
