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
        return []
    urls = set(index[list_of_words[0]].keys())
    for word in list_of_words[1:]:
        if word not in index:
            return []
        urls = urls.intersection(set(index[word].keys()))
    
    # Compute TF-IDF scores for the URLs and sort them
    scored_urls = [(sum(compute_tfidf(word, url, index) for word in list_of_words), url) for url in urls]
    scored_urls.sort(reverse=True)
    return scored_urls

# Parse the query and return matching pages based on AND, OR, NOT operators
def parse_query(query, index):
    query = query.strip()
    if not query:
        print("  Empty query.")
        return []

    if " AND " in query:
        words = [word.strip() for word in query.split(" AND ")] # Strip whitespace from each word
        for word in words:
            if word == "" or word.isspace(): # Check for empty or whitespace-only words
                print("  Empty word in query.")
                return []
            elif word not in index: # Check if the word is not in the index
                print(f"  '{word}' not found in index.")
                return []
        return find_pages(words, index) # Use the find_pages function to get URLs that contain all the words
    
    elif " OR " in query:
        words = [word.strip() for word in query.split(" OR ")] # Strip whitespace from each word
        urls = set()
        for word in words:
            if word == "" or word.isspace(): # Check for empty or whitespace-only words
                print("  Empty word in query.")
                return []
            elif word in index:
                urls.update(set(index[word].keys())) # Add URLs that contain the word to the set
            else:
                print(f"  '{word}' not found in index.")
                pass
        if not urls:
            print("  No URLs found.")
            return []
        # Compute TF-IDF scores for the URLs and sort them
        scored = [(sum(compute_tfidf(word, url, index) for word in words), url) for url in urls]
        scored.sort(reverse=True)
        return scored
    
    elif " NOT " in query:
        words = [word.strip() for word in query.split(" NOT ")] # Strip whitespace from each word
        if len(words) != 2:
            print("  Invalid NOT query format. Use 'word1 NOT word2'.")
            return []
        if words[0] == words[1]:
            print("  Cannot exclude the same word you're searching for.")
            return []
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