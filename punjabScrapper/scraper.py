
import os
import json
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings()


# Helper Function: Clean strings for uniformity
def clean_text(text):
    return " ".join(text.split()).strip()

# Function: Scrape URLs and Save Downloadable Links
def scrape_links_and_save(input_json, output_json):
    # Read the input JSON file
    with open(input_json, 'r', encoding='utf-8') as f:
        sources = json.load(f)

    # Initialize the output structure
    output_data = []

    # Process each source
    for source in sources:
        urls = source.get("urls")  # Expecting a list of URLs
        main_title = clean_text(source.get("title", "Untitled"))

        if not isinstance(urls, list):
            print(f"Skipping entry with invalid 'urls' format: {urls}")
            continue

        for main_url in urls:  # Iterate over each URL in the list
            print(f"Scraping URL: {main_url}")

            # Initialize data for this URL
            main_data = {
                "title": main_title,
                "url": main_url,
                "subtitles": [],
                "downloadable_links": []
            }

            # Set to track unique links
            unique_links = set()

            try:
                # Fetch the HTML content
                response = requests.get(main_url, verify=False)
                print("1")
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                print("2")

                # Find all anchor tags with downloadable links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if href.lower().endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx')):
                        link_text = clean_text(link.text)
                        link_data = {"text": link_text, "url": href}

                        # Add unique links only
                        if href not in unique_links:
                            unique_links.add(href)
                            main_data["downloadable_links"].append(link_data)
                        else:
                            print(f"Duplicate link found and skipped: {href}")

                # Find subtitles and their links
                for subtitle_tag in soup.find_all(['h2', 'h3']):  # Adjust tags if needed
                    subtitle_text = clean_text(subtitle_tag.text)
                    subtitle_links = []
                    for sibling in subtitle_tag.find_all_next('a', href=True):
                        sibling_href = sibling['href']
                        if sibling_href.lower().endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx')):
                            sibling_text = clean_text(sibling.text)
                            sibling_link_data = {"text": sibling_text, "url": sibling_href}

                            # Add unique links only
                            if sibling_href not in unique_links:
                                unique_links.add(sibling_href)
                                subtitle_links.append(sibling_link_data)
                            else:
                                print(f"Duplicate subtitle link found and skipped: {sibling_href}")

                    if subtitle_links:
                        main_data["subtitles"].append({
                            "subtitle": subtitle_text,
                            "downloadable_links": subtitle_links
                        })

            except Exception as e:
                print(f"Error processing {main_url}: {e}")

            # Add the scraped data for this URL to the output
            output_data.append(main_data)

    # Save the output data to JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"Scraped data saved to {output_json}")

# Example Usage
if __name__ == "__main__":
    scrape_links_and_save("punj_docs_urls.json", "downloadable_links.json")


