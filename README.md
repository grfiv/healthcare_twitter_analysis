Healthcare Twitter Analysis  
===========================  

The use of social media data and data science to gain insights into health care and medicine. 

The current status report is in the main folder.  

IPython Notebooks
================= 
- **Online Twitter Basics.ipynb**   
  Sign on to Twitter directly, live, search for specific topics, and do analytics on live data.    
  
  Look in the `code` directory.  

Add twitter data to the files
=================
The 897 files for this project are located on Google Drive. Install the app and you will have direct access to them.  
[Google Drive files on the web](https://drive.google.com/folderview?id=0B2io9_E3COquYWdlWjdzU3ozbzg&usp=sharing)    

However, these files have none of the Twitter data besides the ['text'] field (which is called "content").  

The repo ([GitHub](https://github.com/grfiv/healthcare_twitter_analysis)) contains two python programs in the `code` folder to solve this problem:  
Both read in a text file containing a list of fully-qualified file names to process ...    

1. `get_twitter_json.py` produces a json output file with the exact Twitter json for each tweet, augmented by additional fields as shown in `fields_added_to_twitter_json.txt` in the `files` folder.   
2. `create_bulkfile.py` produces a csv output file with additional Twitter data fields plus calculated fields like sentiment from AFINN-111 and place name & coordinates from the Google Geocoding API. See `list_of_variable_names_in_the_processed_file.txt` in the `files` folder for a list of columns.  

Samples of both file types are included in the `files` folder. 

**get_twitter_json.py**   
```     
def get_twitter_json(list_of_filenames, starting_at=1, ending_at=0, geocode=True):
    """
    1) reads in a list of fully-qualified filenames from "list_of_filenames"
        
    2) processes each row of each topsy file in the "list_of_filenames", 
       making batched calls to Twitter to retrieve the json for each tweet
           adding the data from the topsy file such as "score"
           plus unix timestamps for the topsy firstpost_date field and Twitter's created_at field
           plus coordinate and place name data for Twitter's user location field
    
    - after every 13,500 rows, or whenever there is a threshold-exceeded error
      the program goes to sleep for 15 minutes.
      
    Note: a file named twitter_credentials.py must be in the folder with the code
          see the repo: it contains your Twitter credentials
    
    Note: if geocode=True a file named mapquest_key.txt must be in the folder with the code
          get a MapQuest key here: http://developer.mapquest.com/
   
      
    Input: list_of_filenames   a text file with fully-qualified file names
           starting_at         the line number of "list_of_filenames" where processing should start
           ending_at           if 0   process all files beginning with the "starting_at" line in "list_of_filenames"
                               if > 0 process the files from line "starting_at" to line "ending_at" in "list_of_filenames"
           geocode             if True, batched requests are made to the MapQuest Developers API for coordinate and place name data
                               if False, these call are not made and no geo info is added
                                 
           
    Output: a text file named "bigtweet_filexxx.json", where xxx is the "starting_at" number
        
    Usage: %run get_twitter_json.py "filename_list.csv" 2 2
                          - or -
           nohup python get_twitter_json.py "filename_list.csv" 1 0 &
    
    A message like "6 skipped id 448176144668721152" means that Twitter failed to return any data about 
    a tweet with id 448... and that this is the 6th instance of this. Fewer than 1% are skipped.
    
    To use the output file in python:
    =================================
import json
tweet_file = open("bigtweet_file002.json", "r")
for line in tweet_file:
    tweet = json.loads(str(line))
    if tweet['retweet_count'] > 100:
        print "\n\n%d %s\n%s"%(tweet['retweet_count'], tweet['user']['name'], tweet['text'])

        
    To use the output file in R:
    ============================
library(rjson)
file_path  = ("../files/bigtweet_file002.json")
tweet_list = fromJSON(sprintf("[%s]", paste(readLines(file_path),collapse=",")))

for (i in 1:length(tweet_list)){
    if (tweet_list[[i]]$retweet_count > 100){
        cat(sprintf("\n\n%d %s\n%s",tweet_list[[i]]$retweet_count, tweet_list[[i]]$user$name, tweet_list[[i]]$text))
    }
} 
## convert to twitteR structure
library(twitteR)
tweets = import_statuses(raw_data=tweet_list)

   To store in MongoDB using python:
   =================================
# create a python list of each tweet
import json
tweet_file = open("../files/bigtweet_file002.json", "r")
tweet_list = [json.loads(str(line)) for line in tweet_file]

# store the list in MongoDB
from pymongo import MongoClient
client = MongoClient()
db     = client['file002']
posts  = db.posts
#db.posts.remove( { } ) # delete if previously created

posts.insert(tweet_list)

# same example as above
for result in db.posts.find({ "retweet_count": { "$gt": 100 } }):
    print "%d %s\n%s"%(result['retweet_count'],result['user']['name'],result['text'])
    """
```    


**create_bulkfile.py**  
```  
def create_bulkfile(list_of_filenames, starting_at=1, ending_at=0):
    """
    - reads in a list of fully-qualified filenames from "list_of_filenames"
    
        I'm expecting file names to have the Windows Google Drive structure, for example
        ... Twitter Data\June\Cardiovasucular\Tweets_AFib.csv  
        
        the code is commented with a simple solution you can implement to allow you to have
        any arbitrary fully-qualified filename, for any operating system
        
    - processes each row of each file in the file list, 
      making batched calls to Twitter to retrieve the data for each tweet
    
    - after every 13,500 rows, or whenever there is a threshold-exceeded error
      the output_file is written and the program goes to sleep for 15 minutes.
      
    Note: AFINN-111.txt must be in the same folder
          you can use it as is or include your own n-grams
          the 'sentiment' field is the sum of the scores of all the n-grams found  
          
    Note: Requires pygeocoder  
    
    Input: list_of_filenames   a text file with fully-qualified file names
           starting_at         the line number of "list_of_filenames" where processing should start
           ending_at           if 0   process all files beginning with the "starting_at" line in "list_of_filenames"
                               if > 0 process the files from line "starting_at" to line "ending_at" in "list_of_filenames"
           
    Output: a csv file named "bigtweet_filexxx.csv", where xxx is the "starting_at" number
        
    Usage: %run create_bulkfile.py "filename_list.csv" 1 0
    
    A message like "263 skipped id 463811853097787392" indicates that Twitter did not return data
    for a tweet with the id of 463811853097787392 and this is the 263rd instance of this. 
    As a result of this and other less-common errors the output file will have fewer rows than 
    the total rows in the input files.
    """
```   
Notify me through the Issues tab of GitHub if you have any problems with these programs.  

Twitter text parsing functions    
==============================    

- **parse_tweet_text**    
  The Online Twitter Basics.ipynb notebook makes extensive use of this function.  
```  
def parse_tweet_text(tweet_text):
    """
    Input:  tweet_text: a string with the text of a single tweet
                        or a concatenation of tweets
                
    Output: lists of tokens in the text:
              words (many emoticons are recognized as words)
              hashtags
              users mentioned
              urls
              
    Usage: words, hashes, users, urls = parse_tweet_text(tweet_text)
    """
```  

- **find_WordsHashUsers**    
```  
Process an entire csv file of tweets using the parse_tweet_text function above.  

  Input:  input_filename: any csv file containing the tweet text  
          text_field_name: the name of the column containing the tweet text  
          list_or_set: do you want every instance ("list") or unique entries ("set")?  
    
  Output: lists or sets of  
            words  
            hashtags  
            users mentioned  
            urls  
            
   Usage:  from twitter_functions import find_WordsHashUsers
   
           word_list, hash_list, user_list, url_list, num_tweets = \  
           find_WordsHashUsers("../files/Tweets_BleedingDisorders.csv", "content", "list")  
    
           word_set, hash_set, user_set, url_set, num_tweets =  \  
           find_WordsHashUsers("../files/Tweets_BleedingDisorders.csv", "content", "set")
```             

Project Description
================= 
The dataset consists of ~2.5 Million tweets, more than 15 Million words. Potential areas which could be explored:  

1. Algorithms Research: Phrase detection, Spam Filtering for tweets, Natural Language Processing, Clustering, Classification, Bag of word analysis, Ontology for Healthcare, Part of Speech Analysis etc.    

2. Technology / Framework Research: What are the various frameworks / libraries / toolkits to implement text analysis, machine learning, NLP? (Preferably open source). What specific big data technology stack could be useful? Which Database / Data warehouse Technology Stack is lightweight and useful here?    

3. Business/ Domain Research: What kind of data is readily available (example - open government data) that could be useful to correlate with disease related tweets. Can we find a collection of hospital names, drug names, important medical hashtags, twitter usernames of healthcare organizations etc. that will aid in this project. What are the business use cases for this data set?     

4. Visualization Research: Finally one of the most critical, what set of visualization would help describe this data? Which libraries / tools could be used? I would recommend everyone to visit the “Collaboration Space” on Coursolve where we are having many interesting discussions. You would get a lot more ideas and probably collaborate on the next steps too.   
