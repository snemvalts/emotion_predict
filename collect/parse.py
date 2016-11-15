#!/usr/bin/env python3

import sys
import re
import html.parser as htmlparser
import csv
from collections import Counter
import math
import os
current_dir = os.path.dirname(__file__)

def correct_lines(dataset):
	return_arr = []
	it = 1
	buffer = [] 
	for i in dataset:
		if(";;" in i):
			if(buffer):
				buffer.append(i)
				return_arr.append(" ".join(buffer).rstrip())
				buffer = []
			else:
				return_arr.append(i)
		else:
			buffer.append(i)
		it+=1

	return return_arr

def remove_stopwords(dataset):
	stopwords = open(os.path.join(current_dir,"../supplemental/stopwords.txt"), "r").read().splitlines()
	return_arr = []
	print("> This WILL take a long time")
	percentages = [math.floor(i/10*len(dataset)) for i in range(0,10)]
	for j,i in enumerate(dataset):
		string = i
		if(j in percentages):
			print("> "+str(percentages.index(j)*10)+"%",end="\r")
		for word in stopwords:
			#TODO: painstakingly slow, takes 4.2x longer with this line alone
			string = string.replace(" "+word+" "," ")
			#string = string.replace(" "+word.upper()+" "," ")
			#string = string.replace(" "+word.capitalize()+" "," ")
		return_arr.append(string)

	return return_arr


def remove_unpredicted_doublesemis(dataset):
	return_arr = []
	it = 0
	for i in dataset:
		#endswith because some uwu;;$ split doesn't work properly
		if(len(i.split(";; ")) > 2) or i.endswith(";;"):
			it+=1
			continue
		else: return_arr.append(i)
	print(">"+str(it)+" were broken")
	return return_arr


def deserialize_html(dataset):
	return_arr = []
	parser = htmlparser.HTMLParser()

	for i in dataset:
		return_arr.append(parser.unescape(i))

	return return_arr


def remove_links(dataset):
	return_arr = []
	pattern = re.compile("http\S+ ")

	for i in dataset:
		return_arr.append(pattern.sub('',i))

	return return_arr


def remove_mentions(dataset):
	return_arr = []
	pattern = re.compile("\@\w+[ . ? !] ?")

	for i in dataset:
		return_arr.append(pattern.sub('',i))

	return return_arr


def assign_emotions(dataset):
	return_arr = []
	file = open(os.path.join(current_dir,"data/classification.csv"),"r")
	reader = csv.reader(file)
	emojis = { k:v for k,v,i in reader }
	file.seek(0)
	scores = { k:i for k,v,i in reader }

	for i in dataset:
		list = i.split(";; ")
		tweet_emoji = list[1].split(",")
		tweet_emoji_score = [0]*len(tweet_emoji)
		for i,emoji in enumerate(tweet_emoji):
			if(emoji in emojis):
				#assign the emotion label
				tweet_emoji[i] = emojis[emoji]
				tweet_emoji_score[i] = scores[emoji]


		#TODO: Transform the tweet_emoji array, find the most common, something like that?
		return_arr.append(list[0].rstrip()+' ;; ' + ','.join(tweet_emoji) + ' ;; ' + ','.join(map(str,tweet_emoji_score)))

	return return_arr


def remove_emoji(dataset):
	return_arr = []
	pattern = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
	for i in dataset:
		return_arr.append(pattern.sub('',i))

	return return_arr


def main(functions):
	if(not functions):
		functions = ["correct_lines","remove_stopwords","deserialize_html","remove_links","remove_mentions","remove_unpredicted_doublesemis","assign_emotions","remove_emoji"]
	dataset = open(os.path.join(current_dir,"data/tweets.log"),"r").read().splitlines()
	for i in functions:
		print("Working on: "+i)
		if(globals()[i]):
			dataset = globals()[i](dataset)
	
	open(os.path.join(current_dir,"data/tweets.processed.log"),"w").write("\n".join(dataset))
	print("Job's done!")

if __name__ == "__main__":
	main(sys.argv[1:])