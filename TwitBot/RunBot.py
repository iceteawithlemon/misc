
#Tweets lines from a text file
#26/08/13
#by iceteawithlemon
#using python-twitter & python 2.7

import twitter

#Logs in with your developer credentials
#Replace these with your details
c_k='Consumer Key'
c_s='Consumer Secret'
a_t_k='Access Token Key'
a_t_s='Access Token Secret'
api = twitter.Api(consumer_key=c_k,
consumer_secret=c_s, access_token_key=a_t_k, access_token_secret=a_t_s)
print "\nSuccesfully authentificated.\n"

#Opens text file and creates a list with each line of the file as an element. Checks if any tweets are too long.
t=open('totweet.txt', 'r')
totweet=t.read()
t.close()
tweetList=totweet.split("\n")
for tweet in tweetList:
	if len(tweet)>139:
		print "This tweet is too long! Please shorten it!\n"
		print tweet, "\n"
print "Text file is ready, about to fetch existing tweets from timeline.\n"

#Fetches tweets on timeline, turns it into a usable format, and then into a list.
statusesRaw = api.GetUserTimeline("Facts_Bot", count=20)
statuses=[]
for status in statusesRaw:
        tweet=str(status.text.encode("utf-8", "ignore"))
	statuses.append(tweet)
print "List of existing tweets ready, about to try and tweet.\n"

#Checks if first element in list has already been tweeted (prepared in the previous bit of code). If it has been tweeted, then it checks the next thing to be tweeted, if not it tweets it and stops.
Tweeted=False
i=0
while not Tweeted and i<len(tweetList):
        if i==0:
                tweetList[i]=tweetList[i][3:]
	if tweetList[i] not in statuses:
		print "I am going to tweet this now:\n"
		print tweetList[i], "\n"
		justTweeted=api.PostUpdate(tweetList[i])
		print "I have now tweeted this:\n"
		print justTweeted.text
		Tweeted=True
	else:
		i+=1
if i>len(tweetList):
	print "Everything in this file has already been tweeted: please add new tweets to totweet.txt"
