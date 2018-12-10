
# Common utility functions

def extract_number(n):
    n = n.replace('.', '')
    n = n.replace('+', '')
    n_list = [str(s) for s in n.split() if s.isdigit()]

    s = ''.join(n_list).strip()
    
    if not s:
        s = 0

    return int(s)

# Utility functions for reading and writing files using pickel python package
def read_file_from_pickle(file):
    file_content = {}
    
    if file.is_file():
        with open(file, "rb") as f:
            file_content = pickle.load(f)
            f.close()
    
    return file_content

def write_file_to_pickle(file, content):
    with open(file, "wb") as f:
        pickle.dump(content, f)
        f.close()

# Apply Jaccard similarity to find out 3 most similar clusters
def get_jaccard(a, b):
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


# Utility functions for clustering and wordcloud

def get_listing_content(i, sflag):
    listing_words = ''
    if sflag:
        listing_words = listing_content_persist[i]
    else:
        listing_id = listing_index_persist['listing_ids'][i]
        listing_data = listings_persist[listing_id]
        listing_words = listing_data['description']

    return listing_words + ' '

def get_wc_save_path(i, sflag):

    f_name_prefix = ''

    if(sflag):
        f_name_prefix = "wordcloud"
    else:
        f_name_prefix = "wordcloud_all"

    return f_name_prefix + "/cluster_" + str(i)


def compare_clusters(c1, c2):

    jac_score_list = []
    comb_list = []
    cmp_output = {}

    for i in range(len(c1)):
        for j in range(len(c2)):
            # Adding the score of each cluster combination to jac_score_list
            jac_score_list.append(get_jaccard(set(c1[i]), set(c2[j])))
            comb_list.append([i,j])

    cmp_output['score_list'] = jac_score_list
    cmp_output['comb_list'] = comb_list
    
    return cmp_output


def get_similar_clusters(top_3_list, c1, c2):
    similar_clusters = []

    for t in top_3_list:
        t_list = list(t)
        c_list_1 = c1[t_list[1][0]]
        c_list_2 = c2[t_list[1][1]]

        s_list = list(set(c_list_1 + c_list_2))

        similar_clusters.append(s_list)

    return similar_clusters