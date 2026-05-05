HELP_TEXT = """
Available commands:
  build              Crawl quotes.toscrape.com and build the inverted index
  load               Load a previously built index from disk
  print <word>       Display the index entry for a word
  find <query>       Search for pages containing your query
  help               Show this help message
  quit / exit / q    Exit the tool

Specific help for each command:
  build --help       Instructions for building the index
  load --help        Instructions for loading the index
  print --help       Instructions for printing a word's index entry
  find --help        Instructions for searching the index

Find query syntax:
  find love                    Single word search
  find good friends            Multi-word search (all words must appear)
  find love AND friendship     Pages containing both words
  find love OR friendship      Pages containing either word
  find love NOT death          Pages with 'love' but not 'death'

Tips:
  - Boolean operators must be uppercase (AND, OR, NOT)
  - Results are ranked by TF-IDF relevance score
  - If a word is not found, similar words will be suggested
  - Common words like 'the', 'a', 'is' are filtered out automatically
"""

PRINT_HELP = """
print <word>
  Displays the inverted index entry for a given word.
  Shows every page the word appears on, its frequency, and token positions.
  Example: print love
"""

FIND_HELP = """
find <query>
  Searches the index for pages matching your query.
  Supports single words, multi-word, and boolean operators (AND, OR, NOT).
  Results are ranked by TF-IDF relevance score.
  Examples:
    find indifference
    find good friends
    find love AND friendship
    find love OR hope
    find love NOT death

  Note:
  - Boolean operators must be uppercase (AND, OR, NOT)
  - Boolean operators cannot start or end the query
  - Empty words in the query are not allowed
  - Different operators cannot be mixed in the same query (e.g. 'love AND hope OR joy' is invalid)
  - Results are ranked by TF-IDF relevance score
"""

BUILD_HELP = """
build
  Crawls quotes.toscrape.com and builds the inverted index.
  Observes a 6 second politeness window between requests.
  Saves the index to data/index.json when complete.
"""

LOAD_HELP = """
load
  Loads the inverted index from data/index.json.
  Run 'build' first if no index exists yet.
"""