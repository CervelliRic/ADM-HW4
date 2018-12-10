
if(len(iindex_tf_idf_persist.keys()) == 0):
    
    print("Inverted Indexes are being calculated")

    word_iindex = {}

    #Creating inverted index using tf-idf and consine similarity
    for word in words_persist:
        word_doc_list = vocabulary_persist[words_persist[word]]
        word_iindex[word] = []

        # Store indexes based on number of times a particular word is present in a given document
        for doc in word_doc_list:
            doc_content = listing_content_persist[doc]
            # Pushing the term frequency with document id
            word_iindex[word].append([doc, doc_content.split().count(word)])

    # Store indexes based on tf-idf
    docs_length = len(listing_content_persist.keys())
    iindex_tf_idf_persist = word_iindex

    for key, word in iindex_tf_idf_persist.items():
        # find out the relative importance of a particular terms relating it to document count
        idf= math.log10( docs_length / len(word) )

        for elem in word:
            # Add the document score corresponding to a particular term which we then use in the 
            # search results ranking of documents
            elem[1] = idf * elem[1]
    

    # Persisting the indexes calculated 
    write_file_to_pickle(index_file, iindex_tf_idf_persist)
else:
    print("Inverted Indexes already present")
    