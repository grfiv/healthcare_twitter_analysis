def find_WordsHashUsers(input_filename, text_field_name="content", list_or_set="list"):
    """
    Input:  input_filename: the csv file
            text_field_name: the name of the column containing the tweet text
            list_or_set: do you want every instance ("list") or unique entries ("set")?
    
    Output: lists or sets of
            words
            hashtags
            users mentioned
            urls
            
    Usage:  word_list, hash_list, user_list, url_list, num_tweets = \
            find_WordsHashUsers("../files/Tweets_BleedingDisorders.csv", "content", "list")
    
            word_set, hash_set, user_set, url_set, num_tweets =  \
            find_WordsHashUsers("../files/Tweets_BleedingDisorders.csv", "content", "set")
    """
    import csv
    import re
    
    if list_or_set != "set" and list_or_set != "list":
        print "list_or_set must be 'list' or 'set', not " + list_or_set
        return()
    
    if list_or_set == "list":
        word_list = list()
        hash_list = list()
        user_list = list()
        url_list  = list()
    else:
        word_set = set()
        hash_set = set()
        user_set = set()
        url_set  = set()
    
    with open(input_filename, "rb" ) as infile:
       reader     = csv.DictReader(infile)
       lines      = list(reader) # list of all lines/rows in the input file
       totallines = len(lines)   # number of lines in the input file
       
       # read the input file line-by-line
       # ================================
       for linenum, row in enumerate(lines):
        
           content = row[text_field_name].lower()
           
           urls = re.findall(r"\b((?:https?|ftp|file)://[-A-Z0-9+&@#/%?=~_|$!:,.;]*[A-Z0-9+&@#/%=~_|$])", content, re.IGNORECASE)
           content = re.sub(r"\b((?:https?|ftp|file)://[-A-Z0-9+&@#/%?=~_|$!:,.;]*[A-Z0-9+&@#/%=~_|$])", "", content, 0, re.IGNORECASE)
           hashes  = re.findall(r"#(\w+)", content)
           content = re.sub(r"#(\w+)", "", content, 0)
           users   = re.findall(r"@(\w+)", content)
           content = re.sub(r"@(\w+)", "", content, 0)
           content = re.sub(r"\b(https?|ftp|file)://[-A-Z0-9+&@#/%?=~_|$!:,.;]*[A-Z0-9+&@#/%=~_|$]", "", content, 0, re.MULTILINE)
           words   = content.split()
           
           if list_or_set == "list":
               word_list.extend(words)
               hash_list.extend(hashes)
               user_list.extend(users)
               url_list.extend(urls)
           else:
               word_set.update(words)
               hash_set.update(hashes)
               user_set.update(users)
               url_set.update(urls)
           
    if list_or_set == "list":
        return (word_list, hash_list, user_list, url_list, totallines)
    else:
        return (word_set, hash_set, user_set, url_set, totallines)