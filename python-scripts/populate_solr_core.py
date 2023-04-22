import csv
import requests

# You can download this dataset from: https://drive.google.com/file/d/18SFI65X0JcUCsubm3uhtK1JexD1RsaS6/view?usp=share_link
csv_file_path = 'metadata.csv'

solr_collection = 'cord-papers'
solr_update_url = f'http://localhost:8983/solr/{solr_collection}/update?commit=true'


def encode_query(query):
    response = requests.get(f'http://localhost:8080/get-encoded-query?query={query}')
    return response.json()


# Read the CSV file and send each document to Solr for indexing
with open(csv_file_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for i, row in enumerate(reader):

        document = {
            'cord_uid': row['cord_uid'],
            'title': row['title'],
            'abstract': row['abstract'],
            'publish_time': row['publish_time'],
            'authors': row['authors'],
            'journal': row['journal'],
            'url': row['url'],
            'vector': encode_query(row['abstract']),
        }

        # Send the document to Solr for indexing
        headers = {'Content-Type': 'application/json'}
        response = requests.post(solr_update_url, headers=headers, json=[document])

        if response.status_code == 200:
            print(f"Document {i} - {row['cord_uid']} indexed successfully.")
        else:
            print(f"Failed to index document {i} - {row['cord_uid']} . Error: {response.text}")
