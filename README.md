# HrafnBot [![Execution Tests](https://github.com/uaineteine/HrafnBot/actions/workflows/ExecutionTests.yaml/badge.svg)](https://github.com/uaineteine/HrafnBot/actions/workflows/ExecutionTests.yaml)

![icon](https://raw.githubusercontent.com/uaineteine/HrafnBot/main/doc/hrafnicon.png)

This script downloads files from URLs specified in a CSV file and saves them to relative locations on your local machine.

## Requirements
* Python 3.x
* requests library
* pandas library

You can install the required libraries using pip:

```sh
pip install requests pandas
```

## Usage
Prepare a CSV file with two columns:
The first column should contain the URLs of the files to be downloaded.
The second column should contain the relative paths where the files should be saved.

Example CSV content:
https://example.com/file1.txt, downloads/file1.txt
https://example.com/file2.txt, downloads/file2.txt

Run the script with the path to the CSV file as an argument:
```sh
python file_downloader.py path/to/your/file.csv
```
This will download the files specified in example.csv and save them to the specified relative locations.

##  Script Description
The script consists of the following functions:

* read_data_from_file(file_path): Reads the CSV file and returns two lists: one with URLs and another with relative locations.
* download_file(url, save_path): Downloads a file from the given URL and saves it to the specified path.
* main(file_path): Main function that orchestrates reading the CSV file, creating necessary directories, and downloading files.

## License
This project is licensed under the MIT License.
