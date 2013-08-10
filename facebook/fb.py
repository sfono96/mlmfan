import requests
from pprint import pprint as pp
from guess_language import guessLanguage as gl

#Your APP ID. You Need to register the application on facebook
#http://developers.facebook.com/
FACEBOOK_APP_ID = 606056719434426
FACEBOOK_APP_SECRET = 'ddb002bfd42ac53aa82c96045516b1ee' # just for reference

# handle authentication
url = 'https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (str(FACEBOOK_APP_ID), FACEBOOK_APP_SECRET)
r = requests.get(url) 
access_token = r.text.split('=')[1]

# now search for whatever
query = 'Xango'
limit = 1000
searchurl = 'https://graph.facebook.com/search?q=%s&type=post&access_token=%s&limit=%s&locale=en_US' % (query,access_token,str(limit))
#print searchurl
rs = requests.get(searchurl)
posts = rs.json()['data']
#print len(posts)
legit_posts = 0
for p in posts:
	m = ''
	if 'message' in p.keys(): # make sure there is a post
		# no category then go ahead and pass
		if 'category' not in p['from'].keys():
			m = p['message'].encode('ascii','ignore')
		# if category check to see that not the spammy category (Bank/financial institution)
		elif p['from']['category'] <> 'Bank/financial institution':
			m = p['message'].encode('ascii','ignore')
		
		# now check that it is in english
		if gl(m) == 'en':
			legit_posts += 1
			print legit_posts, m

print legit_posts
	


