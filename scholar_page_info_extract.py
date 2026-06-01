import requests
from bs4 import BeautifulSoup
import time
import random
from cache_helper import *
import re


def fetch_scholar_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        raise Exception(f"HTTP error: {r.status_code}")

    if is_blocked_page(r.text):
        raise Exception("Blocked by Google Scholar")

    return BeautifulSoup(r.text, "html.parser")

def is_blocked_page(html):
    html_lower = html.lower()

    indicators = [
        "unusual traffic",
        "not a robot",
        "recaptcha",
        "detected unusual traffic",
        "/sorry/index"
    ]

    return any(ind in html_lower for ind in indicators)

def is_valid_metrics(stats):
    return (
        stats.get("citations", 0) > 0 or
        stats.get("h-index", 0) > 0
    )

def extract_stats(soup):
    stats = {}

    # ---- extract citation stats ----
    rows = soup.find_all("tr")

    for row in rows:
        cols = row.find_all("td")

        if len(cols) >= 2:
            key = cols[0].get_text(strip=True).lower()
            val = cols[1].get_text(strip=True)

            if key in ["citations", "h-index", "i10-index"]:
                try:
                    stats[key] = int(val)
                except:
                    stats[key] = 0

    # ---- extract affiliation ----
    aff_tag = soup.find("a", class_="gsc_prf_ila")

    if aff_tag:
        stats["affiliation"] = aff_tag.get_text(strip=True)
    else:
        stats["affiliation"] = None

    return stats

def extract_yearly_citations(soup):
    scripts = soup.find_all("script")

    for script in scripts:
        text = script.string or script.text

        if not text:
            continue

        if "gsc_g_hist_data" in text:
            # try to extract JSON object
            match = re.search(r"gsc_g_hist_data\s*=\s*(\{.*?\});", text, re.DOTALL)

            if match:
                try:
                    return json.loads(match.group(1))
                except:
                    pass

            # fallback: try generic JSON extraction
            match = re.search(r"(\{.*\"citations\".*\})", text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except:
                    pass

    return None

def get_author_metrics(scholar_url):
    soup = fetch_scholar_page(scholar_url)

    stats = extract_stats(soup)

    if not is_valid_metrics(stats):
        raise Exception("Invalid or empty Scholar page")

    yearly = extract_yearly_citations(soup)

    return {
        "citations": stats.get("citations", 0),
        "hindex": stats.get("h-index", 0),
        "i10index": stats.get("i10-index", 0),
        "affiliation": stats.get("affiliation"),
        "yearly": yearly
    }

def is_good_advisor(metrics):
    c = metrics["citations"]
    h = metrics["hindex"]

    return (
        c > 2000 or     # established
        h > 20          # strong academic signal
    )

def score_author(metrics):
    c = metrics["citations"]
    h = metrics["hindex"]

    score = 0

    score += min(c / 1000, 50)   # cap influence
    score += h * 2

    return score

def process_author_cached(scholar_url, cache):
    # --- cache hit ---
    if scholar_url in cache:
        return cache[scholar_url]

    # --- cache miss ---
    result = process_author(scholar_url)

    cache[scholar_url] = result
    return result

def process_author(scholar_url):
    metrics = get_author_metrics(scholar_url)

    return {
        "metrics": metrics,
        "is_good": is_good_advisor(metrics),
        "score": score_author(metrics)
    }

def process_all_authors(pages):
    cache = load_cache()
    filtered = []

    for i, p in enumerate(pages):
        try:
            author_metrics = process_author_cached(p['homepage'], cache)

            if author_metrics and author_metrics.get("is_good"):
                p["overall_metrics"] = author_metrics
                filtered.append(p)

            print(f"{i+1}/{len(pages)} done")

            # save periodically (important)
            if i % 5 == 0:
                save_cache(cache)

            time.sleep(random.uniform(2, 5))

        except Exception as e:
            print(f"Error processing {p.get('homepage')}: {e}")

    # final save
    save_cache(cache)

    return filtered

if __name__ == '__main__':
    print(process_author("https://scholar.google.co.in/citations?user=1g1i1B4AAAAJ&hl=en"))
    print(process_author("https://scholar.google.com/citations?user=X_IAjb8AAAAJ&hl=en"))