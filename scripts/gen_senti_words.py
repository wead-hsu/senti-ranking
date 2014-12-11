#!/usr/bin/python

import codecs
import sys
import json

def load_feature_values(ifn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	feature_values = set()
	line = sf.readline()

	while line:
		feature_values.add(line.split()[0])
		line = sf.readline()

	return feature_values

def load_adj_values(ifn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	line = sf.readline()

	comments = json.loads(line)
	adj_words = set()
	for comment in comments:
		content = comment['content']
		seg_res = content[0]
		pos_res = content[1]
		res_len = len(seg_res)
		idx = 0
		while idx < res_len:
			if idx + 1 < res_len and pos_res[idx][0] == u'z' and pos_res[idx + 1][0] == u'a':
				adj_words.add(seg_res[idx] + seg_res[idx+1])
				idx += 2
			elif idx + 1 < res_len and pos_res[idx][0] == u'd' and pos_res[idx + 1][0] == u'a':
				adj_words.add(seg_res[idx] + seg_res[idx + 1])
				idx += 2
			elif idx < res_len and pos_res[idx][0] == u'a':
				adj_words.add(seg_res[idx])
				idx += 1
			else:
				idx += 1

	return adj_words

def cal_senti_words(ifn, words, ofn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	of = codecs.open(ofn, 'w', 'utf-8')
	line = sf.readline()
	comments = json.loads(line)
	
	words_cnt = {}
	for word in words:
		words_cnt[word] = {}
		words_cnt[word]['1'] = 0
		words_cnt[word]['2'] = 0
		words_cnt[word]['3'] = 0
		words_cnt[word]['4'] = 0
		words_cnt[word]['5'] = 0
	
	for comment in comments:
		content = comment['content']
		seg_res = content[0]
		pos_res = content[1]
		rating = comment['rating']
		res_len = len(seg_res)
		idx = 0
		while idx < res_len:
			if idx + 2 < res_len and seg_res[idx] + seg_res[idx + 1] + seg_res[idx + 2] in words:
				word = seg_res[idx] + seg_res[idx+1] + seg_res[idx+2]
				words_cnt[word][rating] += 1
				idx += 1
			elif idx + 1 < res_len and seg_res[idx] + seg_res[idx+1] in words:
				word = seg_res[idx] + seg_res[idx+1]
				words_cnt[word][rating] += 1
				idx += 1
			elif idx < res_len and seg_res[idx] in words:
				word = seg_res[idx]
				words_cnt[word][rating] += 1
				idx += 1
			else:
				idx += 1

	for word in words:
		sum_cnt = 0
		sum_cnt += words_cnt[word]['1']
		sum_cnt += words_cnt[word]['2']
		sum_cnt += words_cnt[word]['3']
		sum_cnt += words_cnt[word]['4']
		sum_cnt += words_cnt[word]['5']

		of.write(word + '\t' + str(words_cnt[word]['1']) + '\t' + str(words_cnt[word]['2']) + '\t' + str(words_cnt[word]['3']) + '\t' + str(words_cnt[word]['4']) + '\t' + str(words_cnt[word]['5']) + '\t'+ str(sum_cnt) + '\n')

	return

mutals = load_feature_values('../data/selected-words/converted-grams')
adjs = load_adj_values('../data/raw-data/train-translate.json')
words = mutals | adjs
cal_senti_words('../data/raw-data/train-translate.json', words, '../data/senti-words/mutals-and-adj')
