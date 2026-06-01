import requests
import time
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from ddgs import DDGS
from cache_helper import *
import random

def search_author(author_name, num_results=5):
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(author_name+" Google Scholar", max_results=num_results):
            results.append({
                "title": r.get("title", ""),
                "link": r.get("href", "")
            })

    return results

def search_author_cached(author_name, cache, num_results=5):
    key = author_name.lower()

    # --- cache hit ---
    if key in cache:
        print(f"CACHE HIT (search): {author_name}")
        return cache[key]

    # --- cache miss ---
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(author_name + " Google Scholar", max_results=num_results):
            results.append({
                "title": r.get("title", ""),
                "link": r.get("href", "")
            })

    # only cache if non-empty (avoid caching failures)
    if results:
        cache[key] = results

    return results


def score_link(link, title, author_name):
    score = 0
    domain = urlparse(link).netloc.lower()
    url = link.lower()
    title = title.lower()
    name = author_name.lower()

    # --- strong positives ---
    if ".edu" in domain or ".ac." in domain:
        score += 5

    if any(k in url for k in ["people", "faculty", "person", "~"]):
        score += 4

    if any(k in title for k in ["professor", "university", "lab"]):
        score += 3

    # name match
    name_parts = name.split()
    if all(part in url or part in title for part in name_parts):
        score += 3

    # --- negatives ---
    if any(bad in domain for bad in [
        "scholar.google", "researchgate", "linkedin",
        "twitter", "youtube", "dblp"
    ]):
        score -= 5

    if link.endswith(".pdf"):
        score -= 3

    return score

def pick_homepage(results):
    for r in results:
        link = r["link"]
        title = r['title']

        # prefer personal domains or university pages
        if 'scholar.google' in link:
            return r

    return results[0] if results else None

def get_author_homepage_from_search(author_name, cache):
    results = search_author_cached(author_name, cache, 10)

    best = pick_homepage(results)

    return {
        "name": author_name,
        "homepage": best["link"] if best else None,
        "candidates": results
    }

def get_all_homepages(authors):
    search_cache = load_search_cache()
    results = []

    for i, name in enumerate(authors):
        try:
            info = get_author_homepage_from_search(name, search_cache)

            if info:
                results.append(info)

            print(f"{i+1}/{len(authors)} done: {name}")

            # save cache periodically
            if i % 5 == 0:
                save_search_cache(search_cache)

            time.sleep(random.uniform(2, 4))  # safer than fixed sleep

        except Exception as e:
            print(f"Error for {name}: {e}")

    # final save
    save_search_cache(search_cache)

    return results

# authors = [
#     "Chandra Shekhar Seelamantula",
#     "Se Young Yun"
# ]

# data = get_all_homepages(authors)

# print(data)


# search_query = scholarly.search_author("Zhouchen Lin")

# results = list(search_query)
# print(len(results))