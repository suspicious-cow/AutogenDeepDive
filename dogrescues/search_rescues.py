# filename: search_rescues.py
import requests
import csv
import os

# Function to perform a web search using Google Custom Search JSON API
def google_search(search_term, api_key, cse_id, **kwargs):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': search_term,
        'cx': cse_id,
        'key': api_key,
    }
    params.update(kwargs)
    response = requests.get(search_url, params=params)
    return response.json()

# Function to extract relevant information from search results
def extract_info(results):
    info_list = []
    for item in results.get('items', []):
        title = item.get('title')
        snippet = item.get('snippet')
        if 'foster' in snippet.lower() or 'rescue' in snippet.lower():
            info = {
                'Title': title,
                'URL': item.get('link')
            }
            info_list.append(info)
    return info_list

# Replace with your actual API key and search engine ID
API_KEY = 'YOUR_API_KEY'
SEARCH_ENGINE_ID = 'YOUR_SEARCH_ENGINE_ID'

# Perform the search
search_results = google_search('dog rescue and foster organizations', API_KEY, SEARCH_ENGINE_ID, num=10)

# Extract information from search results
rescue_info = extract_info(search_results)

# Save the information to a CSV file
output_file = 'rescues_info.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Title', 'URL']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for info in rescue_info:
        writer.writerow(info)

print(f"Search completed. Information saved to {output_file}")