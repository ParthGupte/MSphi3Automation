from filter_papers import *
from author_page_finding import *
from scraping_openreview import get_neurips_papers
from scholar_page_info_extract import process_all_authors
import pandas as pd

def flatten_author(p):
    metrics = p.get("overall_metrics", {})

    return {
        "name": p.get("name"),
        "homepage": p.get("homepage"),
        "citations": metrics.get("citations"),
        "hindex": metrics.get("hindex"),
        "i10index": metrics.get("i10-index"),
        "affiliation": metrics.get("affiliation"),
        "score": metrics.get("score"),
    }



def save_to_csv(pages, filename="authors.csv"):
    flat_data = [flatten_author(p) for p in pages]

    df = pd.DataFrame(flat_data)
    df.to_csv(filename, index=False)
    df = df.sort_values(by="score", ascending=False)

    print(f"Saved {len(df)} authors to {filename}")

papers = get_neurips_papers(2025)
gen_papers = filter_generation_papers(papers)
good_papers = filter_good_papers(gen_papers)
good_paper_authors = authors_list(good_papers)
pages = get_all_homepages(good_paper_authors)
good_profs = process_all_authors(pages)
print(len(good_profs))
save_to_csv(good_profs)