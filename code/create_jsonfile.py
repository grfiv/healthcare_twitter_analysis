def create_jsonfile(list_of_filenames, starting_at=1, ending_at=0):
    """
    - reads in a list of fully-qualified filenames from "list_of_filenames"
        
    - processes each row of each file in the file list, 
      making batched calls to Twitter to retrieve the data for each tweet
    
    - after every 13,500 rows, or whenever there is a threshold-exceeded error
      the output_file is written and the program goes to sleep for 15 minutes.
      
    Input: list_of_filenames   a text file with fully-qualified file names
           starting_at         the line number of "list_of_filenames" where processing should start
           ending_at           if 0   process all files beginning with the "starting_at" line in "list_of_filenames"
                               if > 0 process the files from line "starting_at" to line "ending_at" in "list_of_filenames"
           
    Output: a text file named "bigtweet_filexxx.json", where xxx is the "starting_at" number
        
    Usage: %run create_jsonfile.py "filename_list.csv" 1 0
    
    To use the output file in python:
import json
tweet_file = open("../files/bigtweet_file003.json", "r")
for line in tweet_file:
    tweet = json.loads(str(line))
    if tweet['retweet_count'] > 100:
        print "\n\n%d %s\n%s"%(tweet['retweet_count'], tweet['user']['name'], tweet['text'])

        
    To use the output file in R:
library(rjson)
file_path  = ("../files/bigtweet_file003.json")
tweet_list = fromJSON(sprintf("[%s]", paste(readLines(file_path),collapse=",")))

for (i in 1:length(tweet_list)){
    if (tweet_list[[i]]$retweet_count > 100){
        cat(sprintf("\n\n%d %s\n%s",tweet_list[[i]]$retweet_count, tweet_list[[i]]$user$name, tweet_list[[i]]$text))
    }
} 
    """
    import csv
    import json
    import re
    import time
    import sys
    import datetime
    from twitter_functions import lookup_multiple_tweets
    
    # convert input parameter strings to integer
    starting_at = int(starting_at) 
    ending_at   = int(ending_at)
    
    process_start = datetime.datetime.now()
    print "\n================================"
    print "process start: %s"%process_start.strftime("%c")
    print "================================\n"
    
    # read the list of filenames into "filename_list"
    # ===============================================
    filename_list = []
    with open(list_of_filenames, "rb") as namefile:
        csv_reader = csv.reader(namefile)
        for row in csv_reader:
            filename_list.extend(row)
    
    output_filename   = "bigtweet_file" + "%03d"%(starting_at,) + ".json"
    step              = 100 # we're going to process in groups of "step"
    list_of_tweet_ids = []  # tweet ids of these rows
    output_dict       = []  # list of dicts to send to output file
    
    # the Twitter rate limits are documented here
    # https://dev.twitter.com/docs/rate-limiting/1.1/limits
    sleep_batch       = 13500 # we sleep after this many lines processed
    sleep_batch_rows  = 0     # the number of lines we've processes since the last sleep
    
    number_of_files   = len(filename_list) # how many files in the list
    file_counter      = 1                  # which one is this one
    global first_sleep
    first_sleep       = True               # first time through, we write an output_file header
    invalid_json      = False              # in case Twitter sends us junk
    global total_processed
    total_processed   = 0                  # how many rows have we processed
    
    # read each file in and process it
    # ==================================
    for input_filename in filename_list:
        
        # skip the first "starting_at-1" files
        if file_counter < starting_at:
            print "Skipping %d of %d %s"%(file_counter, number_of_files, input_filename)
            file_counter+=1
            continue  
            
        if ending_at != 0: number_of_files = ending_at
            
        # find the shortened file name
        #
        # note: if your filenames do not fit my convention
        #       replace the two lines below with
        #
        #       short_file_name = input_filename
        #
        match = re.search(r"Twitter Data\\(.*)", input_filename) 
        short_file_name = match.group(1)  

        # stop if we're beyond "ending_at"
        if ending_at > 0:
            if file_counter > ending_at:
                print "Ending before %d of %d %s"%(file_counter, number_of_files, input_filename)
                break
        
        # open an input file
        with open(input_filename, "rb" ) as infile:
            reader     = csv.DictReader(infile)
            lines      = list(reader) # list of all lines/rows in the input file
            totallines = len(lines)   # number of lines in the input file
            
            print "\n--Processing %d of %d %s rows %d"%(file_counter, number_of_files, short_file_name,totallines)
            
            # read the input file line-by-line
            # ================================
            for linenum, row in enumerate(lines):
                
                # sleep if we're over the limit of lines processed
                sleep_batch_rows+=1
                if sleep_batch_rows > sleep_batch:
                    print "sleeping after %d lines of file %d of %d %s"%(linenum, file_counter, number_of_files, short_file_name)
                    sleep_batch_rows = 0
                    sleep_process(output_dict, output_filename)
                    
                # accumulate a batch of rows from the input file
                # ==============================================
                tweet_id  = row['url'].split("/")[-1]
                # make sure tweet_id is actually numeric
                if re.match(r"^\d+", tweet_id):
                    # Successful match at the start of the string
                    row['id'] = tweet_id
                    list_of_tweet_ids.append(tweet_id)
                else:
                    print "tweet url terminated with non-numeric in line %d"%(linenum+1)
                    print row['url']
                
                # if batch-size reached, process the batch
                if len(list_of_tweet_ids) >= step or (linenum+1) >= totallines:
                   
                    # make a batch request to Twitter 
                    # ===============================
                    result = lookup_multiple_tweets(list_of_tweet_ids)
                        
                    list_of_tweet_ids = []
                    
                    for foo in result:
                        try:
                            tweetdata_list = json.loads(foo)
                            break
                        except ValueError, e:
                            print "\nTwitter returned invalid json"
                            print e
                            print "after %d lines of file %d of %d %s"%(linenum, file_counter, number_of_files, short_file_name)
                            invalid_json = True
                            break
                            
                    if invalid_json:
                        invalid_json = False
                        break
                        
                    # if Twitter returns an error
                    #
                    # better process
                    # try:
                    #     statuses = api.GetUserTimeline(u.id)
                    #     print [s.text for s in statuses]
                    # except TwitterError, t:
                    #     print t
                    if 'errors' in tweetdata_list:
                        print "Twitter returned an error message:"
                        print "message: " + str(tweetdata_list["errors"][0]['message'])
                        print "code:    " + str(tweetdata_list["errors"][0]['code'])
                        print "after %d lines of file %d of %d %s"%(linenum, file_counter, number_of_files, short_file_name)
                        sleep_batch_rows = 0
                        sleep_process(tweetdata_list, output_filename)
                        continue
                        
                    process_output_file(tweetdata_list, output_filename)
                  
        file_counter+=1
                            
    # how long did it take?
    process_end     = datetime.datetime.now()
    process_elapsed = process_end - process_start
    process_seconds = process_elapsed.seconds
    process_minutes = process_seconds/60.0
    process_hours   = process_minutes/60.0
    
    print "\n================================"
    print "process start: %s"%process_start.strftime("%c")
    print "process end:   %s"%process_end.strftime("%c")
    print "process elapsed hours %0.2f"%process_hours
    print "================================\n"    
    
                    
    
