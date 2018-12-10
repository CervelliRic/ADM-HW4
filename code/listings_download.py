

# Downloading individual listings pages from the listing links persisted
# Please create a directory data_detail
# Checking if the pages are already downloaded
# Check the first file 
listing_detail_file = Path(os.path.join(my_path, "data_detail/listing_detail_0.html"))


if listing_detail_file.is_file() == False:
    
    print('Downloading individual listing pages...')

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

        # Downloading the pages
        for i in range(690, len(links_list)):

            cur_url = links_list[i]

            cur_content = requests.get(cur_url)

            res_text = BeautifulSoup(cur_content.text, "lxml")

            cur_detail_file = os.path.join(my_path, "data_detail/listing_detail_" + str(i) + ".html")

            cur_html_file= open(cur_detail_file, "w")
            cur_html_file.write(str(res_text))
            cur_html_file.close()

            # Wait for 3 seconds before downloading the next page
            time.sleep(3)
else:
    print('Individual listing pages already downloaded')
    