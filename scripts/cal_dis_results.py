#!/usr/bin/python

import codecs
import sys
import numpy as np

def cal_results(ifn):
	sf = codecs.open(ifn, 'r', 'utf-8')

	line = sf.readline()
	error = 0.0
	line_cnt = 0
	while line:
		line_cnt += 1
		words = line.split()
		numbers = []
		for word in words:
			numbers.append(float(word))
		
		answer = 1

		if numbers[2] == 0:
			answer = numbers[0]
		else:
			max_idx = 2
			sec_idx = 2
			for i in range(2,7):
				if numbers[max_idx] < numbers[i]:
					sec_idx = max_idx
					max_idx = i
				elif numbers[sec_idx] < numbers[i]:
					sec_idx = i

			if np.abs(max_idx - 1 - numbers[0]) > 2.5:
				answer = numbers[0]
			else:
				answer = max_idx - 1
			
		error += (numbers[7] - answer) * ( numbers[7] - answer)
		print answer
		line = sf.readline()
	
	print error/line_cnt

cal_results('../data/feature/word-feature-not-ext-slt')
