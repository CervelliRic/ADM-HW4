
# Import all the persisted data at once
# Data to import: 
# Listing data, Individual listing links, Listing Index 
# Words, Vocabulary, listing_content, iindex_tf_idf
# information_dataset, description_dataset

# Path to the current working directory to refer to all the files relatively
my_path = os.path.dirname(os.path.realpath('__file__'))

# Datastructures for holding the listings and other metadata
# Please create a directory(in your current working directory) with name 'indexes'  

#Holds individual listings data for the listing pages downloaded
listings_file = Path(os.path.join(my_path, "indexes/listings.pkl"))
listings_persist = {}

if listings_file.is_file():
    with open(listings_file, "rb") as listings:
        listings_persist = pickle.load(listings)
        listings.close()

#Holds the URLs of individual listings for extracting complete description of a particular listing
listing_links_file = Path(os.path.join(my_path, "indexes/listing_links.pkl"))
listing_links_persist = read_file_from_pickle(listing_links_file)


#Holds the order of individual listing
listing_index_file = Path(os.path.join(my_path, "indexes/listing_index.pkl"))
listing_index_persist = read_file_from_pickle(listing_index_file)
     

# Retrieving persisted information for listing content and word map (words and vocabulary)
content_file = Path(os.path.join(my_path, "indexes/listing_content.pkl"))
listing_content_persist = read_file_from_pickle(content_file)



vocabulary_file = Path(os.path.join(my_path, "indexes/vocabulary.pkl"))
vocabulary_persist = read_file_from_pickle(vocabulary_file)

words_file = Path(os.path.join(my_path, "indexes/words.pkl"))
words_persist = read_file_from_pickle(words_file)
        
index_file = Path(os.path.join(my_path, "indexes/iindex_tf_idf.pkl"))
iindex_tf_idf_persist = read_file_from_pickle(index_file)


# Information data set
information_ds_file = Path(os.path.join(my_path, "indexes/information_dataset.pkl"))
information_ds_persist = read_file_from_pickle(information_ds_file)

# Description data set - containing tf-idf values
description_ds_file = Path(os.path.join(my_path, "indexes/description_dataset.pkl"))
description_ds_persist = read_file_from_pickle(description_ds_file)