import asyncio
from urllib.parse import urlparse, parse_qs
from playwright.async_api import async_playwright


async def scrape_top_results(query: str, num_results: int = 5) -> list[str]:
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()


        await page.goto("https://duckduckgo.com/")
        await page.fill("input[name='q']", query)
        await page.keyboard.press("Enter")

        await asyncio.sleep(5)

        await page.wait_for_selector("a", timeout=10000)

        # Step 2: Get raw DuckDuckGo redirect links
        raw_links = await page.eval_on_selector_all(
            "a", "elements => elements.map(e => e.href)"
        )

        # Step 3: Extract real destination URLs
        links = []
        for url in raw_links:
            if not url:
                continue

            try:
                parsed = urlparse(url)
            except:
                continue

            if "duck.ai" in (parsed.hostname or ""):
                continue

            if "duckduckgo" in url:
                continue

            if parsed.scheme not in ("http", "https"):
                continue

            links.append(url)

        # Remove duplicates
        links = list(set(links))

        print(f"Number of URLs found: {len(links)}. Using top {num_results} results.")

        top_links = links[:num_results]

        # Step 4: Visit each URL and extract body text
        for idx, url in enumerate(top_links):
            try:
                new_page = await browser.new_page()
                await new_page.goto(url, timeout=15000)
                await new_page.wait_for_load_state("domcontentloaded")

                # Basic body text extraction
                body_text = await new_page.locator("body").inner_text()
                results.append(body_text.strip())
                print(f"Extracted {len(body_text.strip())} characters.")
                await new_page.close()
            except Exception as e:
                print(f"Failed to scrape {url}: {e}")
                continue

        await browser.close()

    return results


# Optional: test run
if __name__ == "__main__":
    query = "top 10 delhi tourist places"
    scraped_texts = asyncio.run(scrape_top_results(query))

    print(f"Extracted content from {len(scraped_texts)} pages.\n")
    # for i, text in enumerate(scraped_texts):
        # print(f"\n=== Page {i+1} Preview ===\n{text[:1000]}\n{'='*50}")
