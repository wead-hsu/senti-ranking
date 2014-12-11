#!/usr/bin/python
#encoding=utf-8
import codecs
import json

def is_same(word):
	is_chinese = True
	is_same = True
	if word[0] >= u'\u4e00' and word[0] <= u'\u9fa5':
		is_chinese = True
	else:
		is_chinese = False
	
	for char in word:
		if char >= u'\u4e00' and char <= u'\u9fa5':
			#print '1'
			if not is_chinese:
				is_same = False
				break
		else:
			#print '0'
			if is_chinese:
				is_same = False
	
	return is_same

def gen_word_list(ifn, pfn, ofn, tfn, hfn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	pf = codecs.open(pfn, 'r', 'utf-8')
	of = codecs.open(ofn, 'w', 'utf-8')
	tf = codecs.open(tfn, 'w', 'utf-8')
	hf = codecs.open(hfn, 'w', 'utf-8')

	stop_words = set()
	line = pf.readline()
	while line:
		stop_words.add(line.strip())
		line = pf.readline()

	line = sf.read()
	comments = json.loads(line)
	
	unigrams = {}
	for comment in comments:
		seg_res = comment['content'][0]
		for word in seg_res:
			if word not in stop_words and is_same(word) and word.strip():
				unigrams[word] = unigrams.get(word, 0) + 1
	
	bigrams = {}
	for comment in comments:
		seg_res = comment['content'][0]
		for idx in range(len(seg_res) - 1):
			word = seg_res[idx] + seg_res[idx+1]
			if seg_res[idx] not in stop_words and seg_res[idx+1] not in stop_words and is_same(word) and word.strip():
				bigrams[word] = bigrams.get(word, 0) + 1
	
	trigrams = {}
	for comment in comments:
		seg_res = comment['content'][0]
		for idx in range(len(seg_res) - 2):
			word = seg_res[idx] + seg_res[idx+1] + seg_res[idx+2]
			if seg_res[idx] not in stop_words and seg_res[idx+1] not in stop_words and seg_res[idx+2] not in stop_words and is_same(word) and word.strip():
				trigrams[word] = trigrams.get(word, 0) + 1

	unigram_sorted = sorted(unigrams.items(), key = lambda d:d[1], reverse = True)
	bigram_sorted = sorted(bigrams.items(), key = lambda d:d[1], reverse = True)
	trigram_sorted = sorted(trigrams.items(), key = lambda d:d[1], reverse = True)
	
	for item in unigram_sorted:
		of.write(item[0] + '\t' + str(item[1]) + '\n')
	for item in bigram_sorted:
		tf.write(item[0] + '\t' + str(item[1]) + '\n')
	for item in trigram_sorted:
		hf.write(item[0] + '\t' + str(item[1]) + '\n')

if __name__ == '__main__':
	#print is_same(u'电影。')
	gen_word_list('../data/raw-data/train-translate.json', '../data/raw-data/stop-words', '../data/word-list/unigram', '../data/word-list/bigram', '../data/word-list/trigram')
