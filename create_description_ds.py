from os.path import join as pjoin
import os
from pathlib import Path

# For persisting indexes in an external file
import pickle

# Path to the current working directory to refer to all the files relatively
my_path = os.path.dirname(os.path.realpath('__file__'))

description_ds_file = Path(os.path.join(my_path, "indexes/description_dataset.pkl"))

# Existing indexes
listings_file = Path(os.path.join(my_path, "indexes/listings.pkl"))
listing_index_file = Path(os.path.join(my_path, "indexes/listing_index.pkl"))
content_file = Path(os.path.join(my_path, "indexes/listing_content.pkl"))
vocabulary_file = Path(os.path.join(my_path, "indexes/vocabulary.pkl"))
words_file = Path(os.path.join(my_path, "indexes/words.pkl"))
index_file = Path(os.path.join(my_path, "indexes/iindex_tf_idf.pkl"))


# Data sets
description_ds_persist = {}

# Master data
listings_persist = {}
listing_index_persist = {}

# Meta data for creating description dataset
listing_content_persist = {}
vocabulary_persist = {}
words_persist = {}
iindex_tf_idf_persist = {}

# Retrieving already persisted information
# Check if indexes exists, if not create new index files
#if yes load the previously persisted indexes and content

# Description data set - containing tf-idf values
if description_ds_file.is_file():
    with open(description_ds_file, "rb") as description_ds:
        description_ds_persist = pickle.load(description_ds)
        description_ds.close()

# Fetching the master data and other useful metadata 
# only if datasets are not present
if(len(description_ds_persist.keys()) == 0):
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
    
    # Check if the index file exists, 
    # if yes load the previously persisted indexes
    if index_file.is_file():
        # Retriving precreated inverted indexes
        with open(index_file, "rb") as iindex_tf_idf:
            iindex_tf_idf_persist = pickle.load(iindex_tf_idf)
            iindex_tf_idf.close()

# Preparing Description data set
# Create description data set
# Extract the words in individual listings
# Create a matrix with rows as listings and columns as words
# Combile listing title and description
# Remove stop words
# Calculate the term frequency
# Calculate the td*idf score for that word in that document
# Which gives the description data set for the 10000 listings saved
if(len(description_ds_persist.keys()) == 0):

    print("Description data set is being created...")

    list_len = len(listing_index_persist['listing_ids'])
    description_ds = []
    
    #Build the description data set
    for i in range(list_len):
        
        cur_list_id = listing_index_persist['listing_ids'][i]
        
        cur_list_obj = listings_persist[cur_list_id]

        cur_word_list = []
        
        #Initialize each word tf-idf with 0's
        for word in words_persist:
            cur_word_list.append(0)

        # @TODO: Need to optimize the number of verfications done here
        for key, word in iindex_tf_idf_persist.items():
            # elem[0] - list_id
            # elem[1] - tf-idf
            for elem in word:
               # Update tf-idf of that word for that listing 
               if(elem[0] == i):
                   cur_word_list[words_persist[key]] = elem[1]
        
        description_ds.append(cur_word_list)

    description_ds_persist['dataset'] = description_ds


    # Persisting the indexes calculated 
    with open(description_ds_file, "wb") as description_ds:
        pickle.dump(description_ds_persist, description_ds)
        description_ds.close()
else:
	print("Description data set already present")
    
print(len(description_ds_persist['dataset'][6789]))