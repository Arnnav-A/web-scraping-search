import argparse
import asyncio

from validator import is_valid_query
from similarity import get_similar_query, add_query_result
from scraper import scrape_top_results
from summary import summarize_scraped_texts


def process_query(query: str):
    if not is_valid_query(query):
        print("Invalid query.")
        return

    print("Valid query!")

    cached_answer = get_similar_query(query)

    if cached_answer:
        print("Cached answer found:\n")
        print(cached_answer)
    else:
        print("No cached answer found. Scraping and summarizing...\n")
        scraped_texts = asyncio.run(scrape_top_results(query))
        answer = summarize_scraped_texts(scraped_texts, query)
        add_query_result(query, answer)
        print("Generated answer:\n")
        print(answer)


def main():
    parser = argparse.ArgumentParser(description="Web Scraping CLI App")
    parser.add_argument("query", type=str, nargs="+", help="Your search query")

    args = parser.parse_args()
    full_query = " ".join(args.query)
    process_query(full_query)


if __name__ == "__main__":
    main()
