import sys
import csv

def a(f):
	return ["a","b","c"]

def b(f):
	return [1,2,3]
def main(functions):
	if(not functions):
		functions = ["a","b"]
	dataset = open("data/tweets.processed.log","r").read().splitlines()
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

	f = open("data/tweets.features.csv","w")
	writer = csv.writer(f)
	writer.writerows(featureset)

	print("Job's done!")


if __name__ == "__main__":
	main(sys.argv[1:])