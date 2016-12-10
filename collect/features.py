import sys
import csv
import os
import math
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
		#TODO: this is the wildcard, modify this
		for j in entry_arr:
			emotion_dict[j] = i[index]

	return emotion_dict


def normalize(arr):
	max_arr = max(arr)
	min_arr = min(arr)
	return [(i-min_arr)/(max_arr-min_arr) for i in arr]


def punctuation(dataset):
	return amount_of_character(dataset,["!","?","."])


def amount_of_i(dataset):
	return amount_of_character(dataset,["i","I"])


def summed_words(dataset):
	pos = pos_words(dataset)
	neg = neg_words(dataset)
	summed = []
	for it, i in enumerate(pos):
		summed.append(i+-1*neg[it])

	return normalize(summed)

def words_competition(dataset):
	pos = pos_words(dataset)
	neg = neg_words(dataset)
	total = []
	for p, n in zip(pos,neg):
		total.append(p+n)

	return normalize(total)

def pos_words(dataset):
	return_arr = []
	dictionary = generate_wordnet_dict("positive")
	for i in dataset:
		scores = []
		for j in i[0].split(" "):
			#TODO: this is pretty early, maybe average or something else?
			if(j in dictionary):
				scores.append(float(dictionary[j]))
		
		if(len(scores) == 0):
			return_arr.append(0)
		else:
			return_arr.append(sum(scores)/len(scores))

	return normalize(return_arr)


def neg_words(dataset):
	return_arr = []
	dictionary = generate_wordnet_dict("negative")
	for i in dataset:
		scores = []
		for j in i[0].split(" "):
			#TODO: this is pretty early, maybe average or something else?
			if(j in dictionary):
				scores.append(float(dictionary[j]))
		
		if(len(scores) == 0):
			return_arr.append(0)
		else:
			return_arr.append(sum(scores)/len(scores))


	return normalize(return_arr)


def summed_real(dataset):
	pos = pos_real(dataset)
	neg = neg_real(dataset)
	summed = []
	for it, i in enumerate(pos):
		summed.append(i+-1*neg[it])

	return normalize(summed)


def real_competition(dataset):
	pos = pos_real(dataset)
	neg = neg_real(dataset)
	total = []
	for p, n in zip(pos,neg):
		total.append(p+n)

	return normalize(total)

def pos_real(dataset):
	positive = ["JOY","LOVE"]
	return_arr = []
	for i in dataset:
		pos = 0 
		for it,j in enumerate(i[1]):
			if(j in positive):
				pos+=i[2][it]
		return_arr.append(pos/len(i[1]))


	return normalize(return_arr)


def neg_real(dataset):
	negative = ["SAD","FEAR","CONTEMPT","ANGER"]
	return_arr = []
	for i in dataset:
		neg = 0
		for it,j in enumerate(i[1]):
			if(j in negative): neg+=i[2][it]
		return_arr.append(neg/len(i[1]))

	return normalize(return_arr)

def amount_of_character(dataset,letterset):
	return_arr = []
	for i in dataset:
		for mark in letterset:
			try:
				return_arr.append(math.log10(i[0].count(mark)))
			except ValueError:
				#can't take log of 0
				return_arr.append(0)
	return normalize(return_arr)

def main(functions):
	if(not functions):
		#functions = ["summed_words","pos_real","neg_real","punctuation","amount_of_i"]
		#functions = ["summed_words","words_competition","summed_real","real_competition","punctuation","amount_of_i"]
		#functions = ["summed_words","punctuation","amount_of_i","summed_real"]
		functions = ["pos_words","neg_words","amount_of_i","punctuation","pos_real","neg_real"]
	dataset = open(os.path.join(current_dir,"data/tweets.processed.log"),"r").read().splitlines()
	dataset = [i.split(" ;; ") for i in dataset]
	for i,v in enumerate(dataset):
		dataset[i][1] = dataset[i][1].split(",")
		dataset[i][2] = [float(j) for j in dataset[i][2].split(",")]

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
			if(isinstance(i[j],float)):
				featureset[j].append("%.2f" % i[j])
			else:
				featureset[j].append(i[j])

	f = open(os.path.join(current_dir,"data/tweets.features.csv"),"w")
	writer = csv.writer(f)
	writer.writerow(functions)
	writer.writerows(featureset)

	print("Job's done!")


if __name__ == "__main__":
	main(sys.argv[1:])