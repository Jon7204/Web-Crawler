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