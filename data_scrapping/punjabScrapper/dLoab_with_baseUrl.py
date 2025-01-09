import os
import json
import requests
from urllib.parse import urljoin

# Helper function: Create directory if it doesn't exist
def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Helper function: Download a file
def download_file(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {save_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Function to get the adjusted base URL
def get_base_url(base_url):
    return "/".join(base_url.rstrip("/").split("/")[:-1]) + "/"

# Main function to download files from JSON
def download_from_json(input_json, output_dir, base_url):
    # Adjust the base URL
    adjusted_base_url = get_base_url(base_url)
    
    # Load the JSON data
    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for entry in data:
        main_title = entry.get("title", "Untitled").replace(" ", "_")
        title_dir = os.path.join(output_dir, main_title)
        create_dir(title_dir)
        
        # Download main downloadable links
        for link in entry.get("downloadable_links", []):
            relative_url = link.get("url")
            if not relative_url.startswith(("http", "https")):
                full_url = urljoin(adjusted_base_url, relative_url)
            else:
                full_url = relative_url

            link_text = link.get("text", "file").replace(" ", "_")
            filename = os.path.join(title_dir, os.path.basename(relative_url))
            download_file(full_url, filename)
        
        # Handle subtitles if necessary
        for subtitle_entry in entry.get("subtitles", []):
            subtitle = subtitle_entry.get("subtitle", "Subtitle").replace(" ", "_")
            subtitle_dir = os.path.join(title_dir, subtitle)
            create_dir(subtitle_dir)
            
            for sublink in subtitle_entry.get("downloadable_links", []):
                relative_url = sublink.get("url")
                if not relative_url.startswith(("http", "https")):
                    full_url = urljoin(adjusted_base_url, relative_url)
                else:
                    full_url = relative_url

                sublink_text = sublink.get("text", "file").replace(" ", "_")
                subfilename = os.path.join(subtitle_dir, os.path.basename(relative_url))
                download_file(full_url, subfilename)

    print(f"All files downloaded to {output_dir}")

# Example usage
if __name__ == "__main__":
    base_url = "https://ekhidmat.punjab.gov.pk/ekhidmat-downloads/"
    download_from_json("downloadable_links.json", "downloads", base_url)
