from os.path import join as pjoin
import os
from pathlib import Path

# For persisting indexes in an external file
import pickle

import nltk
# For word tokenization
from nltk.tokenize import RegexpTokenizer
# For stop words list
from nltk.corpus import stopwords
# For word stemming
from nltk.stem.snowball import SnowballStemmer

#First we import stopwords from nltk
nltk.download('stopwords')
stop_words = set(stopwords.words('italian'))
#To remove punctuation we use regexptokenizer, but we leave dollar symbol $ because maybe is used in some queries
tokenizer = RegexpTokenizer(r'\w+|\$')
#we create the stemmer
ps = SnowballStemmer('italian')

# Path to the current working directory to refer to all the files relatively
my_path = os.path.dirname(os.path.realpath('__file__'))

# Existing indexes
listings_file = Path(os.path.join(my_path, "indexes/listings.pkl"))
listing_index_file = Path(os.path.join(my_path, "indexes/listing_index.pkl"))

# Retrieving persisted information for listing content and word map
# Please create a directory(in your current working directory) with name 'indexes'  
content_file = Path(os.path.join(my_path, "indexes/listing_content.pkl"))
vocabulary_file = Path(os.path.join(my_path, "indexes/vocabulary.pkl"))
words_file = Path(os.path.join(my_path, "indexes/words.pkl"))

vocabulary_persist = {}
words_persist = {}
listing_content_persist = {}

if content_file.is_file():
    with open(content_file, "rb") as listing_content:
        listing_content_persist = pickle.load(listing_content)
        listing_content.close()
        
# Check if the vocabulary file exists, 
#if yes load the previously persisted vocabulary
if vocabulary_file.is_file():
    with open(vocabulary_file, "rb") as vocabulary:
        vocabulary_persist = pickle.load(vocabulary)
        vocabulary.close()
            
# Check if the words file exists, 
#if yes load the previously persisted words
if words_file.is_file():
    with open(words_file, "rb") as words:
        words_persist = pickle.load(words)
        words.close()


# Fetching the master data and other useful metadata 
# only if datasets are not present
if(len(listing_content_persist.keys()) == 0):
    # Listings data
    if listings_file.is_file():
        with open(listings_file, "rb") as listings:
            listings_persist = pickle.load(listings)
            listings.close()

    # Getting order of individual listings        
    if listing_index_file.is_file():
        with open(listing_index_file, "rb") as listing_index:
            listing_index_persist = pickle.load(listing_index)
            listing_index.close()

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
                sr = ps.stem(r)
                
                listing_words.append(sr)
                
                if not  sr in listing_word_map:
                    listing_word_map[sr] = [i]
                else:
                    listing_word_map[sr]+=[i]
                    
                    
        listing_content_persist[i] = ' '.join(listing_words)
    
    # Saving the content and indexes for the first time
    # We made use of pickel python module
    #Saving content dictionary
    with open(content_file, "wb") as listing_content:
        pickle.dump(listing_content_persist, listing_content)
        listing_content.close()
    
    # Word and Vocabulary indexes based on word map
    c = 0
    for key in listing_word_map:
        words_persist[key] = c
        vocabulary_persist[c] = listing_word_map[key]
        c += 1
    
    #Save vocabulary and words
    with open(vocabulary_file, "wb") as vocabulary:
        pickle.dump(vocabulary_persist, vocabulary)
        vocabulary.close()
          
    with open(words_file, "wb") as words:
        pickle.dump(words_persist, words)
        words.close()
