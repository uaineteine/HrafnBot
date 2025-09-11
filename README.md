# HrafnBot [![Execution Tests](https://github.com/uaineteine/HrafnBot/actions/workflows/ExecutionTests.yaml/badge.svg)](https://github.com/uaineteine/HrafnBot/actions/workflows/ExecutionTests.yaml)

![icon](https://raw.githubusercontent.com/uaineteine/HrafnBot/main/doc/hrafnicon.png)

HrafnBot is a CLI tool that downloads files from URLs specified in a CSV file and saves them to relative locations on your local machine. It can be installed system-wide and run from anywhere using the `hrafnbot` command.

## Installation

### Quick Install
1. Clone or download this repository
2. Run the installer with your desired installation directory:

**Linux/Mac:**
```sh
python install.py /opt/hrafnbot
```

**Windows:**
```sh
python install.py C:\Tools\HrafnBot
```

The installer will:
- Copy all necessary files to the installation directory
- Install Python dependencies automatically
- Add the installation directory to your system PATH
- Make the `hrafnbot` command available globally

### Installation Options
```sh
python install.py <install_directory> [OPTIONS]

Options:
  --no-path    Don't automatically add to PATH
  --no-deps    Don't install Python dependencies
```

## Requirements
* Python 3.x
* requests library
* pandas library
* uainepydat library

Dependencies are automatically installed during the installation process, or you can install them manually:

```sh
pip install -r requirements.txt
```

## Usage

### After Installation
Once installed, you can use HrafnBot from anywhere:

```sh
hrafnbot <input_file.csv>
```

### Input File Format
Prepare a CSV file with two columns:
- The first column should contain the URLs of the files to be downloaded
- The second column should contain the relative paths where the files should be saved

Example CSV content:
```
https://example.com/file1.txt, downloads/file1.txt
https://example.com/file2.txt, downloads/file2.txt
```

### Examples
```sh
# Download files specified in myfiles.csv
hrafnbot myfiles.csv

# Get help
hrafnbot --help
```

### Legacy Usage (Backwards Compatible)
You can still run the original script directly:
```sh
python hrafn_retrieve.py path/to/your/file.csv
```

##  Script Description
The script consists of the following functions:

* read_data_from_file(file_path): Reads the CSV file and returns two lists: one with URLs and another with relative locations.
* download_file(url, save_path): Downloads a file from the given URL and saves it to the specified path.
* main(file_path): Main function that orchestrates reading the CSV file, creating necessary directories, and downloading files.

## License
This project is licensed under the MIT License.
