# import os
# import json
# import requests
# from urllib.parse import urlparse

# # Helper function: Create directory if it doesn't exist
# def create_dir(path):
#     if not os.path.exists(path):
#         os.makedirs(path)

# # Helper function: Download a file
# def download_file(url, save_path):
#     try:
#         response = requests.get(url, stream=True)
#         response.raise_for_status()
#         with open(save_path, 'wb') as file:
#             for chunk in response.iter_content(chunk_size=8192):
#                 file.write(chunk)
#         print(f"Downloaded: {save_path}")
#     except Exception as e:
#         print(f"Failed to download {url}: {e}")

# # Main function to download files from JSON
# def download_from_json(input_json, output_dir):
#     # Load the JSON data
#     with open(input_json, 'r', encoding='utf-8') as f:
#         data = json.load(f)
    
#     for entry in data:
#         main_title = entry.get("title", "Untitled").replace(" ", "_")
#         title_dir = os.path.join(output_dir, main_title)
#         create_dir(title_dir)
        
#         # Download main downloadable links
#         for link in entry.get("downloadable_links", []):
#             link_url = link.get("url")
#             link_text = link.get("text", "file").replace(" ", "_")
#             filename = os.path.join(title_dir, os.path.basename(urlparse(link_url).path) or f"{link_text}.unknown")
#             download_file(link_url, filename)
        
#         # Handle subtitles and their links
#         for subtitle_entry in entry.get("subtitles", []):
#             subtitle = subtitle_entry.get("subtitle", "Subtitle").replace(" ", "_")
#             subtitle_dir = os.path.join(title_dir, subtitle)
#             create_dir(subtitle_dir)
            
#             for sublink in subtitle_entry.get("downloadable_links", []):
#                 sublink_url = sublink.get("url")
#                 sublink_text = sublink.get("text", "file").replace(" ", "_")
#                 subfilename = os.path.join(subtitle_dir, os.path.basename(urlparse(sublink_url).path) or f"{sublink_text}.unknown")
#                 download_file(sublink_url, subfilename)

#     print(f"All files downloaded to {output_dir}")

# # Example usage
# if __name__ == "__main__":
#     download_from_json("downloadable_links.json", "downloads")


import os
import json
import requests
import re
from urllib.parse import urlparse
from PyPDF2 import PdfReader

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

# Function to extract heading from a PDF file
def extract_heading_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            # Get the text from the first page
            page = reader.pages[0]
            text = page.extract_text()
            
            # Split the text into lines and take the first non-empty line as the heading
            lines = text.split('\n')
            heading = lines[0].strip()
            return heading
    except Exception as e:
        print(f"Failed to extract heading from {pdf_path}: {e}")
        return None

# Function to clean up the extracted heading for use as a filename
def clean_filename(text):
    return re.sub(r'[^a-zA-Z0-9\s]', '', text).replace(" ", "_").lower()

# Main function to download files from JSON
def download_from_json(input_json, output_dir):
    # Load the JSON data
    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for entry in data:
        main_title = entry.get("title", "Untitled").replace(" ", "_")
        title_dir = os.path.join(output_dir, main_title)
        create_dir(title_dir)
        
        # Download main downloadable links
        for link in entry.get("downloadable_links", []):
            link_url = link.get("url")
            link_text = link.get("text", "file").replace(" ", "_")
            filename = os.path.join(title_dir, os.path.basename(urlparse(link_url).path) or f"{link_text}.unknown")
            download_file(link_url, filename)

            # Extract heading and rename file
            heading = extract_heading_from_pdf(filename)
            if heading:
                new_filename = clean_filename(heading) + ".pdf"
                new_file_path = os.path.join(title_dir, new_filename)
                os.rename(filename, new_file_path)
                print(f"Renamed {filename} to {new_filename}")
        
        # Handle subtitles and their links
        for subtitle_entry in entry.get("subtitles", []):
            subtitle = subtitle_entry.get("subtitle", "Subtitle").replace(" ", "_")
            subtitle_dir = os.path.join(title_dir, subtitle)
            create_dir(subtitle_dir)
            
            for sublink in subtitle_entry.get("downloadable_links", []):
                sublink_url = sublink.get("url")
                sublink_text = sublink.get("text", "file").replace(" ", "_")
                subfilename = os.path.join(subtitle_dir, os.path.basename(urlparse(sublink_url).path) or f"{sublink_text}.unknown")
                download_file(sublink_url, subfilename)

                # Extract heading and rename the subtitle file
                heading = extract_heading_from_pdf(subfilename)
                if heading:
                    new_subfilename = clean_filename(heading) + ".pdf"
                    new_subfile_path = os.path.join(subtitle_dir, new_subfilename)
                    os.rename(subfilename, new_subfile_path)
                    print(f"Renamed {subfilename} to {new_subfilename}")

    print(f"All files downloaded and renamed in {output_dir}")

# Example usage
if __name__ == "__main__":
    download_from_json("downloadable_links.json", "downloads2")
