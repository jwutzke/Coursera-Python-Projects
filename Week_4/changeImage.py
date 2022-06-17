#!/usr/bin/env python3
"""Resize & Convert all TIFF images in image_folder to output_format.

Usage: ./process_images.py output_format image_folder output_size
Example: ./process_images.py jpeg ~/supplier-data/images 640x480
Note: output_rotation is in degrees counter-clockwise
"""

import sys
from os import listdir
from os.path import isfile, join, splitext, basename
from PIL import Image


def get_files(file_folder, extension):
    """Return a list of files from file_folder."""
    return [f for f in listdir(file_folder) if isfile(join(file_folder, f))
            and extension in f]


def resize_image(image, size):
    """Resize image to size."""
    x, y = parse_size(size)
    return image.resize((int(x), int(y)))


def save_image(image, filename_out, format_out):
    """Save image being processed as filename."""
    return image.save(filename_out, format=format_out)


def parse_size(size_string):
    """Return size as a list with x as [0] and y as [1]."""
    return size_string.split("x")


if len(sys.argv) == 1:
    print("Usage: ./{} output_format image_folder output_size".
          format(basename(__file__)))
    sys.exit(2)
try:
    output_format = sys.argv[1]
    image_folder = sys.argv[2]
    output_size = sys.argv[3]
except IndexError:
    print("ERROR: You did not enter all required parameters.")
    print("Usage: ./{} output_format image_folder output_size".
          format(basename(__file__)))
    sys.exit(2)

for filename in get_files(image_folder, ".tiff"):
    filename_in = "{}/{}".format(image_folder, filename)
    filename_out = "{}/{}.{}".format(image_folder,
                                     splitext(filename)[0],
                                     output_format)

    with Image.open(filename_in) as im:
        print("Opened: {}".format(filename_in))
        if im.format == "TIFF":
            print("{} is a {} mode: {}".format(filename, im.format, im.mode))
            im = resize_image(im, output_size)
            print("Saving as {} in {} format".format(filename_out,
                                                     output_format))
            im = im.convert("RGB")
            save_image(im, filename_out, output_format.upper())
