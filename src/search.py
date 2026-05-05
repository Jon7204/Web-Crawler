from math import log
from difflib import get_close_matches

# Print the word, its frequency, and positions in the URL
def print_word(word, index):
    if word in index:
        print(f"  Word: '{word}'")
        for url, data in index[word].items(): # Retrieve each URL and its associated data for the word
            print(f"  URL: {url}")
            print(f"    Frequency: {data['frequency']}")
            print(f"    Positions: {data['positions']}")
    else:
        print(f"  Word '{word}' not found in index.")
        suggest_word(word, index)   

# Find pages that contain all the words in the list
def find_pages(list_of_words, index):
    if not list_of_words or list_of_words[0] not in index: # Check if the list is empty or if the first word is not in the index
        if list_of_words:
             print(f"  Word not found in index: {list_of_words[0]}")
             suggest_word(list_of_words[0], index)   
        else:
            print(f"  No pages found for words: {list_of_words}")
        return []
    
    urls = set(index[list_of_words[0]].keys()) # Start with the set of URLs that contain the first word
    for word in list_of_words[1:]: 
        if word not in index:
            print(f"  Word not found in index: {word}")
            suggest_word(word, index)   
            return []
        urls = urls.intersection(set(index[word].keys())) # Intersect with the set of URLs that contain the next word to find common URLs

    if not urls:
        print(f"  No pages found for words: {list_of_words}")
        return []

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
    for operator in ["AND", "OR", "NOT"]:
        if query.startswith(operator + " ") or query.endswith(" " + operator):
            print(f"  Invalid query: cannot start or end with '{operator}'.")
            return []

    # find_pages already handles AND logic, so just split on " AND " and pass the words to find_pages
    if " AND " in query: 
        words = [word.strip() for word in query.split(" AND ")] # Strip whitespace from each word
        for word in words:
            if word == "" or word.isspace(): # Check for empty or whitespace-only words
                print("  Empty word in query.")
                return []
            elif word not in index: # Check if the word is not in the index
                print(f"  '{word}' not found in index.")
                suggest_word(word, index) 
                return []
        return find_pages(words, index)
    
    # OR logic: find all URLs that contain any of the words, then compute TF-IDF scores and sort them
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
                suggest_word(word, index)
                pass
        if not urls:
            print("  No URLs found.")
            return []
        # Compute TF-IDF scores for the URLs and sort them
        scored = [(sum(compute_tfidf(word, url, index) for word in words), url) for url in urls]
        scored.sort(reverse=True)
        return scored
    
    # NOT logic: find URLs that contain the first word but not the second word, then compute TF-IDF scores and sort them
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
            suggest_word(words[0], index) 
            return []
        final_urls = include_urls - exclude_urls
        if not final_urls:
            print(f"  No URLs found for '{words[0]}' excluding '{words[1]}'.")
            return []
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

# Suggest similar words if the exact word is not found in the index
def suggest_word(word, index):
    all_words = list(index.keys())
    suggestions = get_close_matches(word, all_words, n=3, cutoff=0.6) # Get up to 3 close matches with a similarity cutoff of 0.6
    if suggestions:
        print(f"  Did you mean: {', '.join(suggestions)}?")
    else:
        print(f"  No similar words found in index for '{word}'.")