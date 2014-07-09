Coursolve Healthcare Twitter Analysis project
===========================
Try a sample file
=================
Before trying the instructions below, just download the sample *.csv file and play around with it. It may have enough data in it to get you started with basic analyses and visualizations.

I. Setup
========
1. Pull these files onto your computer 
  - twitter_functions.py
  - add_twitter_data.py   
  - twitter_credentials.py 

2. Copy in the .csv file you want to convert (I have only tested with *Tweets_BleedingDisorders.csv*)


3. Modify "twitter_credentials.py" with your personal Twitter credentials  
``` 
def twitter_credentials():  
    """
    A sample of this file is on the repo. Just download it, fill in your info and
    save it in the same path as the other files.
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
cd the folder with the programs and file
%run add_twitter_data.py "the_name_of_your_file.csv"
```

The program will notify you every 10 lines; the output file is the name of the input file with "_full" appended.    

Twitter has a throttle which may stop you mid-flight and force you to wait 15 minutes. BUT, if any input lines have been processed by that point they WILL be written to the output file.

This is version 0.1. An improvement will be for me to move to batch requests and to use POST rather than GET.  

In the meantime, even with the throttle, this should give you something you can test your analyses and visualizations on without having to bother yourself with the data acquision from Twitter.

If you have problems I will try to help: george@georgefisher.com