def sleep_process(output_dict, output_filename):
    import time
    import sys
    import datetime
    from datetime import timedelta
    
    process_output_file(output_dict, output_filename)
    
    length_of_sleep = int(15.1*60)  # seconds
    timenow    = datetime.datetime.today().strftime("%H:%M:%S")
    timeplus15 = (datetime.datetime.today()+timedelta(seconds=length_of_sleep)).strftime("%H:%M:%S")
    print "sleeping at %s, will resume at %s"%(timenow, timeplus15)
    sys.stdout.flush()
    
    time.sleep(length_of_sleep)
    
def process_output_file(output_dict, output_filename):
    import json
    import datetime
    
    global total_processed
    global first_sleep
    
    if 'errors' not in output_dict:
        if first_sleep:
            with open(output_filename, 'wb') as f:
                first_sleep = False
                for tweet in output_dict:
                    json.dump(tweet,f)
                    f.write("\n")
                    total_processed+=1
        else:
            with open(output_filename, 'a') as f:
                for tweet in output_dict:
                    json.dump(tweet,f)
                    f.write("\n")
                    total_processed+=1
                
        timenow     = datetime.datetime.today().strftime("%H:%M:%S")
        print "%s processed at %s, rows %d"%(output_filename, timenow, total_processed)
    output_dict = []
    
                    
if __name__ == '__main__':
    import sys
    create_jsonfile(sys.argv[1],sys.argv[2],sys.argv[3])