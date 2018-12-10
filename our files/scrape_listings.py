
# If this is True then the listing description is updated from 
# the individual pages
desc_flag = False

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
        for cur_listing in listing_container.find_all(class_=["listing-item", "js-row-detail"], recursive=False):

            listing_dict = {
                "id": "",
                "listing_id": "",
                "title": "",
                "price": 0,
                "locali": 0,
                "superficie": 0,
                "bagni": 0,
                "piano": 0,
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
                        listing_dict['price'] = extract_number(cur_feature.text.strip())
                    else:
                        # Extract other features information
                        # @TODO: Need to refine locali to contain a list: example: 1-5 should be [1,2,3,4,5]
                        feature_name = cur_feature.find(class_="lif--muted")

                        # @TODO: Need to do this more efficiently
                        if(feature_name):
                            feature_name = feature_name.text.strip()

                            if feature_name in listing_dict:
                                feature_value = cur_feature.find(class_="text-bold").text.strip()
                                listing_dict[feature_name] = extract_number(feature_value)


                listing_index_persist['listing_ids'].append(listing_dict['listing_id'])

                l_index += 1
                listings_persist[listing_dict['listing_id']] = listing_dict


    # Remove duplicate listing entries
    listing_index_persist['listing_ids'] = list(set(listing_index_persist['listing_ids']))

    # Persist the listings object and dictionary using pickel library
    
    #Save listings data
    write_file_to_pickle(listings_file, listings_persist)

    #Save individual listings links data
    write_file_to_pickle(listing_links_file, listing_links_persist)

    #Save index of listings
    write_file_to_pickle(listing_index_file, listing_index_persist)

else:
    print("Indexes are already created")


print("No of links:")
print(len(listing_links_persist.keys()))

print("No of listings:")
print(len(listings_persist.keys()))

print("No of listings in the listing index file:")
print(len(listing_index_persist['listing_ids']))


if desc_flag:

    # Parse the detail pages 
    # And update the description of individual listings
    for i in range(len(listing_links_persist.keys())):
        cur_detail_page = BeautifulSoup(open(os.path.join(my_path, 'data_detail/listing_detail_' + str(i) + '.html')), 'html.parser')

        cur_page_contact = cur_detail_page.find('div',{"id":"up-contact-box"})
        if cur_page_contact:
            cur_page_elem = cur_page_contact.find(class_="info-agenzia")

            if cur_page_elem:
                cur_page_id = cur_page_elem.get("data-annuncio")

                cur_page_description =  cur_detail_page.find(class_="description-text")

                if cur_page_description:
                    cur_page_description = cur_page_description.text.strip()

                    cur_page_description = "".join(cur_page_description.splitlines())

                    if cur_page_id in listings_persist:
                        listings_persist[cur_page_id]['description'] = cur_page_description
                    else:
                        pass
                        #print("Page key not found in the persisted data")
                else:
                    pass
                    #print("Page Description not found")
            else:
                pass
                #print("Page ID not found")
        else:
            pass
            #print("Contact not found")

    #Save listings data with new content (complete listing description)
    write_file_to_pickle(listings_file, listings_persist)