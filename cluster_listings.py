
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

# @TODO: Based on the optimial cluster count from Elbow method
print('Clustering for Information Dataset: ')
ids_c_list = cluster_documents(information_ds_persist['dataset'], 10)

print('Clustering for Description Dataset: ')
dds_c_list = cluster_documents(description_ds_persist['dataset'], 10)

# Jaccard similarity
print('Applying Jacard similarity for the clusters: ')
cmp_output  = compare_clusters(ids_c_list, dds_c_list)

# Getting top 3 similar clusters and use it to generate wordcloud
top_3_tuple = sorted(zip(cmp_output['score_list'], cmp_output['comb_list']), reverse=True)[:3]
top_3_list = list(top_3_tuple)

#Preparing the cluster list for generating word cloud
top_c_list = get_similar_clusters(top_3_list, ids_c_list, dds_c_list)