# filename: scrape_contact_info.py
import csv
import requests
from bs4 import BeautifulSoup

# Function to scrape contact information from a given URL
def scrape_contact_info(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        # This is a simple and naive way to find email and phone numbers, it might not work for all websites
        email = None
        phone = None
        for a in soup.find_all('a', href=True):
            if 'mailto:' in a['href']:
                email = a['href'].split('mailto:')[1]
                break
        for text in soup.stripped_strings:
            if '@' in text and '.' in text:
                email = text
                break
        # You may need to add more sophisticated methods to find the phone number
        return email, phone
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None, None

# Load the URLs from the CSV file
input_file = 'rescues_info.csv'
output_file = 'contact_info.csv'

with open(input_file, 'r', newline='', encoding='utf-8') as csvfile, \
     open(output_file, 'w', newline='', encoding='utf-8') as output_csvfile:
    reader = csv.DictReader(csvfile)
    fieldnames = ['Title', 'URL', 'Email', 'Phone']
    writer = csv.DictWriter(output_csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        title = row['Title']
        url = row['URL']
        email, phone = scrape_contact_info(url)
        writer.writerow({'Title': title, 'URL': url, 'Email': email, 'Phone': phone})

print(f"Scraping completed. Contact information saved to {output_file}")