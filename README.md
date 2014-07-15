Healthcare Twitter Analysis  
===========================  

The use of social media data and data science to gain insights into health care and medicine.  

IPython Notebooks
================= 
- **Online Twitter Basics.ipynb**   
  You can use this notebook to sign on to Twitter directly, search for specific topics, and do analytics on live data.    
  
  Look in the *code* directory.  
  I recommend starting notebooks with `ipython notebook --pylab=inline` from the command line. pylab loads a number of scientific and plotting functions, making it easier to use.  

Analyses
=================  
  
- **Hashtags_and_Score.pdf**  
  A quick look at hashtag and score distributions    
- **Numerical_EDA.pdf**  
  Statistics on the all the numerical fields available      
- **Score_predicted_by_Numerics.pdf**  
  Do any of the numerics predict score?   
- **TextMining.pdf**  
  Word Cloud and dendogram.    
- **SentimentAnalysis.pdf**   
  Comparison of the Breen and AFINN sentiment-scoring systems. 

  
Twitter text parsing functions    
==============================    

- **parse_tweet_text**    
  The Online Twitter Basics.ipynb notebook makes extensive use of this function.  
```  
Parse the text of a single tweet, or a concatenated string from many tweets, 
and return the individual words, hashtags, users mentioned, urls and sentiment score.    

    Input:  tweet_text: a string with the text of a single tweet
            AFINN:      (optional) True 
                        Must have "AFINN-111.txt" in your folder  
                        but the function doesn't care what's in it  
                        so you can add your own n-grams.
    
    Output: lists of:
              words
              hashtags
              users mentioned
              urls
              
            (optional) AFINN-111 score 
            
    Usage: from twitter_functions import parse_tweet_text 
    
           words, hashes, users, urls = parse_tweet_text(tweet_text)
           
           words, hashes, users, urls, AFINN_score = parse_tweet_text(tweet_text, AFINN=True)
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

Try a sample file
=================
Before trying the instructions below, just download one of the sample .csv files and play around. These files have been filled out with the data available from Twitter and will get you started with analyses and visualizations.  

I. Setup
========
1. Pull these files onto your computer 
  - twitter_functions.py
  - add_twitter_data_bulk.py   
  - twitter_credentials.py 
  
2. Copy in any .csv files you want to convert from   
   https://drive.google.com/folderview?id=0B2io9_E3COquYWdlWjdzU3ozbzg&usp=sharing

3. Modify "twitter_credentials.py" with your personal Twitter credentials  
``` 
def twitter_credentials():  
    """
    A sample of this file is on the repo. Just download it, fill in your info and
    save it in the same path as the other files.
    
    See https://apps.twitter.com/ to get your own credentials
    """
    api_key = " your credentials "  
    api_secret = " your credentials "  
    access_token_key = " your credentials "  
    access_token_secret = " your credentials "  
    return (api_key,api_secret,access_token_key,access_token_secret)  
```

II. Run
=======

In IPython:
```
cd <to the folder with the programs and files>
%run add_twitter_data_bulk.py "the_name_of_your_file.csv"
```

The program will notify you after every batch; the output file is the name of the input file with "_full" appended. Twitter sometimes returns less data than we requested, in which case we stop when we reach an id mismatch and request a new batch. Rows processed up to an id mismatch are retained.

The change from serial to batch processing gets much further before running into Twitter's throttle (I processed well over 10,000 lines during testing before I hit it) but it's still there. As before, if any input lines have been processed by that point they WILL be written to the output file. The new code also runs to completion considerably faster.

This version is pretty robust, so you ought to really be able to make progress. But bugs undoubtedly remain and if you encounter problems I will try to help: use the "Issues" tab on the right of the GitHub screen and give me as much documentation as you can so I can reproduce the problem. Thanks.
  
Project Description
================= 
The dataset consists of ~2.5 Million tweets, more than 15 Million words. Potential areas which could be explored:  

1. Algorithms Research: Phrase detection, Spam Filtering for tweets, Natural Language Processing, Clustering, Classification, Bag of word analysis, Ontology for Healthcare, Part of Speech Analysis etc.    

2. Technology / Framework Research: What are the various frameworks / libraries / toolkits to implement text analysis, machine learning, NLP? (Preferably open source). What specific big data technology stack could be useful? Which Database / Data warehouse Technology Stack is lightweight and useful here?    

3. Business/ Domain Research: What kind of data is readily available (example - open government data) that could be useful to correlate with disease related tweets. Can we find a collection of hospital names, drug names, important medical hashtags, twitter usernames of healthcare organizations etc. that will aid in this project. What are the business use cases for this data set?     

4. Visualization Research: Finally one of the most critical, what set of visualization would help describe this data? Which libraries / tools could be used? I would recommend everyone to visit the “Collaboration Space” on Coursolve where we are having many interesting discussions. You would get a lot more ideas and probably collaborate on the next steps too.   
