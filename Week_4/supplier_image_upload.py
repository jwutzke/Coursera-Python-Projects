#!/usr/bin/env python3
"""Image Uploader.

This script uploads images to a webserver via post unauthenticated
Usage: ./supplier_image_upload.py image_folder server_url
Example:
"""
from os import listdir
from os.path import isfile, join, basename
import sys
import requests


def get_files(file_folder, extension):
    """Return a list of files from file_folder."""
    return [f for f in listdir(file_folder) if isfile(join(file_folder, f))
            and extension in f]


def upload_file(url, filename):
    """Upload filename to url."""
    with open(filename, 'rb') as file:
        return requests.post(url, files={'file': file})


def main(argv):
    """Get list of JPEGs and upload to server_url."""
    if len(argv) == 1:
        print("Usage: ./{} image_folder server_url".
              format(basename(__file__)))
        sys.exit(2)
    try:
        image_folder = sys.argv[1]
        server_url = sys.argv[2]
    except IndexError:
        print("You did not enter all required parameters.")
        sys.exit(2)

    for filename in get_files(image_folder, ".jpeg"):
        upload = upload_file(server_url, "{}/{}".format(image_folder,
                                                        filename))
        if upload.status_code == 201:
            print("Successfully POSTed {} to {}".format(filename, server_url))
        else:
            print("Failure POSTing {} to {}".format(filename, server_url))


if __name__ == "__main__":
    main(sys.argv)
