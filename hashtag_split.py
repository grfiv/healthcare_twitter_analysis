def hashtag_split(input_filename):
    """
    input:  a csv file that has been processed by add_twitter_data_bulk.py
    output: a csv file with a row for every hashtag in a row of the input file
    use:    %run hashtag_split "Tweets_BleedingDisorders_full.csv"
    """
    import csv
        
    output_filename   = input_filename.split(".")[0][:-5] + "_hashtagsplit.csv"
    bulk_list         = []  # batch of rows from input file 
    list_of_tweet_ids = []  # tweet ids of these rows
    output_dict       = []  # list of dicts to send to output file
    
    with open(input_filename, "rb" ) as infile:
       reader     = csv.DictReader(infile)
       lines      = list(reader) # list of all lines/rows in the input file
       totallines = len(lines)   # number of lines in the input file
       print "Rows in input file: " + str(totallines)
       
       # read the input file line-by-line
       # ================================
       for linenum, row in enumerate(lines):
           if row['hashtags']:
               tags = row['hashtags'].split("~")
               for tag in tags:
                  output_row = dict(row)
                  output_row['hashtag'] = tag.lower()
                  output_row.pop('hashtags', None)
                  output_dict.append(output_row)
               
    # create the output file
    # ======================
    if output_dict:
        f = open(output_filename,'wb')
        w = csv.DictWriter(f, delimiter=",", fieldnames=output_dict[0].keys())
        w.writeheader()
        w.writerows(output_dict)
        f.close()
        print output_filename + " has been created; " + str(len(output_dict)) + " rows"
    else:
        print output_filename + " was NOT created"
                       

if __name__ == '__main__':
    import sys
    hashtag_split(sys.argv[1])