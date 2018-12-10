
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
    write_file_to_pickle(description_ds_file, description_ds_persist)
    
else:
    print("Description data set already present")
    
#print(description_ds_persist['dataset'][789])