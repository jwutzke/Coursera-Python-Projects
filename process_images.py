#!/usr/bin/env python3

# Resize, Rotate, and Convert all TIFF images in FOLDER_IN, save to FOLDER_OUT
# Usage: ./process_images.py output_format output_rotation output_size
# Example: ./process_images.py jpeg 90 640x480
# Note: output_rotation is in degrees counter-clockwise

import sys
from os import listdir
from os.path import isfile, join
from PIL import Image

FOLDER_IN = "./images"
FOLDER_OUT = "/opt/icons"


def get_files(file_folder):
    """Return a list of files from file_folder."""
    return [f for f in listdir(file_folder) if isfile(join(file_folder, f))]


def rotate_image(image, rotation):
    """Rotate image rotation degrees."""
    return image.rotate(angle=int(rotation))


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


try:
    output_format = sys.argv[1]
    output_rotation = sys.argv[2]
    output_size = sys.argv[3]
except IndexError:
    print("You did not enter all required parameters.")
    sys.exit(1)

for filename in get_files(FOLDER_IN):
    filename_in = FOLDER_IN + "/" + filename
    filename_out = FOLDER_OUT + "/" + filename

    with Image.open(filename_in) as im:
        print("Opened: {}".format(filename_in))
        if im.format == "TIFF":
            print("{} is a {} mode: {}".format(filename, im.format, im.mode))
            im = rotate_image(im, output_rotation)
            im = resize_image(im, output_size)
            print("Saving as {} in {} format".format(filename_out, output_format))
            im = im.convert("RGB")
            save_image(im, filename_out, output_format.upper())
