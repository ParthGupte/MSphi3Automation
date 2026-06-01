import openreview


def get_neurips_papers(year=2025):
    client = openreview.api.OpenReviewClient(
        baseurl="https://api2.openreview.net"
    )

    venue_id = f"NeurIPS.cc/{year}/Conference"

    notes = client.get_all_notes(
        content={"venueid": venue_id}
    )

    papers = []

    for note in notes:
        content = note.content

        
        papers.append({
            "title": content.get("title"),
            "abstract": content.get("abstract"),
            "authors": content.get("authors"),
            "pdf": f"https://openreview.net/pdf?id={note.id}",
            "primary_area": content.get("primary_area"),
            "venue": content.get("venue"),
            "TLDR": content.get("TLDR"),
            "keys": content.keys()

        })

    return papers

if __name__ == '__main__':
    papers =  get_neurips_papers(2025)
    print(papers[0])
    # venues = []
    # for paper in papers:
    #     venue = paper['venue']['value']
    #     if venue not in venues:
    #         venues.append(venue)
    # print(venues)