import oauth2 as oauth
import urllib2 as urllib

# See Assginment 6 instructions or README for how to get these credentials
access_token_key = "48696845-DwzKPGQV6Dlfo97sRvb78MbOYAnTRprnsPVMVYSEF"
access_token_secret = "S16DwJcSG4GxQZvMG3XSO6nGCS5fH3ByOucnvnKbH9w"

consumer_key = "Px9XaX9AgvXYeM3cGIAdw"
consumer_secret = "bWvfJx7MBWN524MpYuxec2ADONs6qQBO8KKkmu8sCqc"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"

http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(parameters):
  url = "https://api.twitter.com/1.1/search/tweets.json"
  
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()
  #print url
  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)
  
  return response


