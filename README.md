Healthcare Twitter Analysis  
===========================  

The use of social media data and data science to gain insights into health care and medicine. 

The current status report is in the main folder. 

[![DOI](https://zenodo.org/badge/5738/grfiv/healthcare_twitter_analysis.png)](http://dx.doi.org/10.5281/zenodo.11426)

-------------------------------


All of the tweets for this project have been processed and consolidated into a single file that can be downloaded with this link:

- https://s3-us-west-2.amazonaws.com/healthcare-twitter-analysis/HTA_noduplicates.gz  
1.85 Gb zipped / 15.80 Gb unzipped  


Each of the 4 million rows in this file is a tweet in json format containing the following information:

- All the Twitter data in exactly the json format of the original  
- Unix time stamp  
- data from the original files:  
    - originating file name  
    - score  
    - author screen name  
    - URLs  

60% of the records have geographic information ...  
- Latitude & Longitude  
- Country name & ISO2 country code  
- City  
- For country code "US"  
  - Zipcode  
  - Telephone area code  
  - Square miles inside the zipcode  
  - 2010 Census population of the zipcode  
  - County & FIPS code  
  - State name & USPS abbreviation   

The basic technique for using this file in Python is the following:


    import json
    
    with open("HTA_noduplicates.json", "r") as f:
        # convert each row in turn into json format and process
        for row in f:
            tweet = json.loads(row)
            text  = tweet["text"]      # text of original tweet
            ...                        # etc.
            
Python provides very powerful analytical and plotting features but R is also very handy; R does not work well with large datasets but Python can be used to create a targeted subset file that R can read (or Excel, or anything else for that matter).

The Status Report in the main part of the repo contains  
- a comprehensive explanation of the dataset  
- examples of analyses done with this dataset  
- a list of references to other healthcare-related Twitter analyses  
- instructions for using Amazon Web Services
- sample programs using this file with Python, R and MongoDB.
