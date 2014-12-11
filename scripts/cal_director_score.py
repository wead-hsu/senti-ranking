#!/usr/bin/python

import json
import codecs
import xml.etree.ElementTree as etree
import sys

def cal_director_score(ifn, mfn, ofn):
	sf = codecs.open(ifn, 'r', 'utf-8')
	comments = json.loads(sf.readline())
	of = codecs.open(ofn, 'w', 'utf-8')
	mf = open(mfn)
	text = mf.read()
	movies = etree.fromstring(text)

	movie_director = {}
	movie_score = {}
	for movie in movies:
		for attr in movie:
			if attr.tag == 'id':
				movie_id = attr.text
			if attr.tag == 'director':
				director = attr.text
			if attr.tag == 'rating':
				rating = attr.text
		movie_director[movie_id] = director
		movie_score[movie_id] = rating

	director_score = {}
	for item in movie_director.items():
		print item[1]
		director_score[item[1]] = [0.0, 0.0]

	for comment in comments:
		rating = float(comment['rating'])
		movie_id = comment['movie_id']
		director_score[movie_director[movie_id]][0] += rating
		director_score[movie_director[movie_id]][1] += 1
		
	for movie in movie_director.keys():
		of.write(movie + '\t' +  movie_director[movie] + '\t' + str(director_score[movie_director[movie]][0]/director_score[movie_director[movie]][1]) + '\t' + movie_score[movie] + '\n')

cal_director_score('../data/raw-data/train-translate.json', '../data/raw-data/movies.xml', '../data/feature/director_score')
