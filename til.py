import urllib2
import json
from time import sleep
import twitter



# empty list to store the facts
fact_list = []

API_key = ''
API_secret = ''

Access_token = ''
Access_secret = ''


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
	


