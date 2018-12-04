import time
import requests
from bs4 import BeautifulSoup

url_root = 'https://www.immobiliare.it/vendita-case/roma/?criterio=rilevanza&pag='


for i in range(844, 1001):
    
    cur_url = url_root + str(i)

    cur_content = requests.get(cur_url)

    res_text = BeautifulSoup(cur_content.text, "lxml")

    cur_html_file= open("listing_" + str(i) + ".html", "w")
    cur_html_file.write(str(res_text))
    cur_html_file.close()

    time.sleep(5)




