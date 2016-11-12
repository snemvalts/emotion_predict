from guess_language import guess_language
import twitter
import re
import requests
import random
import time
import itertools
import os
current_dir = os.path.dirname(__file__)

apikey_file = open(os.path.join(current_dir,"auth/apikey.txt"), "r")
consumer_key = apikey_file.readline().rstrip()
consumer_secret = apikey_file.readline().rstrip()

#create a new app, get the
access_token_file = open(os.path.join(current_dir,"auth/accesstoken.txt"), "r")
access_token = access_token_file.readline().rstrip()
access_token_secret = access_token_file.readline().rstrip()

dictionary = requests.get('https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa.txt').text.splitlines()
stopwords = open(os.path.join(current_dir,"../supplemental/stopwords.txt"), "r").read().splitlines()
dictionary = [i for i in dictionary if i not in stopwords]

random.shuffle(dictionary[:1000])


emoji_pattern = re.compile('[\U0001f600-\U0001f640]')

api = twitter.Api(	
					consumer_key = consumer_key,
					consumer_secret = consumer_secret,
					access_token_key = access_token,
					access_token_secret = access_token_secret	
				)
#api.PostUpdate('Test post, please ignore!')

def main():
	tweet_file = open(os.path.join(current_dir,"data/tweets.log"),"a")	
	for i in dictionary[:100]:
		print("=============")
		print("Word: "+str(i))
		print("Progress: "+str((dictionary.index(i)+1)/100*100)+"%")
		tweets = perform_search(i,10,None)
		for tweet in tweets:
			#Tweet Text Goes Here ;; 😂,😂,😂
			tweet_file.write(str(tweet[0].rstrip().strip("\n"))+" ;; "+str(','.join(tweet[1])) + "\n")
			#tweet_file.write("AAAAAAAAAAA")
		tweet_file.flush()
		print("Done Writing")

	#print(data)

	#print(api.GetSearch(term="test")[0].AsDict()["text"])


def perform_search(term,times,ID):
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
		print(e.message[0]["message"])
		if(e.message[0]["code"] == 88):
			print("Going to sleep")
			for i in range(0,15):
				time.sleep(60)
				print("Have slept "+str(i+1	)+" minutes")
			
			return []


	for i in search:
		text = i.AsDict()["text"]
		has_emoji = emoji_pattern.findall(text)
		if has_emoji and not text.startswith("RT") and guess_language(text) == "en":
			#print(text)
			data.append([re.sub(emoji_pattern,'',text),has_emoji])
			lastId = i.id

	#remove last otherwise twitter's api returns the tweet last batch ended with
	if(len(data) > 1):
		del data[-1]

	return_arr = data + performSearch(term, times-1, lastId)
	return_arr.sort()
	return list(return_arr for return_arr,_ in itertools.groupby(return_arr))


if __name__ == '__main__':
	main()