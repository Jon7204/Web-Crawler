import json
import os

from search import print_word, find_pages
from indexer import build_index
from crawler import crawl

url = "https://quotes.toscrape.com"


def main():
    index = None
    while True:
        command = input("> ").lower()
        if command == "quit" or command == "exit" or command == "q":
            break

        elif command == "build":
            print(f"Crawling {url}")
            pages = crawl(url)
            print(f"Building index for {len(pages)} pages")
            index = build_index(pages)

            print("Index built. Saving index to data/index.json")
            json_index = json.dumps(index, indent=2)
            with open("data/index.json", "w") as f:
                f.write(json_index)
            print("Index built and saved to data/index.json")

        elif command == "load":
            if os.path.exists("data/index.json"):
                with open("data/index.json", "r") as f:
                    index = json.load(f)
                print("Index loaded from data/index.json")
            else:
                print("No index found. Please build the index first.")
        
        elif command.startswith("print "):
            if index is not None:
                word = command[6:]
                print_word(word, index)
            else:
                print("No index loaded. Please build or load the index first.")
        
        elif command.startswith("find "):
            if index is not None:
                words = command[5:].split()
                pages = find_pages(words, index)
                if pages:
                    print(f"Pages containing all words {words}:")
                    for page in pages:
                        print(f"  {page}")
                else:
                    print(f"No pages found containing all words {words}.")
            else:
                print("No index loaded. Please build or load the index first.")
        else:
            print("Unknown command. Please try again.")
        
if __name__ == "__main__":
    main()