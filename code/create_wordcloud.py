
def create_wordcloud(clist, stopwords_flag):

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
        plt.savefig(get_wc_save_path(c_index, stopwords_flag))
        #plt.show()

        c_index += 1  


#Creating wordcloud with top 3 similar clusters
# Wordcloud with all the words
create_wordcloud(top_c_list, False)

# Wordcloud without stopwords
create_wordcloud(top_c_list, True)