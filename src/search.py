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
    return urls