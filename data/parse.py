#!/usr/bin/env python3

import sys
import re
import html.parser as htmlparser


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

def main(functions):
	if(not functions):
		functions = ["correct_lines","deserialize_html","remove_links"]
	dataset = open("tweets.log","r").read().splitlines()
	for i in functions:
		print("Working on: "+i)
		if(globals()[i]):
			dataset = globals()[i](dataset)
	
	open("tweets.processed.log","w").write("\n".join(dataset))
	print("Job's done!")

if __name__ == "__main__":
	main(sys.argv[1:])