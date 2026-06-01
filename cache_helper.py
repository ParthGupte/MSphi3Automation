import json
import os

CACHE_FILE = "author_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

SEARCH_CACHE_FILE = "search_cache.json"

def load_search_cache():
    if os.path.exists(SEARCH_CACHE_FILE):
        with open(SEARCH_CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_search_cache(cache):
    with open(SEARCH_CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)