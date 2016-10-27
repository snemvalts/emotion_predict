import sys


def distribution(dataset):
	labels = {}
	for i in dataset:
		for j in i[1]:
			if(j in labels):
				labels[j] += 1
			elif(j.upper() == j):
				labels[j] = 0

	print("DISTRIBUTION")
	for key in labels:
		print("================")
		print("Key: "+key)
		print("Amount: "+str(labels[key]))
		print("Percentage in tweets: "+str(labels[key]/len(dataset)*100)+"%")
	print("================")

def exclusivity(dataset):
	labels = {}
	for i in dataset:
		for j in i[1]:
			if(j in labels):
				labels[j] += 1
			elif(j.upper() == j):
				labels[j] = 0

	print("DISTRIBUTION")
	for key in labels:
		print("================")
		print("Key: "+key)
		print("Amount: "+str(labels[key]))
		print("Percentage in tweets: "+str(labels[key]/len(dataset)*100)+"%")
	print("================")
	
def main(functions):
	if(not functions):
		functions = ["distribution"]
	dataset = open("data/tweets.processed.log","r").read().splitlines()
	dataset = [i.split(" ;; ") for i in dataset]
	for i,v in enumerate(dataset):
		dataset[i][1] = dataset[i][1].split(",")
	for i in functions:
		print("Working on: "+i)
		if(globals()[i]):
			globals()[i](dataset)



if __name__ == "__main__":
	main(sys.argv[1:])