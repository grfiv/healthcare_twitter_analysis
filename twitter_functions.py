
def twitterreq(url, method, parameters):
    """
    Send twitter URL request
    
    Utility function used by the others in this package
    
    Note: calls a function twitter_credentials() contained in
          a file named twitter_credentials.py which must be provided 
          individually by each user, which returns the values for: 
              api_key
              api_secret
              access_token_key
              access_token_secret
          as a tuple in that order
          
     This is a modification of a shell provided by
     Bill Howe
     University of Washington
     for the Coursera course Introduction to Data Science
     Spring/Summer 2014
     (which I HIGHLY recommend)
    """
    import oauth2 as oauth
    import urllib2 as urllib

    # this is a private function containing my Twitter credentials
    from twitter_credentials import twitter_credentials
    api_key,api_secret,access_token_key,access_token_secret = twitter_credentials()

    _debug = 0

    oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
    oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

    signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

    http_method = "GET"


    http_handler  = urllib.HTTPHandler(debuglevel=_debug)
    https_handler = urllib.HTTPSHandler(debuglevel=_debug)

    '''
    Construct, sign, and open a twitter request
    using the hard-coded credentials above.
    '''
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

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response

def lookup_tweet(tweet_id):
    """
    Ask Twitter for information about a specific tweet by its id
    
    the Twitter API for this is here:
    https://dev.twitter.com/docs/api/1.1/get/statuses/show/%3Aid
    
Use: 
import json
from twitter_functions import lookup_tweet

result = lookup_tweet("473010591544520705")
for foo in result:
    tweetdata = json.loads(foo)
    break
# there must be a better way

print json.dumps(tweetdata, sort_keys = False, indent = 4)


# all may be null; have to check
for tag in tweetdata["entities"]["hashtags"]:
print tag["text"]
tweetdata["place"]
tweetdata["geo"]
tweetdata["lang"]
tweetdata["coordinates"]
# plus, potentially redundant, tweetdata["user"][...]
    """
    
    url = "https://api.twitter.com/1.1/statuses/show.json?id=" + tweet_id
    parameters = []
    response = twitterreq(url, "GET", parameters)
      
    return response
    
def lookup_user(rsarver):
    """
    Ask Twitter for information about a user name
    
    the Twitter API for this is here:
    https://dev.twitter.com/docs/api/1.1/get/users/show
    
Use: 
import json
from twitter_functions import lookup_user

result = lookup_user("flgprohemo")
for foo in result:
    userdata = json.loads(foo)
    break
# there must be a better way

print json.dumps(userdata, sort_keys = False, indent = 4)


# all may be null; have to check
userdata["location"].encode('utf-8')
userdata["description"].encode('utf-8')
userdata["utc_offset"].encode('utf-8')
userdata["time_zone"].encode('utf-8')
userdata["status"]["lang"].encode('utf-8')
    """
    
    url = "https://api.twitter.com/1.1/users/show.json?screen_name=" + rsarver
    parameters = []
    response = twitterreq(url, "GET", parameters)
      
    return response
    
def lookup_multiple_users(csv_of_screen_names):
    """
    Ask Twitter for information about up to 100 screen names
    The input argument must be a string of screen names separated by commas
    
    the Twitter API for this is here:
    https://dev.twitter.com/docs/api/1.1/get/users/lookup
    
    Version 0.1 uses GET; Twitter urges POST; I will get to that later
    
Use: 
import json
from twitter_functions import lookup_multiple_users

screen_name_list    = ["grfiv","flgprohemo"]
csv_of_screen_names = ",".join(screen_name_list)

result = lookup_multiple_users(csv_of_screen_names)
for foo in result:
    userdata = json.loads(foo)
    break
# there must be a better way

for user in userdata:
    print "For screen name: " + user["screen_name"]
    print json.dumps(user, sort_keys = False, indent = 4)

    """
    
    url = "https://api.twitter.com/1.1/users/lookup.json?screen_name=" + csv_of_screen_names
    parameters = []
    response = twitterreq(url, "GET", parameters)
      
    return response