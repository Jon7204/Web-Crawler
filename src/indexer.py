import re
from bs4 import BeautifulSoup

# Ignore common stop words to reduce noise in the index
STOPWORDS = {"the", "a", "an", "is", "it", "in", "on", "at", "to", "and", "or", "of", "for", "with", "that", "this", "was", "are"}
 
 # Extract text from HTML
def extract_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Tokenize text into words, converting to lowercase and removing punctuation
def tokenize(text):
    tokens = re.findall(r'\b\w+\b', text.lower())
    return [token for token in tokens if token not in STOPWORDS]

# Build reverse index
def build_index(pages):
    index = {}
    # Iterate through each page 
    for url, html in pages.items():
        text = extract_text(html)
        tokens = tokenize(text)

        # Update the index with token frequencies and positions
        for position, token in enumerate(tokens):
            if token not in index: # If the token is not already in the index, add it
                index[token] = {}
            if url not in index[token]: # If the URL is not already associated with the token, add it
                index[token][url] = {"frequency": 0, "positions": []}
            index[token][url]["frequency"] += 1
            index[token][url]["positions"].append(position)
    return index