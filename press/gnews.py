from pprint import pprint as pp
import urllib2, simplejson, urllib
from tagzapper import strip_tags

query = 'ACN inc -Newswire -Apple -Accenture -Anovia'

# news
def gnews(query):
	
	# query google
	news_url = ('https://ajax.googleapis.com/ajax/services/search/news?v=1.0&q=%s&rsz=3&ned=us') % urllib.quote_plus(query)
	print news_url
	news_request = urllib2.Request(news_url, None)
	news_response = urllib2.urlopen(news_request)

	# Process the JSON string.
	news_results = simplejson.load(news_response)
	nres = news_results['responseData']['results']
	
	# save results
	i = 0
	top_three = {} # save results for top 3 articles in a dict of dicts {1:{'title':x1,'url':y1},2:{'title':x2,'url':y2},3:{'title':x3,'url':y3}}
	for r in nres:
		i += 1
		top_three[i] = {}
		top_three[i]['title'] = strip_tags(r['title'].encode('ascii','ignore'))
		top_three[i]['url'] = r['unescapedUrl']
		top_three[i]['content'] = strip_tags(r['content'].encode('ascii','ignore'))
	
	return top_three


print pp(gnews(query))