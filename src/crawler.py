import requests
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def crawl(base_url, politeness_window=6):
    visited = set()
    to_visit = [base_url]
    pages = {}

    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue
        try:
            response = requests.get(url)
            response.raise_for_status()
            visited.add(url)
            pages[url] = response.text
            print(f"Crawled: {url}")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                absolute_link = urljoin(url, link['href'])
                if urlparse(absolute_link).netloc == urlparse(base_url).netloc:
                    to_visit.append(absolute_link)

            if to_visit:
                time.sleep(politeness_window)
        except requests.RequestException as e:
            print(f"Failed to crawl {url}: {e}")

    return pages