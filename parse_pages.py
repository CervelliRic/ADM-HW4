from bs4 import BeautifulSoup

from os.path import join as pjoin
import os
from pathlib import Path

import html

from lxml import html

# For persisting indexes in an external file
import pickle

# Path to the current working directory to refer to all the files relatively
my_path = os.path.dirname(os.path.realpath('__file__'))

listings_file = Path(os.path.join(my_path, "indexes/listings.pkl"))
listing_links_file = Path(os.path.join(my_path, "indexes/listing_links.pkl"))
listing_index_file = Path(os.path.join(my_path, "indexes/listing_index.pkl"))

listings_persist = {}
listing_index_persist = {}
#Contains information about the link for individual listing
# We will scrape this information separately and update master data structure of all the listings
listing_links_persist = {}

# Extract only the number in the price
def extract_price(price_str):
    price_str = price_str.replace('.', '')
    str_list = [str(s) for s in price_str.split() if s.isdigit()]

    return ''.join(str_list)


# Retrieving already persisted information
# Check if indexes exists, if not create new index files
#if yes load the previously persisted indexes and content

if listings_file.is_file():
    with open(listings_file, "rb") as listings:
        listings_persist = pickle.load(listings)
        listings.close()

if listing_links_file.is_file():
    with open(listing_links_file, "rb") as listing_links:
        listing_links_persist = pickle.load(listing_links)
        listing_links.close()
        
if listing_index_file.is_file():
    with open(listing_index_file, "rb") as listing_index:
        listing_index_persist = pickle.load(listing_index)
        listing_index.close()

if(len(listing_index_persist.keys()) == 0):

    print("Indexes are being created")

    l_index = 0
    listing_index_persist['listing_ids'] = []

    # Every page has 25 listings so
    # 410*25 will be more than 10000 listings
    for i in range(1, 410):

        cur_listing_page = BeautifulSoup(open(os.path.join(my_path, 'data/listing_' + str(i) + '.html')), 'html.parser')

        listing_container = cur_listing_page.find(class_="annunci-list")



        # Need to improve exception handling in this loop
        # Extract the information of individual listing
        for cur_listing in listing_container.find_all(class_=["listing-item", "js-row-detail"], recursive=False):

            listing_dict = {
                "id": "",
                "listing_id": "",
                "title": "",
                "price": "",
                "locali": "",
                "superficie": "",
                "bagni": "",
                "piano": "",
                "immobile": "",
                "listing_link": "",
                "description": ""
            }

            listing_body = cur_listing.find(class_="listing-item_body")

            if(listing_body):

                listing_dict['id'] = l_index
                listing_dict['listing_id'] = cur_listing.get("data-id")

                listing_dict['title'] = listing_body.find(class_="titolo").text.strip()

                listing_dict["listing_link"] = listing_body.find("a", {"id": "link_ad_" + listing_dict['listing_id']}).get("href")

                listing_dict['description'] = listing_body.find(class_="descrizione").text.strip()

                # Extracting the listing features 
                listing_features = listing_body.find(class_=["listing-features", "list-piped"])

                listing_links_persist[listing_dict['listing_id']] = listing_dict["listing_link"]

                for cur_feature in listing_features.find_all(class_="lif__item", recursive=False):

                    feature_cls_list = cur_feature.get("class")

                    # Extract listing price
                    if 'lif__pricing' in feature_cls_list:
                        listing_dict['price'] = extract_price(cur_feature.text.strip())
                    else:
                        # Extract other features information
                        # @TODO: Need to refine locali to contain a list: example: 1-5 should be [1,2,3,4,5]
                        feature_name = cur_feature.find(class_="lif--muted")

                        # @TODO: Need to do this more efficiently
                        if(feature_name):
                            feature_name = feature_name.text.strip()

                            if feature_name in listing_dict:
                                feature_value = cur_feature.find(class_="text-bold").text.strip()
                                listing_dict[feature_name] = feature_value


                listing_index_persist['listing_ids'].append(listing_dict['listing_id'])

                l_index += 1
                listings_persist[listing_dict['listing_id']] = listing_dict


    # Remove duplicate listing entries
    listing_index_persist['listing_ids'] = list(set(listing_index_persist['listing_ids']))

    # Persist the listings object and dictionary using pickel library
    #Save listings data
    with open(listings_file, "wb") as listings:
        pickle.dump(listings_persist, listings)
        listings.close()

    #Save individual listings links data
    with open(listing_links_file, "wb") as listing_links:
        pickle.dump(listing_links_persist, listing_links)
        listing_links.close()

    #Save index of listings
    with open(listing_index_file, "wb") as listing_index:
        pickle.dump(listing_index_persist, listing_index)
        listing_index.close()

else:
    print("Indexes are already created")


print("No of links:")
print(len(listing_links_persist.keys()))

print("No of listings:")
print(len(listings_persist.keys()))

print("No of listings in the listing index file:")
print(len(listing_index_persist['listing_ids']))