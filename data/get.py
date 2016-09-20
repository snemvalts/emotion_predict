import twitter
import re
import requests
import random
import time


apikey_file = open("apikey.txt", "r")
consumer_key = apikey_file.readline().rstrip()
consumer_secret = apikey_file.readline().rstrip()

#create a new app, get the
access_token_file = open("accesstoken.txt", "r")
access_token = access_token_file.readline().rstrip()
access_token_secret = access_token_file.readline().rstrip()

dictionary = requests.get('https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa.txt').text.splitlines()
stopwords = open("stopwords.txt", "r").read().splitlines()
dictionary = [i for i in dictionary if i not in stopwords]

random.shuffle(dictionary)


emojiPattern = re.compile('[\U0001f600-\U0001f640]')

api = twitter.Api(	
					consumer_key = consumer_key,
					consumer_secret = consumer_secret,
					access_token_key = access_token,
					access_token_secret = access_token_secret	
				)

def main():

	tweetsFile = open("tweets.log","a")	
	for i in dictionary[:100]:
		print("=============")
		print("Word: "+str(i))
		print("Progress: "+str((dictionary.index(i)+1)/100*100)+"%")
		tweets = performSearch(i,5,None)
		for tweet in tweets:
			#Tweet Text Goes Here ;; 😂,😂,😂
			tweetsFile.write(str(tweet[0])+" ;; "+str(','.join(tweet[1])) + "\n")
			#tweetsFile.write("AAAAAAAAAAA")
		tweetsFile.flush()
		print("Done Writing")
		print("=============")

	#print(data)

	#print(api.GetSearch(term="test")[0].AsDict()["text"])

def performSearch(term,times,ID):
	if(times <= 0):
		return []
	print("Iteration #"+str(times))
	data = []
	lastId = 0
	try:
		if(ID):
			search = api.GetSearch(term=term, count=100, max_id=ID-1)
		else:
			search = api.GetSearch(term=term, count=100)
	except twitter.error.TwitterError as e:
		print("Exception! "+e[0].message)
		if(e[0].code == 88):
			print("Going to sleep")
			for i in range(0,15):
				time.sleep(60)
				print("Have slept "+str(i)+" minutes")


	for i in search:
		text = i.AsDict()["text"]
		hasEmoji = emojiPattern.findall(text)
		if hasEmoji and not text.startswith("RT"):
			#print(text)
			data.append([re.sub(emojiPattern,'',text),hasEmoji])
			lastId = i.id

	#remove last otherwise twitter's api returns the tweet last batch ended with
	if(len(data) > 1):
		del data[-1]

	return data + performSearch(term, times-1, lastId)

if __name__ == '__main__':
	main()