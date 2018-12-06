import math
from sklearn.cluster import KMeans
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from os.path import join as pjoin
import os
from pathlib import Path

# For persisting indexes in an external file
import pickle

# Path to the current working directory to refer to all the files relatively
my_path = os.path.dirname(os.path.realpath('__file__'))

information_ds_file = Path(os.path.join(my_path, "indexes/information_dataset.pkl"))
description_ds_file = Path(os.path.join(my_path, "indexes/description_dataset.pkl"))

listings_file = Path(os.path.join(my_path, "indexes/listings.pkl"))
listing_links_file = Path(os.path.join(my_path, "indexes/listing_links.pkl"))
listing_index_file = Path(os.path.join(my_path, "indexes/listing_index.pkl"))

content_file = Path(os.path.join(my_path, "indexes/listing_content.pkl"))

# Data sets
description_ds_persist = {}
information_ds_persist = {}

# Meta data for listings
listings_persist = {}
listing_index_persist = {}
listing_content_persist = {}

if listings_file.is_file():
    with open(listings_file, "rb") as listings:
        listings_persist = pickle.load(listings)
        listings.close()
        
if listing_index_file.is_file():
    with open(listing_index_file, "rb") as listing_index:
        listing_index_persist = pickle.load(listing_index)
        listing_index.close()

if content_file.is_file():
    with open(content_file, "rb") as listing_content:
        listing_content_persist = pickle.load(listing_content)
        listing_content.close()


# Information data set
if information_ds_file.is_file():
    with open(information_ds_file, "rb") as information_ds:
        information_ds_persist = pickle.load(information_ds)
        information_ds.close()

# Description data set - containing tf-idf values
if description_ds_file.is_file():
    with open(description_ds_file, "rb") as description_ds:
        description_ds_persist = pickle.load(description_ds)
        description_ds.close()


def get_listing_content(i, sflag):
    listing_words = ''
    if sflag:
        listing_words = listing_content_persist[i]
    else:
        listing_id = listing_index_persist['listing_ids'][i]
        listing_data = listings_persist[listing_id]
        listing_words = listing_data['description']

    return listing_words + ' '

def get_wc_save_path(i, iflag, sflag):

    f_name_head = ''
    f_name_tail = ''

    if(iflag):
        f_name_head = "wordcloud_ids"
    else:
        f_name_head = "wordcloud_dds"

    if(sflag):
        f_name_tail = ""
    else:
        f_name_tail = "_all"

    return f_name_head + f_name_tail + "/cluster_" + str(i)


# data - is the dataset
# k  - number of clusters
# @TODO: Need to use Elbow method to decide on
# Optimal number of clusters

def cluster_documents(data, k):       
    #use k-means to clusterize the songs
    kmeans = KMeans(n_clusters=k, init='random') # initialization
    kmeans.fit(data) # actual execution
    c = kmeans.predict(data)
    c_list = list(c)

    clustered_list = []

    # Creating a multi dimentional array based on k
    for c in range(k):
        clustered_list.append([])

    # Extract the listing ids from indexes
    index = 0
    for i in c_list:
        clustered_list[i].append(index)
        index += 1
    
    return clustered_list


def create_wordcloud(clist, dataset_flag, stopwords_flag):

    c_index = 0   
    
    for cluster in clist:
        
        cur_cluster_words = " "
        
        # Extracting all the words of the listings in current cluster
        for list_id in cluster:
            cur_cluster_words +=  get_listing_content(list_id, stopwords_flag)
        
        #strg_cloud = ' '.join(strg_cloud.split())
        
        wordcloud = WordCloud(width = 300, height = 300, margin = 0, collocations=False).generate(cur_cluster_words)
        
        plt.imshow(wordcloud, interpolation = "bilinear")
        plt.axis("off")
        plt.margins(x=0,y=0)
        plt.savefig(get_wc_save_path(c_index, dataset_flag, stopwords_flag))
        plt.show()

        c_index += 1  


print('Clustering for Information Dataset: ')
ids_c_list = cluster_documents(information_ds_persist['dataset'], 10)

print('Generating wordcloud for the clusters with all the words: ')
create_wordcloud(ids_c_list, True, False)

print('Generating wordcloud for the clusters without stopwords: ')
create_wordcloud(ids_c_list, True, True)

print('Clustering for Description Dataset: ')
dds_c_list = cluster_documents(description_ds_persist['dataset'], 10)

print('Generating wordcloud for the clusters with all the words: ')
create_wordcloud(dds_c_list, False, False)

print('Generating wordcloud for the clusters without stopwords: ')
create_wordcloud(dds_c_list, False, True)


