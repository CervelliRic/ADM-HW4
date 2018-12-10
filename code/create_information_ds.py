
#Preparing information data set
if(len(information_ds_persist.keys()) == 0):

    information_ds_persist['dataset'] = []

    # Get the persisted listings data
    for listing_id in listing_index_persist['listing_ids']:
        cur_listing = listings_persist[listing_id]

        listing_info = [cur_listing['price'], cur_listing['locali'], cur_listing['superficie'], cur_listing['bagni'], cur_listing['piano']]

        information_ds_persist['dataset'].append(listing_info)
    
    #Save information data set
    write_file_to_pickle(information_ds_file, information_ds_persist)

else:
    print("Information data set already present")


print(len(information_ds_persist['dataset']))