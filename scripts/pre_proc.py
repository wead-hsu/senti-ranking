#!/usr/bin/python

import xml.etree.ElementTree as etree
import codecs
import jieba.posseg as pseg
import sys
import json

def pre_proc(ifn, ofn):
	sf = open(ifn)
	of = codecs.open(ofn, 'w', 'utf-8')

	text = sf.read()
	root = etree.fromstring(text)

	'''
	commnets:
		val = {id: '', movie_id: '', rating: '', content: ''}
	'''
	comments = []
	for comment_xml in root.getchildren():
		comment = {}
		for attr in comment_xml.attrib.keys():
			comment[attr] = comment_xml.attrib[attr]
		for attr in comment_xml:
			if attr.tag != 'content':
				comment[attr.tag] = attr.text.strip()
			else:
				comment[attr.tag] = []
				seg_res = []
				pos_res = []
				seg_list = pseg.cut(attr.text.strip())
				for seg in seg_list:
					if seg.word.strip():
						seg_res.append(seg.word.encode('utf-8'))
						pos_res.append(seg.flag)
				comment[attr.tag].append(seg_res)
				comment[attr.tag].append(pos_res)
		comments.append(comment)

	of.write(json.dumps(comments, 'utf-8'))

def print_comments(comments):
	of = codecs.open('out', 'w', 'utf-8')

	for comment in comments:
		for word in comment['content'][0]:
			of.write(word + ' ')
		of.write('\n')

if __name__ == '__main__':
	pre_proc('../data/raw-data/train.xml', '../data/raw-data/train.json')
