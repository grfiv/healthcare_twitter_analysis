def add_sentiment(input_filename):
    """
    input:  a csv file that has been processed by add_twitter_data_bulk.py
    output: a csv file with *sentiment* field added based on AFINN-111.txt
    use:    %run add_sentiment "Tweets_BleedingDisorders_full.csv"
    """
    import csv
    import re
        
    output_filename   = input_filename.split(".")[0][:-5] + "_sent.csv"
    output_dict       = []  # list of dicts to send to output file
    
    sentiment_words, sentiment_phrases = parse_sentiment_file("AFINN-111.txt")
    
    with open(input_filename, "rb" ) as infile:
       reader     = csv.DictReader(infile)
       lines      = list(reader) # list of all lines/rows in the input file
       totallines = len(lines)   # number of lines in the input file
       print "Rows in input file: " + str(totallines)
       
       # read the input file line-by-line
       # ================================
       for linenum, row in enumerate(lines):
           if row['content']:
               output_row = dict(row)
               clean_text = removeNonAscii(row['content'])
               clean_text = re.sub("""[?!,":.;()|@#]""", "", clean_text.encode('utf-8'))
               clean_text = clean_text.lower()
               word_list  = clean_text.split()
               
               feelings = 0.0
               # single words
               for word in word_list:
                   if 'http' in word: continue
                   if word in sentiment_words:
                       feelings += sentiment_words[word]
               # phrases
               for phrase in sentiment_phrases:
                   if phrase in clean_text:
                       feelings += sentiment_phrases[phrase]
                       
               output_row['sentiment'] = feelings
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
        
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))
        
def parse_sentiment_file(afinnfile):
    """
    Parse the sentiment file
    """
    sentiment_phrases = {}
    sentiment_words   = {}
    
    sentiment_phrases = {}
    sentiment_words   = {}
    sent_file  = open(afinnfile)
    
    for line in sent_file:
      key, val  = line.split("\t")        
      if " " in key:
        sentiment_phrases[key.lower()] = int(val)
      else:
        sentiment_words[key.lower()] = int(val)
    return (sentiment_words, sentiment_phrases)

if __name__ == '__main__':
    import sys
    add_sentiment(sys.argv[1])