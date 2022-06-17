#!/usr/bin/env python3
"""Django fruit catalog importer.

Adds contents of .txt files in description_directory to django at django_REST_URL.
.txt file Contents should be 4 sections separated by new-lines.

Usage: ./run.py description_directory django_REST_URL
Example ./run.py supplier-data/descriptions http://127.0.0.1/fruits
"""
from os import listdir
from os.path import isfile, join, basename, splitext
import sys
import requests
from re import sub


def get_files(file_folder, extension):
    """Return a list of files from file_folder containing extension."""
    return [f for f in listdir(file_folder) if isfile(join(file_folder, f))
            and extension in f]


if len(sys.argv) == 1:
    print("Usage: ./{} description_directory django_REST_URL".
          format(basename(__file__)))
    sys.exit(2)

try:
    description_directory = sys.argv[1]
    rest_url = sys.argv[2]
except IndexError:
    print("ERROR: You did not enter all required parameters.")
    sys.exit(2)

# List all .txt files in description_directory/argv[1]
for filename in get_files(description_directory, ".txt"):
    print("Opening: {}".format(description_directory + "/" + filename))
    # Open each .txt file
    with open(description_directory + "/" + filename) as file:
        try:
            file_contents = file.read()
        except OSError as error:
            print(error)
            print("Could not read file: {}".
                  format(description_directory + "/" + filename))
            sys.exit(1)

    # For each file make a dictionary
    split_file_contents = file_contents.split("\n")
    try:
        post_dict = {"name": split_file_contents[0].strip(),
                     # Remove all non-digit characters
                     "weight": int(sub(r"[\D]", "",
                                       split_file_contents[1].strip())),
                     "description": split_file_contents[2].strip(),
                     "image_name": splitext(filename)[0]+".jpeg"}
    except IndexError:
        print("ERROR: There were not 4 sections in {}".format(filename))
        sys.exit(1)
    # Post each dictionary to http://external.ip/feedback
    response = requests.post(rest_url, json=post_dict)
    # Check status code, 201 = succeeded
    if response.status_code == 201:
        print("Successfully POSTed {} to {}".format(filename, rest_url))
    else:
        print("Failed to POST {} to {} with status code: {}".
              format(filename, rest_url, response.status_code))
