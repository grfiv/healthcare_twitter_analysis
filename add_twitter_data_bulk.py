def add_twitter_data_bulk(input_filename):
    """
    reads in a *.csv file from the Coursolve Healthcare Twitter Analysis project
    and produces an output *.csv file with a number of Twitter fields added
    
    The name of the output file is the name of the input file with "_full" appended
    
    Notes:
    1. "twitter_functions.py" must be in your folder or somewhere on your path
    
    2. You must provide your own file named "twitter_credentials.py"
       (see https://apps.twitter.com/) written like this:
       
def twitter_credentials():
    api_key = " your credentials "
    api_secret = " your credentials "
    access_token_key = " your credentials "
    access_token_secret = " your credentials "
    return (api_key,api_secret,access_token_key,access_token_secret)
    
     3. You need to be aware that Twitter throttles your activity. 
        This function makes bulk calls to Twitter to try to increase 
        our throughput over add_twitter_data.py which makes one call to
        Twitter for every line
        
     4. IPython usage:
        (1) from add_twitter_data_bulk import add_twitter_data
            add_twitter_data("Tweets_BleedingDisorders.csv")
            
        (2) %run add_twitter_data_bulk.py "Tweets_BleedingDisorders.csv"
        
     5. If you have problems, I'll try to help ... george@georgefisher.com

    """
    import csv
    import json
    from twitter_functions import lookup_multiple_tweets
    from add_twitter_data  import parse_tweet_json
    
    output_filename = input_filename.split(".")[0] + "_full.csv"
    step              = 90  # we're going to process in groups of "step"
    bulk_list         = []  # batch of rows from input file 
    list_of_tweet_ids = []  # tweet ids of these rows
    output_dict       = []  # list of dicts to send to output file
    
    with open(input_filename, "rb" ) as infile:
       reader = csv.DictReader(infile)
       lines      = list(reader) # list of all lines/rows in the input file
       totallines = len(lines)   # number of lines in the input file
       print "Rows in file: " + str(totallines)
       
       # read the input file line-by-line
       # ================================
       for linenum, row in enumerate(lines):
        
           # accumulate a batch of rows from the input file
           # ==============================================
           tweet_id  = row['url'].split("/")[-1]
           row['id'] = tweet_id
           bulk_list.append(row)
           list_of_tweet_ids.append(tweet_id)
           
           # process the batch
           # =================
           if len(bulk_list) >= step or (linenum+1) >= totallines:
               
               # make a batch request to Twitter 
               result = lookup_multiple_tweets(list_of_tweet_ids)
               list_of_tweet_ids = []
               #print type(result)
               for foo in result:
                   tweetdata_list = json.loads(foo)
                   break
               # if twitter returns an error
               #    print the error
               #    break => jump to output file processing
               if 'errors' in tweetdata_list:
                   print "\nTwitter returned an error message:"
                   print "message: " + tweetdata_list["errors"][0]['message']
                   print "code:    " + str(tweetdata_list["errors"][0]['code'])
                   print "\nIf the message is 'Rate limit exceeded', see\nhttps://dev.twitter.com/docs/rate-limiting/1.1"
                   print "It basically seems to mean you have to wait 15 minutes"
                   import datetime
                   from datetime import timedelta
                   timenow    = datetime.datetime.today().strftime("%H:%M:%S")
                   timeplus15 = (datetime.datetime.today()+timedelta(minutes=15)).strftime("%H:%M:%S")
                   print " time now:           " + timenow +"\n time in 15 minutes: " + timeplus15
                   print "\nAny rows of " + input_filename + " that were processed up to this point should be in the output file\n"          
                   break

               # Twitter's response is in an arbitrary order so sort both lists by id
               bulk_list      = sorted(bulk_list,      key=lambda k: k['id'])
               tweetdata_list = sorted(tweetdata_list, key=lambda k: k['id'])
               if len(bulk_list) != len(tweetdata_list):
                   print "\nTwitter returned a different number of responses than we requested"
                   print "Requested: " + str(len(bulk_list))
                   print "Received:  " + str(len(tweetdata_list))
               
               for line, tweetdata in zip(bulk_list, tweetdata_list):
                   if str(tweetdata['id']) != str(line['id']):
                       print "\nmismatch in ids, skipping remaining rows in this batch"
                       print "tweetdata['id']=" + str(tweetdata['id'])
                       print "line['id']=     " + str(line['id'])
                       break

                   parse_tweet_json(line, tweetdata)
                   output_dict.append(line)
                   
               print "Rows processed: " + str(len(output_dict)) 
               bulk_list = []
               
    # create the output file
    # ======================
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
    add_twitter_data_bulk(sys.argv[1])