import twitter
import re
import requests


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

emojiPattern = re.compile('[\U0001f600-\U0001f640]')

api = twitter.Api(	
					consumer_key = consumer_key,
					consumer_secret = consumer_secret,
					access_token_key = access_token,
					access_token_secret = access_token_secret	
				)

def main():
	performSearch("test",3,None)
	#print(data)

	#print(api.GetSearch(term="test")[0].AsDict()["text"])õ

def performSearch(term,times,ID):
	if(times <= 0):
		return []

	data = []
	lastId = 0
	print("==================================================")
	print("RUN "+str(times))
	print("==================================================")

	if(ID):
		search = api.GetSearch(term=term, count=100, max_id=ID)
	else:
		search = api.GetSearch(term=term, count=100)


	for i in search:
		text = i.AsDict()["text"]
		hasEmoji = emojiPattern.findall(text)
		if hasEmoji and not text.startswith("RT"):
			print(text)
			data.append([re.sub(emojiPattern,'',text),hasEmoji])
			lastId = i.id

	#remove last otherwise twitter's api returns the tweet last batch ended with
	if(len(data) > 1):
		del data[-1]

	return data + performSearch(term, times-1, lastId)

if __name__ == '__main__':
	main()