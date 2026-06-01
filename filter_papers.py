

def is_image_video_generation_paper(paper, threshold=2):
    def get_text(field):
        if field is None:
            return ""
        if isinstance(field, dict):
            return field.get("value", "")
        return str(field)

    # extract fields safely
    title = get_text(paper.get("title"))
    abstract = get_text(paper.get("abstract"))
    tldr = get_text(paper.get("TLDR"))

    text = f"{title} {abstract} {tldr}".lower()

    # keyword groups
    strong_keywords = [
        "diffusion",
        "text-to-image",
        "image generation",
        "video generation",
        "generative model",
        "latent diffusion",
        "denoising",
        "flow matching",
        "generation"
    ]

    weak_keywords = [
        "gan",
        "transformer for vision",
        "image synthesis",
        "video synthesis",
        "multimodal generation",
        "visual generation",
        "generative"
    ]

    score = 0

    for k in strong_keywords:
        if k in text:
            score += 2

    for k in weak_keywords:
        if k in text:
            score += 1

    return score >= threshold

def is_spotlight_or_oral(paper):
    return paper['venue']['value'] != 'NeurIPS 2025 poster'

def filter_good_papers(papers):
    return[
        p for p in papers
        if is_spotlight_or_oral(p)
    ]



def filter_generation_papers(papers):
    return [
        p for p in papers
        if is_image_video_generation_paper(p)
    ]

def authors_list(papers):
    authors = []
    for p in papers:
        p_authors = p['authors']['value']
        for a in p_authors:
            if a not in authors:
                authors.append(a)
    return authors

if __name__ == '__main__':
    from scraping_openreview import get_neurips_papers
    papers = get_neurips_papers(2025)
    gen_papers = filter_generation_papers(papers)
    good_papers = filter_good_papers(gen_papers)
    good_paper_authors = authors_list(good_papers)
    print(good_paper_authors[:100])