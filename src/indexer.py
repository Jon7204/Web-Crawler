import re
from bs4 import BeautifulSoup
 
def extract_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

def build_index(pages):
    index = {}
    for url, html in pages.items():
        text = extract_text(html)
        tokens = tokenize(text)
        for position, token in enumerate(tokens):
            if token not in index:
                index[token] = {}
            if url not in index[token]:
                index[token][url] = {"frequency": 0, "positions": []}
            index[token][url]["frequency"] += 1
            index[token][url]["positions"].append(position)
    return index