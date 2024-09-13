import os
import requests
import pandas as pd
import argparse

def read_data_from_file(file_path):
    df = pd.read_csv(file_path, header=None)
    urls = df.iloc[:, 0].tolist()
    relative_locations = df.iloc[:, 1].tolist()
    # Trim leading and trailing whitespace
    relative_locations = [location.strip() for location in relative_locations]
    return urls, relative_locations

def download_file(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)

def main(file_path):
    urls, relative_locations = read_data_from_file(file_path)
    
    for url, relative_location in zip(urls, relative_locations):
        if url and relative_location:
            os.makedirs(os.path.dirname(relative_location), exist_ok=True)
            download_file(url, relative_location)
            print(f"File downloaded from {url} and saved to {relative_location}")
        else:
            print("URL or relative download location not found in the document.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download files from URLs and save to relative locations.')
    parser.add_argument('file_path', type=str, help='Path to the input text file')
    args = parser.parse_args()
    main(args.file_path)
