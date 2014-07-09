def add_twitter_data(input_filename):
    """
    reads in a *.csv file from the Coursolve Healthcare Twitter Analysis project
    and produces an output *.csv file with a number of Twitter fields added
    
    The name of the output file is the name of the input file with "_full" appended
    
    Notes:
    1. "twitter_functions.py" must be in your folder or somewhere on your path
    
    2. You must provide your own file named "twitter_credentials.py"
       written like this:
       
def twitter_credentials():
    api_key = " your credentials "
    api_secret = " your credentials "
    access_token_key = " your credentials "
    access_token_secret = " your credentials "
    return (api_key,api_secret,access_token_key,access_token_secret)
    
     3. You need to be aware that Twitter throttles your activity. There may be a way to
        increase your limit but I have not researched this
        
     4. IPython usage:
        (1) from add_twitter_data import add_twitter_data
            add_twitter_data("Tweets_BleedingDisorders.csv")
            
        (2) %run add_twitter_data.py "Tweets_BleedingDisorders.csv"
        
     5. If you have problems, I'll try to help ... george@georgefisher.com

    """
    import csv
    import json
    import sys
    from twitter_functions import lookup_tweet
    
    output_dict = []
    counter = 0
    #input_filename  = 'Tweets_BleedingDisorders.csv'
    output_filename = input_filename.split(".")[0] + "_full.csv"
    with open(input_filename, "rb" ) as infile:
       reader = csv.DictReader(infile)
       for line in reader:
           tweet_id = line['url'].split("/")[-1]
           result = lookup_tweet(tweet_id)
           for foo in result:
               tweetdata = json.loads(foo)
               break
           if 'errors' in tweetdata:
               print "\nTwitter returned an error message:\n"
               print "message: " + tweetdata["errors"][0]['message']
               print "code:    " + str(tweetdata["errors"][0]['code'])
               print "If the message is 'Rate limit exceeded', see\nhttps://dev.twitter.com/docs/rate-limiting/1.1\n"
               print "It basically seems to mean you have to wait 15 minutes\n"
               print "Any rows of " + input_filename + " that were processed up to this point should be in the output file\n"
               #sys.exit()           
               break
           line["coordinates"]  = str(tweetdata["coordinates"])
           line["favorited"]    = str(tweetdata["favorited"])
           if tweetdata["entities"] is not None:
                if tweetdata["entities"]["hashtags"] is not None:
                    hashtag_string = ""
                    for tag in tweetdata["entities"]["hashtags"]:
                        hashtag_string = hashtag_string + tag["text"] + "~"
                    hashtag_string = hashtag_string[:-1]
                    line["hashtags"] = str(hashtag_string.encode('utf-8'))
                else:
                    line["hashtags"] = ""
                if tweetdata["entities"]["user_mentions"] is not None:
                    user_mentions_string = ""
                    for tag in tweetdata["entities"]["user_mentions"]:
                        user_mentions_string = user_mentions_string + tag["screen_name"] + "~"
                    user_mentions_string = user_mentions_string[:-1]
                    line["user_mentions"] = str(user_mentions_string)
                else:
                    line["user_mentions"] = ""
           line["retweet_count"] = str(tweetdata["retweet_count"])
           line["retweeted"]     = str(tweetdata["retweeted"])
           line["place"]         = str(tweetdata["place"])
           line["geo"]           = str(tweetdata["geo"])
           if tweetdata["user"] is not None:
               line["followers_count"]  = str(tweetdata["user"]["followers_count"])
               line["favourites_count"] = str(tweetdata["user"]["favourites_count"])
               line["listed_count"]     = str(tweetdata["user"]["listed_count"])
               line["location"]         = str(tweetdata["user"]["location"])
               line["utc_offset"]       = str(tweetdata["user"]["utc_offset"])
               line["listed_count"]     = str(tweetdata["user"]["listed_count"])
               line["lang"]             = str(tweetdata["user"]["lang"])
               line["geo_enabled"]      = str(tweetdata["user"]["geo_enabled"])
               line["time_zone"]        = str(tweetdata["user"]["time_zone"])
               line["description"]      = tweetdata["user"]["description"].encode('utf-8')
           
           output_dict.append(line)
           if counter%10 == 0: print "item " + str(counter) + " processed"
           counter+=1
           if (counter > 100): 
            break
            
    if output_dict:
        f = open(output_filename,'wb')
        w = csv.DictWriter(f, delimiter=",", fieldnames=output_dict[0].keys())
        w.writeheader()
        w.writerows(output_dict)
        f.close()
        print output_filename + " has been created"
    else:
        print output_filename + " was NOT created"

if __name__ == '__main__':
    import sys
    add_twitter_data(sys.argv[1])