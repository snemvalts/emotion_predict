import sys
from statistics import mode
import string


def distribution(dataset):
	labels = {}
	for i in dataset:
		for j in i[1]:
			if(j in labels):
				labels[j] += 1
			elif(j.upper() == j):
				labels[j] = 1

	print("DISTRIBUTION")
	for key in labels:
		print("================")
		print("Key: "+key)
		print("Tweets with: "+str(labels[key]))
		print("Percentage in tweets: "+str(labels[key]/len(dataset)*100)+"%")


def average(dataset):
	labels = {}
	for i in dataset:
		for j in i[1]:
			if(j in labels):
				labels[j] += i[1].count(j)
			elif(j.upper() == j):
				labels[j] = 1

	print("AVERAGE")
	for key in labels:
		print("================")
		print("Key: "+key)
		print("Amount: "+str(labels[key]))
		print("Average amount in tweets: "+str(labels[key]/len(dataset)))


def letters(dataset):
	positive = ["JOY","LOVE"]
	negative = ["SAD","FEAR","CONTEMPT","ANGER"]
	max_diff = max_diff_letter = 0
	print("LETTERS")
	for letter in list(string.ascii_lowercase):
		pos_count = neg_count = pos_letter = neg_letter = 0
		print("Working on: "+letter)
		for i in dataset:
			try:
				common = mode(i[1])
			except:
				continue
			if(common in positive):
				pos_count += 1
				pos_letter += i[0].lower().count(letter)
			elif(common in negative):
				neg_count += 1
				neg_letter += i[0].lower().count(letter)
		diff = abs((pos_letter/pos_count)-(neg_letter/neg_count))
		if(diff > max_diff):
			max_diff = diff
			max_diff_letter = letter

	print("Max_diff: "+str(max_diff))
	print("Max_diff_letter: "+max_diff_letter)


def main(functions):
	if(not functions):
		functions = ["distribution","average","letters"]
	dataset = open("data/tweets.processed.log","r").read().splitlines()
	dataset = [i.split(" ;; ") for i in dataset]
	for i,v in enumerate(dataset):
		dataset[i][1] = dataset[i][1].split(",")
	for i in functions:
		if(globals()[i]):
			globals()[i](dataset)
			print("================")
			print("================")


if __name__ == "__main__":
	main(sys.argv[1:])