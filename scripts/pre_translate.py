#!/usr/bin/python
#encoding=utf-8

import xml.etree.ElementTree as etree
import codecs
import jieba.posseg as pseg
import sys
import json

def pre_proc(ifn, efn, tfn, ofn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	ef = codecs.open(efn, 'r', 'utf-8')
	tf = codecs.open(tfn, 'r', 'utf-8')
	of = codecs.open(ofn, 'w', 'utf-8')

	trans_dict = {}
	eline = ef.readline()
	tline = tf.readline()
	while eline:
		trans_dict[eline.strip()] = tline.strip()
		eline = ef.readline()
		tline = tf.readline()

	trans_dict[u'.'] = u'。'
	trans_dict[u','] = u'，'
	trans_dict[u'?'] = u'？'
	trans_dict[u'!'] = u'！'
	trans_dict[u':'] = u'：'
	trans_dict[u'('] = u'（'
	trans_dict[u')'] = u'）'
	trans_dict[u'%'] = u'％'
	trans_dict[u'/'] = u'／'

	line = sf.readline()

	comments = json.loads(line)

	for comment in comments:
		seg_res = comment['content'][0]
		for idx in range(len(seg_res)):
			if seg_res[idx] in trans_dict.keys():
				seg_res[idx] = trans_dict[seg_res[idx]]

	of.write(json.dumps(comments))

if __name__ == '__main__':
	pre_proc('../data/raw-data/train.json', '../data/english/english-words' ,'../data/english/english-translate', '../data/raw-data/train-translate.json')
