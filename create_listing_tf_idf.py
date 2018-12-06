from os.path import join as pjoin
import os
from pathlib import Path

# For persisting indexes in an external file
import pickle

import math

# Path to the current working directory to refer to all the files relatively
my_path = os.path.dirname(os.path.realpath('__file__'))

# Check if the index file exists, if yes load the previously persisted indexes and content
# Please create a directory(in your current working directory) with name indexes  
index_file = Path(os.path.join(my_path, "indexes/iindex_tf_idf.pkl"))

# Retrieving persisted information for listing content and word map
# Please create a directory(in your current working directory) with name 'indexes'  
content_file = Path(os.path.join(my_path, "indexes/listing_content.pkl"))
vocabulary_file = Path(os.path.join(my_path, "indexes/vocabulary.pkl"))
words_file = Path(os.path.join(my_path, "indexes/words.pkl"))

iindex_tf_idf_persist = {}
vocabulary_persist = {}
words_persist = {}
listing_content_persist = {}

# Check if the index file exists, if yes load the previously persisted indexes
if index_file.is_file():
    # Retriving precreated inverted indexes
    with open(index_file, "rb") as iindex_tf_idf:
        iindex_tf_idf_persist = pickle.load(iindex_tf_idf)
        iindex_tf_idf.close()

if(len(iindex_tf_idf_persist.keys()) == 0):

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


if(len(iindex_tf_idf_persist.keys()) == 0):
    
    print("Inverted Indexes are being calculated")

    word_iindex = {}

    #Creating inverted index using tf-idf and consine similarity
    for word in words_persist:
        word_doc_list = vocabulary_persist[words_persist[word]]
        word_iindex[word] = []

        # Store indexes based on number of times a particular word is present in a given document
        for doc in word_doc_list:
            doc_content = listing_content_persist[doc]
            # Pushing the term frequency with document id
            word_iindex[word].append([doc, doc_content.split().count(word)])

    # Store indexes based on tf-idf
    docs_length = len(listing_content_persist.keys())
    iindex_tf_idf_persist = word_iindex

    for key, word in iindex_tf_idf_persist.items():
        # find out the relative importance of a particular terms relating it to document count
        idf= math.log10( docs_length / len(word) )

        for elem in word:
            # Add the document score corresponding to a particular term which we then use in the 
            # search results ranking of documents
            elem[1] = idf * elem[1]
    

    # Persisting the indexes calculated 
    with open(index_file, "wb") as iindex_tf_idf:
        pickle.dump(iindex_tf_idf_persist, iindex_tf_idf)
        iindex_tf_idf.close()
    

