#!/usr/bin/env python3

import sys
import re
import html.parser as htmlparser
import csv
from collections import Counter

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

def remove_unpredicted_doublesemis(dataset):
	return_arr = []
	it = 0
	for i in dataset:
		#endswith because some uwu;;$ split doesn't work properly
		if(len(i.split(";; ")) > 2) or i.endswith(";;"):
			print(i)
			it+=1
			continue
		else: return_arr.append(i)
	print(str(it)+" were broken")
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
	reader = csv.reader(open("classification.csv","r"))
	emojis = { k:v for k,v,i in reader }

	for i in dataset:
		list = i.split(";; ")
		tweet_emoji = list[1].split(",")

		for i,emoji in enumerate(tweet_emoji):
			if(emoji in emojis):
				#assign the emotion label
				tweet_emoji[i] = emojis[emoji]

		#TODO: Transform the tweet_emoji array, find the most common, something like that?
		#print(tweet_emoji)
		return_arr.append(list[0]+' ;; ' + ','.join(tweet_emoji))

	return return_arr



def main(functions):
	if(not functions):
		functions = ["correct_lines","deserialize_html","remove_links","remove_mentions","remove_unpredicted_doublesemis","assign_emotions"]
	dataset = open("tweets.log","r").read().splitlines()
	for i in functions:
		print("Working on: "+i)
		if(globals()[i]):
			dataset = globals()[i](dataset)
	
	open("tweets.processed.log","w").write("\n".join(dataset))
	print("Job's done!")

if __name__ == "__main__":
	main(sys.argv[1:])