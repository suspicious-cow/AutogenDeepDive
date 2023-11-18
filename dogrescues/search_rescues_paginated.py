# filename: search_rescues_paginated.py
import requests
import csv
import time

# Function to perform a web search using Google Custom Search JSON API
def google_search(search_term, api_key, cse_id, start_index, **kwargs):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': search_term,
        'cx': cse_id,
        'key': api_key,
        'start': start_index
    }
    params.update(kwargs)
    response = requests.get(search_url, params=params)
    return response.json()

# Function to extract relevant information from search results
def extract_info(results):
    info_list = []
    for item in results.get('items', []):
        info = {
            'Title': item.get('title'),
            'URL': item.get('link')
        }
        info_list.append(info)
    return info_list

# Replace with your actual API key and search engine ID
API_KEY = 'YOUR_API_KEY'
SEARCH_ENGINE_ID = 'YOUR_SEARCH_ENGINE_ID'

# Perform the search and paginate through results
all_rescue_info = []
for i in range(0, 100, 10):  # Adjust range as needed to get more results
    search_results = google_search('dog rescue and foster organizations', API_KEY, SEARCH_ENGINE_ID, i+1)
    rescue_info = extract_info(search_results)
    all_rescue_info.extend(rescue_info)
    time.sleep(2)  # Pause between requests to avoid rate limiting

# Save the information to a CSV file
output_file = 'rescues_info.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Title', 'URL']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for info in all_rescue_info:
        writer.writerow(info)

print(f"Search completed. Information saved to {output_file}")