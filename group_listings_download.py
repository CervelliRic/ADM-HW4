
# Please create a directory 'data' 
# Checking if the pages are already downloaded
# Check the first file 
listing_page_file = Path(os.path.join(my_path, "data/listing_0.html"))

if listing_page_file.is_file() == False:

    # If there are no files then start downloading each html file with a delay of 3 seconds
    print('Downloading group listings pages...')
    
    url_root = 'https://www.immobiliare.it/vendita-case/roma/?criterio=rilevanza&pag='


    for i in range(1000):

        cur_url = url_root + str(i)

        cur_content = requests.get(cur_url)

        res_text = BeautifulSoup(cur_content.text, "lxml")

        cur_html_file= open("data/listing_" + str(i) + ".html", "w")
        cur_html_file.write(str(res_text))
        cur_html_file.close()
        
        # 3 seconds delay for the next page download attempt
        time.sleep(3)
else:
    print('Group listings pages already downloaded')