import requests
from tagzapper import strip_tags


# pass in the url and will return a string of the article content
def crawL_and_return(url):
	r = requests.get(url)
	return (r.text).encode('ascii','ignore')

print crawL_and_return('http://www.sltrib.com/sltrib/money/56666743-79/xango-company-lehi-webb.html.csp')