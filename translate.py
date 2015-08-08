#!/usr/bin/python
# -*- coding: utf-8 -*-

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import string

class FrequencyCorpus:
	def __init__(self):
		self.frequencies = {}
		with open('lemma.num.txt') as corpus_file:
			for line in corpus_file.readlines():
				tokens = line.split()
				self.frequencies[tokens[2]] = tokens[1]

		self.found = 0
		self.not_found = 0

	def get_frequency(self, word):
		if word in self.frequencies:
			self.found += 1
			return self.frequencies[word]
		else:
			self.not_found += 1
			#print(word)
			return 0

	def get_rate(self):
		return float(self.not_found)/float(self.found)

def get_frequency(word):
	return 1

def get_translation(word):
	return ["translated"]

f_out = open('out.txt', 'w+')

frequencyCorpus = FrequencyCorpus()
lemmatizer = WordNetLemmatizer()
punct = set(string.punctuation)

def translate_fun(orig_text, translated_text):
	orig_tokens = word_tokenize(orig_text)
	freqdist = FreqDist(orig_tokens)
	freqdist.pprint()
	translated_tokens = translated_text.split(' ')
	for orig_token in orig_tokens:
		if not orig_token in punct:
			lemma = lemmatizer.lemmatize(orig_token).lower()
			#print (orig_tokens[i])
			#print(lemma)
			frequency = frequencyCorpus.get_frequency(lemma)

	print(frequencyCorpus.get_rate())



f1 = open('CHAPTER I. Down the Rabbit-Hole.txt', encoding='utf-8')
f2 = open('Глава I. ВНИЗ ПО КРОЛИЧЬЕЙ HOPE.txt', encoding='utf-8')

#translate_fun(f1.read(), f2.read())