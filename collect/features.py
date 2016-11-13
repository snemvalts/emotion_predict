import sys
import csv
import os
current_dir = os.path.dirname(__file__)

def generate_wordnet_dict(emotion):
	if(emotion == "positive"):
		index = 1
	elif(emotion == "negative"):
		index = 2

	words = list(csv.reader(open(os.path.join(current_dir,"../supplemental/sentiwordnet.csv"))))
	del words[0]
	emotion_dict = {}
	for i in words:
		#since some have multiple per word, for each create entry
		entry_arr = i[3:]
		for j in entry_arr:
			emotion_dict[j] = i[index]

	return emotion_dict

def normalize(arr):
	max_arr = max(arr)
	min_arr = min(arr)
	return [(i-min_arr)/(max_arr-min_arr) for i in arr]

def punctuation(dataset):
	return_arr = []
	punctuation = ["!","?","."]
	for i in dataset:
		for mark in punctuation:
			return_arr.append(i[0].count(mark))

	return return_arr


def pos_words(dataset):
	return_arr = []
	dictionary = generate_wordnet_dict("positive")
	for i in dataset:
		score = 0
		for j in i[0].split(" "):
			#TODO: this is pretty early, maybe average or something else?
			if(j in dictionary):
				score+=float(dictionary[j])
		return_arr.append(score)

	return normalize(return_arr)


def neg_words(dataset):
	return_arr = []
	dictionary = generate_wordnet_dict("negative")
	for i in dataset:
		score = 0
		for j in i[0].split(" "):
			#TODO: this is pretty early, maybe average or something else?
			if(j in dictionary):
				score+=float(dictionary[j])
		return_arr.append(score)


	return normalize(return_arr)


#TODO: modify the original parser for intensity
def pos_real(dataset):
	positive = ["JOY","LOVE"]
	return_arr = []
	for i in dataset:
		pos = 0 
		for j in i[1]:
			if(j in positive): pos+=1
		return_arr.append(pos/len(i[1]))


	return return_arr


def neg_real(dataset):
	negative = ["SAD","FEAR","CONTEMPT","ANGER"]
	return_arr = []
	for i in dataset:
		neg = 0
		for j in i[1]:
			if(j in negative): 
				neg+=1
		return_arr.append(neg/len(i[1]))

	return return_arr


def main(functions):
	if(not functions):
		functions = ["pos_words","neg_words","punctuation","pos_real","neg_real"]
	dataset = open(os.path.join(current_dir,"data/tweets.processed.log"),"r").read().splitlines()
	dataset = [i.split(" ;; ") for i in dataset]
	for i,v in enumerate(dataset):
		dataset[i][1] = dataset[i][1].split(",")
	'''
	this will be a matrix of features * n dimensions, like this
	[
		[0,1,2,3],
		[0.2,0.3,0.4]
	]
	where the first element's first feature is 0, the second feature is 0.2 etc
	'''
	featurematrix = []
	for i in functions:
		print("Working on: "+i)
		if(globals()[i]):
			featurematrix.append(globals()[i](dataset))
	
	featureset = []	
	#loop the first one, only use the index
	#append an empty array
	#loop every list in the matrix and populate it using the index-th element from each 
	for j,a in enumerate(featurematrix[0]):
		featureset.append([])
		for i in featurematrix:
			featureset[j].append(i[j])

	f = open(os.path.join(current_dir,"data/tweets.features.csv"),"w")
	writer = csv.writer(f)
	writer.writerow(functions)
	writer.writerows(featureset)

	print("Job's done!")


if __name__ == "__main__":
	main(sys.argv[1:])