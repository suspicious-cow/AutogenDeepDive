# filename: check_csv_content.py
import csv

# Load the URLs from the CSV file
input_file = 'rescues_info.csv'

# Read the CSV file and print the first few rows
with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    # Print the header
    header = next(reader)
    print(header)
    # Print the first 5 rows of data
    for i, row in enumerate(reader):
        print(row)
        if i >= 4:  # Only print the first 5 rows
            break