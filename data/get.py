import twitter
import re

apikey_file = open("apikey.txt", "r")
consumer_key = apikey_file.readline().rstrip()
consumer_secret = apikey_file.readline().rstrip()


#create a new app, get the
access_token_file = open("accesstoken.txt", "r")
access_token = access_token_file.readline().rstrip()
access_token_secret = access_token_file.readline().rstrip()

#print(consumer_key)
#print(consumer_secret)
#print(access_token_secret)


api = twitter.Api(	
					consumer_key = consumer_key,
					consumer_secret = consumer_secret,
					access_token_key = access_token,
					access_token_secret = access_token_secret	
				)

def main():
	search = api.GetSearch(term="test", count=100)
	pattern = re.compile('[\U0001f600-\U0001f640]')
	it = 0
	for i in search:
		it+=1
		print(i.AsDict()["text"])
		print("#"+str(it))
		hasEmoji = pattern.findall(i.AsDict()["text"])
		print(hasEmoji)

	#print(api.GetSearch(term="test")[0].AsDict()["text"])õ



if __name__ == '__main__':
	main()