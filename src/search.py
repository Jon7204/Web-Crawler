from math import log

# Print the word, its frequency, and positions in the URL
def print_word(word, index):
    if word in index:
        print(f"Word: '{word}'")
        for url, data in index[word].items():
            print(f"  URL: {url}")
            print(f"    Frequency: {data['frequency']}")
            print(f"    Positions: {data['positions']}")
    else:
        print(f"Word '{word}' not found in index.")

# Find pages that contain all the words in the list
def find_pages(list_of_words, index):
    if not list_of_words or list_of_words[0] not in index:
        return set()
    urls = set(index[list_of_words[0]].keys())
    for word in list_of_words[1:]:
        if word not in index:
            return set()
        urls = urls.intersection(set(index[word].keys()))
    
    # Compute TF-IDF scores for the URLs and sort them
    scored_urls = [(sum(compute_tfidf(word, url, index) for word in list_of_words), url) for url in urls]
    scored_urls.sort(reverse=True)
    return scored_urls

# Parse the query and return matching pages based on AND, OR, NOT operators
def parse_query(query, index):
    if " AND " in query:
        words = query.split(" AND ")
        # what if a word isn't in the index?
        for word in words:
            if word not in index:
                print(f"  '{word}' not found in index.")
                return []
        return find_pages(words, index)
    
    elif " OR " in query:
        words = query.split(" OR ")
        urls = set()
        for word in words:
            if word in index:
                urls.update(set(index[word].keys()))
            else:
                print(f"  '{word}' not found in index.")
                pass
        if not urls:
            print("  No URLs found.")
            return []
        scored = [(sum(compute_tfidf(word, url, index) for word in words), url) for url in urls]
        scored.sort(reverse=True)
        return scored
    
    elif " NOT " in query:
        words = query.split(" NOT ")
        include_urls = set(index[words[0]].keys()) if words[0] in index else set()
        exclude_urls = set(index[words[1]].keys()) if words[1] in index else set()
        if not include_urls:
            print(f"  '{words[0]}' not found in index.")
            return []
        final_urls = include_urls - exclude_urls
        scored = [(sum(compute_tfidf(word, url, index) for word in [words[0]]), url) for url in final_urls]
        scored.sort(reverse=True)
        return scored
    
    else:
        return find_pages(query.split(), index)

# Compute the TF-IDF score for a given word and URL
def compute_tfidf(word, url, index):
    if word not in index or url not in index[word]:
        return 0.0
    
    # Term Frequency (TF)
    tf = index[word][url]['frequency']
    
    # Inverse Document Frequency (IDF)
    total_docs = len(set(u for word_data in index.values() for u in word_data))
    docs_with_word = len(index[word])
    idf = log(total_docs / (1 + docs_with_word))  # Adding 1 to avoid division by zero
    
    return tf * idf