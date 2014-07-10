Coursolve Healthcare Twitter Analysis project
===========================
Try a sample file
=================
Before trying the instructions below, just download one of the sample .csv files and play around. They may have enough data to get you started with basic analyses and visualizations.

I. Setup
========
1. Pull these files onto your computer 
  - twitter_functions.py
  - add_twitter_data_bulk.py   
  - twitter_credentials.py 
  
2. Note: **add_twitter_data_bulk.py** replaces *add_twitter_data.py*  
         you must refresh *twitter_functions.py*

3. Copy in the .csv file you want to convert (I have only tested with the sample files...that's where they came from)


4. Modify "twitter_credentials.py" with your personal Twitter credentials  
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

The program will notify you after every batch; the output file is the name of the input file with "_full" appended. Twitter sometimes returns less data than we requested, in which place we stop and request a new batch.  

This updated code gets MUCH further before running into Twitter's throttle (I processed nearly 10,000 lines during testing before I hit it) but it's still there. BUT, if any input lines have been processed by that point they WILL be written to the output file.

This is version 0.2.   
- Batch processing has been added. 
- POST processing is recommended by Twitter but I don't currently see the need.
- If anyone want me to parse out place names, send me a python list `place_names = ["Boston","Hong Kong", ...]`


In the meantime, even with the throttle, this should give you something you can test your analyses and visualizations on without having to bother yourself with the data acquisition from Twitter.

If you have problems I will try to help: george@georgefisher.com