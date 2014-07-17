Healthcare Twitter Analysis  
===========================  

The use of social media data and data science to gain insights into health care and medicine.  

IPython Notebooks
================= 
- **Online Twitter Basics.ipynb**   
  Sign on to Twitter directly, live, search for specific topics, and do analytics on live data.    
  
  Look in the *code* directory.  
  I recommend starting notebooks with `ipython notebook --pylab=inline` from the command line. pylab loads a number of scientific and plotting functions, making it easier to use.  

Analyses
=================  
  
- **Hashtags_and_Score.pdf**  
  Hashtag and score distributions    
- **Numerical_EDA.pdf**  
  Statistics on the all the numerical fields available      
- **Score_predicted_by_Numerics.pdf**  
  Do any of the numerics predict score?   
- **TextMining.pdf**  
  Word Cloud and dendogram.    
- **SentimentAnalysis.pdf**   
  Comparison of the Breen and AFINN sentiment-scoring systems.   

Add twitter data to the files
=================
The 897 files for this project are located on Google Drive. Install the app and you will have direct access to them.  
[Google Drive files on the web](https://drive.google.com/folderview?id=0B2io9_E3COquYWdlWjdzU3ozbzg&usp=sharing)    

However, these files have none of the Twitter data besides the ['text'] field (which is called "content").  

The program `create_bulkfile.py` in the *code* folder of [the GitHub repo](https://github.com/grfiv/healthcare_twitter_analysis) reads in a text file containing a list of fully-qualified file names and produces an output file with the additional Twitter data fields included. 

A list of the column names of the output file is in the *files* folder: `list_of_variable_names_in_the_processed_file.txt`  

I have used this program to create files of subsets of the data ... all the files referencing Endocrine, for example, to do research specifically on that disease category.  

Requirements:  
1. A file named `AFINN-111.txt` must be in the same folder as the program. It contains a list of n-grams with their sentiment scores. If you don't like what's there, you can add your own as long as you retain the tab-delimited format.   
2. You must modify `twitter_credentials.py` to contain your own credentials.   

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
    
    Input: list_of_filenames   a text file with fully-qualified file names
           starting_at         the line number of "list_of_filenames" where processing should start
           ending_at           if 0   process all files beginning with the "starting_at" line in "list_of_filenames"
                               if > 0 process the files from line "starting_at" to line "ending_at" in "list_of_filenames"  
           
    Output: a csv file named "bigtweet_filexxx.csv", where xxx is the "starting_at" number
        
    Usage: %run create_bulkfile.py "filename_list.csv" 1 0
    """
```   
Notify me through the Issues tab of GitHub if you have any problems with the program.  

Twitter text parsing functions    
==============================    

- **parse_tweet_text**    
  The Online Twitter Basics.ipynb notebook makes extensive use of this function.  
```  
Parse the text of a single tweet, or a concatenated string from many tweets, 
and return the individual words, hashtags, users mentioned, urls and sentiment score.    

    Input:  tweet_text: a string with the text to be parsed
            AFINN:      (optional) True 
                        Must have "AFINN-111.txt" in your folder  
                        but the function doesn't care what's in it  
                        so you can add your own n-grams.
    
    Output: lists of:
              words
              hashtags
              users mentioned
              urls
              
            (optional) sentiment score 
            
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

Project Description
================= 
The dataset consists of ~2.5 Million tweets, more than 15 Million words. Potential areas which could be explored:  

1. Algorithms Research: Phrase detection, Spam Filtering for tweets, Natural Language Processing, Clustering, Classification, Bag of word analysis, Ontology for Healthcare, Part of Speech Analysis etc.    

2. Technology / Framework Research: What are the various frameworks / libraries / toolkits to implement text analysis, machine learning, NLP? (Preferably open source). What specific big data technology stack could be useful? Which Database / Data warehouse Technology Stack is lightweight and useful here?    

3. Business/ Domain Research: What kind of data is readily available (example - open government data) that could be useful to correlate with disease related tweets. Can we find a collection of hospital names, drug names, important medical hashtags, twitter usernames of healthcare organizations etc. that will aid in this project. What are the business use cases for this data set?     

4. Visualization Research: Finally one of the most critical, what set of visualization would help describe this data? Which libraries / tools could be used? I would recommend everyone to visit the “Collaboration Space” on Coursolve where we are having many interesting discussions. You would get a lot more ideas and probably collaborate on the next steps too.   
