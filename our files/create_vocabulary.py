
#First we import stopwords from nltk
nltk.download('stopwords')
stop_words = set(stopwords.words('italian'))
#To remove punctuation we use regexptokenizer, but we leave dollar symbol $ because maybe is used in some queries
tokenizer = RegexpTokenizer(r'\w+|\$')
#we create the stemmer
ps = SnowballStemmer('italian')

list_len = len(listing_index_persist['listing_ids'])

if(len(listing_content_persist.keys()) == 0):
    
    listing_word_map = {}
    
    # We reach here if we don't have indexes already present
    print("Vocabulary is being created...")
 
    for i in range(list_len):
        
        cur_list_id = listing_index_persist['listing_ids'][i]
        
        cur_list_obj = listings_persist[cur_list_id]

        # Extract all the text in the individual listing
        # For listing title
        t1 = cur_list_obj['title']
        
        # For listing content
        t2 = cur_list_obj['description']
        
        t = t1+ ' ' +t2
        t = t.lower()
        t = tokenizer.tokenize(t)
        
        # This array will contain all the valid words in a given review after removing 
        # all the stop words, punctuations, stemming etc..,, we will use this information
        # to find out the term frequency there by tf-idf values
        listing_words = []
        
        for r in t :
            if not r in stop_words:
                sr = r #ps.stem(r) - avoid stemming for now for the wordcloud
                
                listing_words.append(sr)
                
                if not  sr in listing_word_map:
                    listing_word_map[sr] = [i]
                else:
                    listing_word_map[sr]+=[i]
                    
                    
        listing_content_persist[i] = ' '.join(listing_words)
    
    # Saving the content and indexes for the first time
    # We made use of pickel python module
    #Saving content dictionary
    write_file_to_pickle(content_file, listing_content_persist)
    
    # Word and Vocabulary indexes based on word map
    c = 0
    for key in listing_word_map:
        words_persist[key] = c
        vocabulary_persist[c] = listing_word_map[key]
        c += 1
    
    #Save vocabulary and words
    write_file_to_pickle(vocabulary_file, vocabulary_persist)
    write_file_to_pickle(words_file, words_persist)
else:
    print("Vocabulary data set already present")