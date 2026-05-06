import json
import os

from search import print_word, parse_query
from indexer import build_index
from crawler import crawl
from help import HELP_TEXT, PRINT_HELP, FIND_HELP, BUILD_HELP, LOAD_HELP

def main():
    url = "https://quotes.toscrape.com"
    index = None

    while True:
        # Need the raw input for queries
        raw = input("> ") # Get the raw input from the user
        command = raw.lower() # Convert the command to lowercase for easier comparison
        # Check for quit 
        if command == "quit" or command == "exit" or command == "q":
            break

        # Handle help commands
        elif command == "help":
            print(HELP_TEXT)
        elif command in ("build --help", "build --h"):
            print(BUILD_HELP)
        elif command in ("load --help", "load --h"):
            print(LOAD_HELP)
        elif command in ("print --help", "print --h"):
            print(PRINT_HELP)
        elif command in ("find --help", "find --h"):
            print(FIND_HELP)

        # Handle main commands

        elif command == "build":
            print(f"  Crawling {url}")
            pages = crawl(url)
            print(f"  Building index for {len(pages)} pages")
            index = build_index(pages)

            print("  Index built. Saving index to data/index.json")
            json_index = json.dumps(index, indent=2)
            with open("data/index.json", "w") as f:
                f.write(json_index)
            print("  Index built and saved to data/index.json")

        elif command == "load":
            if os.path.exists("data/index.json"):
                with open("data/index.json", "r") as f:
                    index = json.load(f)
                print(f"Index loaded: {len(index)} unique words from {len(set(url for postings in index.values() for url in postings))} pages.")
            else:
                print("  No index found. Please build the index first.")
        
        elif command.startswith("print "):
            if index is not None:
                word = command[6:]
                print_word(word, index)
            else:
                print("  No index loaded. Please build or load the index first.")
        
        elif command.startswith("find "):
            if index is not None:
                query = raw[5:]
                pages = parse_query(query, index)
                if pages:
                    for score, url in pages:
                        print(f"  {url} (score: {score:.4f})")
            else:
                print("  No index loaded. Please build or load the index first.")
        elif command == "print":
            print("  Please specify a word to print. Usage: print <word>")
        elif command == "find":
            print("  Please specify a query to find. Usage: find <query>")
        else:
            print("  Unknown command. Please try again.")

if __name__ == "__main__":
    main()