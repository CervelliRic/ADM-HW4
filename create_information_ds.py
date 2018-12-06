from os.path import join as pjoin
import os
from pathlib import Path

# For persisting indexes in an external file
import pickle

# Path to the current working directory to refer to all the files relatively
my_path = os.path.dirname(os.path.realpath('__file__'))

information_ds_file = Path(os.path.join(my_path, "indexes/information_dataset.pkl"))


# Existing indexes
listings_file = Path(os.path.join(my_path, "indexes/listings.pkl"))
listing_index_file = Path(os.path.join(my_path, "indexes/listing_index.pkl"))


# Data sets
information_ds_persist = {}

# Master data
listings_persist = {}
listing_index_persist = {}

# Retrieving already persisted information
# Check if indexes exists, if not create new index files
#if yes load the previously persisted indexes and content

# Information data set
if information_ds_file.is_file():
    with open(information_ds_file, "rb") as information_ds:
        information_ds_persist = pickle.load(information_ds)
        information_ds.close()


# Fetching the master data and other useful metadata 
# only if datasets are not present
if(len(information_ds_persist.keys()) == 0):
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


#Preparing information data set
if(len(information_ds_persist.keys()) == 0):

    information_ds_persist['dataset'] = []

    # Get the persisted listings data
    for listing_id in listing_index_persist['listing_ids']:
        cur_listing = listings_persist[listing_id]

        listing_info = [cur_listing['price'], cur_listing['locali'], cur_listing['superficie'], cur_listing['bagni'], cur_listing['piano']]

        information_ds_persist['dataset'].append(listing_info)
    
    #Save information data set
    with open(information_ds_file, "wb") as information_ds:
        pickle.dump(information_ds_persist, information_ds)
        information_ds.close() 

else:
	print("Information data set already present")


print(information_ds_persist['dataset'])

