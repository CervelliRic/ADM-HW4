import time
import requests
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
listing_links_file = Path(os.path.join(my_path, "indexes/listing_links.pkl"))

listing_links_persist = {}

# Retrieving already persisted information
# Check if indexes exists, if not create new index files
#if yes load the previously persisted indexes and content
if listing_links_file.is_file():
    with open(listing_links_file, "rb") as listing_links:
        listing_links_persist = pickle.load(listing_links)
        listing_links.close()

links_list = []

if(len(listing_links_persist.keys()) != 0):

    # Getting listing page links
    for key in  listing_links_persist:
        cur_link = listing_links_persist[key]

        # Check if the link is relative
        # If yes make it absolute link
        # Need to add better checks here
        if(cur_link[0] == "/"):
            cur_link = "https://www.immobiliare.it" + cur_link

        links_list.append(cur_link)


    
    # print(links_list[6960:7000])
    #6960, 7088, 7150, 7905, 8522, 9170
    # Downloading the pages
    for i in range(len(links_list)):
        
        cur_url = links_list[i]

        cur_content = requests.get(cur_url)

        res_text = BeautifulSoup(cur_content.text, "lxml")

        cur_detail_file = os.path.join(my_path, "data_detail/listing_detail_" + str(i) + ".html")

        cur_html_file= open(cur_detail_file, "w")
        cur_html_file.write(str(res_text))
        cur_html_file.close()

        # Wait for 3 seconds before downloading the next page
        time.sleep(5)

