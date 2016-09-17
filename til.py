'''
Background
If you finished the previous project which compared the karma of two new comments, 
hopefully you learned a thing or two about receiving data from Reddit's API. Now you're 
going to take this a step further, and even have the opportunity to make a basic twitter bot.

Goal
Create a program that receives data from the /r/todayilearned subreddit, and looks for new 
facts that have been posted. Each time the program comes across a new fact, the fact should 
be printed into the command line. However, phrases like "TIL ", "TIL that", etc should be 
removed so the only thing that is printed is the fact.

>>New TIL API data here<<
There are a couple things to note about this since you'll more than likely be using a loop 
to check for new posts. According to Reddit's API Access Rules Page, the API pages are only 
updated once every thirty seconds, so you'll have to have your code pause for at least thirty 
seconds before it tries to find more posts. Secondly, if for some reason you decide to try 
to get data sooner than every thirty seconds, make sure to not send more than thirty requests 
per minute. That is the maximum you are allowed to do.

Subgoal Ideas
There is actually a lot you can do once your program starts receiving facts. Instead of 
simply printing the facts, here are some ideas for what you can do with them. If you currently 
do not feel like you can accomplish these ideas, feel free to come back later when you have
more experience.

Print the link to the source of the fact too.

Try to further clean up the fact by adding punctuation to the end if it is missing, 
capitalize the first word, etc.

Write the facts to a separate text file so you end up with a giant compilation of 
random facts.

Create a bot that posts the facts to twitter. This may sound hard, but it's actually pretty 
simple by using the "Python Twitter Tools" module and following the guide posted here. 
Remember, the maximum amount of characters you can use in a tweet is only 140, so you'll 
have to filter out facts that are longer than that.

By now you should be pretty familiar with python, so if you get ideas for improving your 
program, go for it!'''

# here are my imports
import urllib2
import json
from time import sleep
import twitter



# empty list to store the facts
fact_list = []

API_key = 'rq1elvuOIkwmIvjqtIQddm3NX'
API_secret = 'uZ5IVrpVS47tzY8Q0MdZhI8IpzlcvwJISgJeddyFzgKqecchoq'

Access_token = '773972046585982977-JoDlGk8Eyfcl76BHIIacI0wc7wpMN0w'
Access_secret = 'waRzdGGYWeBP5NObxLC4FyMpEfBYVE31PliVQIELN8V5K'


my_auth = twitter.OAuth(Access_token, Access_secret, API_key, API_secret)
twit = twitter.Twitter(auth=my_auth)

# loop to collect and print the information
while True:
	
	# the target site
	site = "https://www.reddit.com/r/todayilearned/new/.json"
	
	# use json and urllib to load data from the site into python variable
	hdr = { 'User-Agent' : 'super happy flair bot by /u/spladug' }
	req = urllib2.Request(site, headers=hdr)
	data = json.load(urllib2.urlopen(req))
	
	#assign the title of the post to new fact
	new_fact = data['data']['children'][0]['data']['title']
	
	# split the new fact into words
	new_fact_words = new_fact.split()
	
	# create a list of words to always remove from the fact
	erase_words = ["TIL", "TIL:"]
	
	# list comprehension to print all the words not in the erase list to result words
	result_words = [word for word in new_fact_words if word not in erase_words]
	
	# gets the first word to do further checks on it
	first_word = result_words[0]
	
	# if the first word is any of the following, remove it from the string
	if first_word == "that" or first_word == "That" or first_word == "TIL-that" or first_word == "of":
		result_words.remove(first_word)
		
	# now join the words back together
	result = ' '.join(result_words)
	
	# capitalizes the first word in the string 
	result = ' '.join(word[0].upper() + word[1:] for word in result.split())
	
	# if it doesn't end with a period or exclamation point, add a period
	if (result.endswith(".") == False) and (result.endswith("!") == False):
		result += "."
		
	# if the fact isn't in the list, add it, and print it out to the terminal, otherwise do nothing
	if result not in fact_list:
		fact_list.append(result)
		print "\nFact:",
		print result
		print "\nAnd here is a link...",
		result_link = data['data']['children'][0]['data']['url']
		print result_link
		
	# print the facts to facts.txt if not already there
	f = open('facts.txt','r+')
	existing_facts = f.read()
	if result not in existing_facts:
		f.write(result+"\n\n")
		if len(result) < 140:
			twit.statuses.update(status=result)
	f.close()
	
	
	

			
	# wait 35 seconds to execute again
	sleep(35)
	


