import json, companies, time, re
from twittersearch import twitterreq
from pprint import pprint as pp

# used for the sentiment file
def sent_dict(file):
	dict = {}
	for line in file:
		(key,val) = line.split('\t')
		dict[key] = int(val.encode('ascii','ignore'))
	return dict

sentiment_file = open('AFINN-111.txt')
sdict = sent_dict(sentiment_file)

def sentiment(company_id,company,since_id,max_id,query):
	
	### store the formatted data + score into this list (list of rows)
	data = []

	### setup twitter query parameters ###
	params = {}
	params['q'] = query
	params['result_type'] = 'recent' # only want recent
	params['count'] = 100 # this is the max possible as of 7/25/13
	params['lang'] = 'en' # english only
	#params['since_id'] = since_id # youngest (larger id)
	params['max_id'] = max_id # oldest (smaller id)
	
	### hit twitter with the query params ###
	response = twitterreq(params)
	
	### now go through each of the tweets ###
	for line in response:
		#print line
		statuses = json.loads(line)['statuses'] # there is only 1 line
		
		### go through each tweet, grab the info and calculate a score ###
		for status in statuses:
		
			### grab info from tweet status ###
			screen_name =  status['user']['screen_name'].encode('ascii','ignore')
		 	#tweet = (status['text'].encode('utf-8')).encode('ascii','ignore')
			tweet = status['text'].encode('ascii','ignore')
		 	followers = int(status['user']['followers_count'])
		 	retweets = int(status['retweet_count'])
		 	tweet_time = time.strftime('%Y,%m,%d,%H,%M,%S', time.strptime(status['created_at'],'%a %b %d %H:%M:%S +0000 %Y')) # convert from twitter format to google format
			#tweet_time = status['created_at']
			id = str(status['id']) # tweet id
			#print id
			if status['geo'] is None:
				geo = ''
			else:
				geo = str(status['geo'])
		 	
			### start a new score and term counter for this tweet ###
			score = 0 #
			term_count = 0
			
			### score the tweet and count the terms ###
			for term in sdict:
				regex_term = '\\b%s\\b' % term # use this to find exact term for example searching for 'Noni' in the string 'Nonification' will fail but pass for the string 'Tahitian Noni'
				fnd = re.findall(regex_term,tweet,flags=re.IGNORECASE)
				if len(fnd) > 0:
					score = score + sdict[term] # add the score
					term_count += 1 # track number of terms found
					
			### populate the data list with this record ###
			datarow = [] 
			datarow.append(company_id)
			datarow.append(company)
			datarow.append(screen_name)
			datarow.append(tweet)
			datarow.append(tweet_time)
			datarow.append(followers)
			datarow.append(retweets)
			datarow.append(score)
			datarow.append(geo)
			datarow.append(term_count)
			datarow.append(id)
			data.append(datarow)
			
	return data

# d = sentiment(1168,'Xango -music',0)
# for row in d:
	# print row

