#!/usr/bin/env python3

import sys

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


def main(functions):
	if(not functions):
		functions = ["correct_lines"]
	dataset = open("tweets.log","r").read().splitlines()
	for i in functions:
		print("Working on: "+i)
		if(globals()[i]):
			dataset = globals()[i](dataset)
	
	open("tweets.processed.log","w").write("\n".join(dataset))
	print("Job's done!")

if __name__ == "__main__":
	main(sys.argv[1:])