#!/usr/bin/env python3
"""Generate PDF from supplier data and send via email."""
import os
from os import listdir
from os.path import isfile, join, basename
import sys
import emails
import reports
import datetime


SENDER = "automation@example.com"
recipient = "{}@example.com".format(os.environ.get('USER'))
SUBJECT = "Upload Completed - Online Fruit Store"
BODY = ("All fruits are uploaded to our website successfully."
        " A detailed list is attached to this email.")


def get_files(file_folder, extension):
    """Return a list of files from file_folder containing extension."""
    return [f for f in listdir(file_folder) if isfile(join(file_folder, f))
            and extension in f]


if len(sys.argv) == 1:
    print("Usage: ./{} description_directory".
          format(basename(__file__)))
    sys.exit(2)

try:
    description_directory = sys.argv[1]
except IndexError:
    print("ERROR: You did not enter all required parameters.")
    print("Usage: ./{} description_directory".
          format(basename(__file__)))
    sys.exit(2)

pdf_body = ""
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

    # For each file make a add to report body
    split_file_contents = file_contents.split("\n")
    try:
        pdf_body = pdf_body + """<br /><br />
        name: {}
        <br /><br />
        weight: {}
        """.format(split_file_contents[0].strip(),
                   split_file_contents[1].strip())
    except IndexError:
        print("ERROR: There were not 2+ sections in {}".format(filename))
        sys.exit(1)

title = "Processed Update on {}".format(datetime.datetime.now().strftime("%c"))
# Generate PDF file and store at /tmp/processed.pdf
reports.generate("/tmp/processed.pdf", title, pdf_body)
# Email generated PDF.
emails.send(emails.generate(SENDER, recipient, SUBJECT, BODY,
                            "/tmp/processed.pdf"))
